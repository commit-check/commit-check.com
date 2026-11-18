# GitLab CI, Bitbucket and Azure Pipelines

On GitHub, the [Action](github-actions.md) and the [App](github-app.md) do
this work for you. Everywhere else Commit Check runs as one job in the
pipeline: it is a Python package with no runtime dependencies, so any runner
that can `pip install` can run it, and it reads the same `cchk.toml` as the
hook and the Action.

Two things are different from running it on your own machine, and each
example below handles both:

- **The checkout can be a detached HEAD**, as it is on GitLab and Azure, and
  then git has no branch to report. `commit-check --branch` reads the name
  from the CI's own variables instead, the merge or pull request's source
  branch first, so the jobs call it as is.
- **A merge request has more than one commit.** `--rev` checks one commit, so
  the job loops over the commits the merge request adds, as in
  [Checking a range of commits](../example.md#checking-a-range-of-commits).
  The loop needs the history those commits sit on, so each example turns
  shallow cloning off. If the range cannot be read, the job fails rather than
  passing with nothing checked.

Each job runs on merge or pull requests only, because the variables it reads
exist only there. Add `--author-name --author-email` to the `commit-check`
call in the loop to check each commit's author as well, and `--files` to
check the files each commit adds (configured in the `[files]` section).

The branch check (`--branch`) also covers `require_rebase_target` (CC202),
which needs the target branch in the clone. Neither GitLab nor Bitbucket
fetches it for a merge or pull request, so each job fetches it first. Without
it the rule reports itself as skipped (`rebase target 'main' not found`) and
the job passes. The jobs fetch the request's target branch; if
`require_rebase_target` names a different branch, fetch that one instead.

!!! note "On 2.18.2 or older"

    Releases before 2.18.3 read only GitHub's variables, so on a detached
    checkout `--branch` judges `HEAD`, which is always allowed, and passes
    whatever the branch is called. Pipe the name in instead: a value piped
    into `--branch` on its own is the name it checks.

    ```console
    $ echo "$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME" | commit-check --branch          # GitLab
    $ echo "$BITBUCKET_BRANCH" | commit-check --branch                             # Bitbucket
    $ echo "${SYSTEM_PULLREQUEST_SOURCEBRANCH#refs/heads/}" | commit-check --branch  # Azure
    ```

## GitLab CI

```yaml title=".gitlab-ci.yml"
commit-check:
  image: python:3.13
  variables:
    GIT_DEPTH: "0"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  script:
    - pip install commit-check
    - target="$CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
    - git fetch --quiet origin "+refs/heads/$target:refs/remotes/origin/$target"
    - commit-check --branch
    - |
      head="${CI_MERGE_REQUEST_SOURCE_BRANCH_SHA:-$CI_COMMIT_SHA}"
      shas=$(git rev-list "$CI_MERGE_REQUEST_DIFF_BASE_SHA..$head") || exit 1
      status=0
      for sha in $shas; do
        commit-check --message --rev "$sha" --compact || status=1
      done
      exit $status
```

- `GIT_DEPTH: "0"` turns shallow cloning off.
- A merge request pipeline fetches only the commit it runs on, so the job
  fetches the target branch for the rebase check. A merge request from a fork
  runs its pipeline in the fork, where `origin` is the fork: fetch from
  `"$CI_MERGE_REQUEST_PROJECT_URL.git"` instead of `origin` there, so the
  branch comes from the target project.
- In a merged results pipeline, `HEAD` is a merge commit GitLab made, and
  `CI_MERGE_REQUEST_SOURCE_BRANCH_SHA` names the merge request's own last
  commit. In a plain merge request pipeline that variable is empty and
  `CI_COMMIT_SHA` is that commit.
- The `python` image ships with git. A `-slim` image does not, and needs it
  installed first.

### Merge request title and description

GitLab passes both to the job, so they are piped in as they are. Add these
lines to the `script`, before the commit loop (its `exit` ends the script):

```yaml
    - printf '%s\n' "$CI_MERGE_REQUEST_TITLE" | commit-check --pr-title
    - printf '%s\n' "$CI_MERGE_REQUEST_DESCRIPTION" | commit-check --ai-attribution-only
```

- `--pr-title` checks the title with the message rules a one-line title can
  meet: everything `--message` runs except a body (CC011), a sign-off (CC012)
  and an AI author (CC017). With squash merges the title is often the commit
  message that lands.
- `--ai-attribution-only` checks the description against your
  `ai_attribution` policy, and, when `[pull_request] ai_declaration_checkboxes`
  is set, that it ticks exactly one AI declaration box (CC501). GitLab task
  lists (`- [x]`, `* [x]`, `1. [x]`) are read like GitHub's.
- GitLab cuts `CI_MERGE_REQUEST_DESCRIPTION` to its first 2700 characters
  (`CI_MERGE_REQUEST_DESCRIPTION_IS_TRUNCATED` is then `true`), so only that
  part is checked. Put the AI declaration boxes near the top of the merge
  request template, so a long description does not cut them off. To fail a
  description that was cut rather than check part of it, add before the
  description check:

    ```yaml
        - test "$CI_MERGE_REQUEST_DESCRIPTION_IS_TRUNCATED" != "true" || { echo "The description is over 2700 characters; GitLab passed only part of it"; exit 1; }
    ```
- Editing the title or description does not start a pipeline. Run the
  pipeline again from the merge request's **Pipelines** tab after an edit.

## Bitbucket Pipelines

```yaml title="bitbucket-pipelines.yml"
image: python:3.13

pipelines:
  pull-requests:
    '**':
      - step:
          name: Commit Check
          clone:
            depth: full
          script:
            - pip install commit-check
            - target="$BITBUCKET_PR_DESTINATION_BRANCH"
            - git fetch --quiet origin "+refs/heads/$target:refs/remotes/origin/$target"
            - commit-check --branch
            - |
              shas=$(git rev-list "$BITBUCKET_PR_DESTINATION_COMMIT..$BITBUCKET_COMMIT") || exit 1
              status=0
              for sha in $shas; do
                commit-check --message --rev "$sha" --compact || status=1
              done
              exit $status
```

- `depth: full` turns off the default clone depth of 50 commits.
- Bitbucket merges the destination branch into the pull request before the
  step runs. The range stops at `BITBUCKET_COMMIT`, the pull request's own
  last commit, so commits that only came in with that merge are not checked.
  The rebase check judges that commit too, not the merge.

### Pull request title and description

Bitbucket gives the step the pull request's id but not its title or
description, so the step reads them from the Bitbucket API. Create a
[repository access token](https://support.atlassian.com/bitbucket-cloud/docs/repository-access-tokens/)
with the **Pull requests: Read** scope, store it as a secured repository
variable named `PR_READ_TOKEN`, and add to the `script`, before the commit
loop:

```yaml
            - >-
              curl -fsS -H "Authorization: Bearer $PR_READ_TOKEN"
              "https://api.bitbucket.org/2.0/repositories/$BITBUCKET_REPO_FULL_NAME/pullrequests/$BITBUCKET_PR_ID"
              -o pr.json
            - >-
              python -c 'import json; pr = json.load(open("pr.json"));
              open("title.txt", "w").write(pr["title"]);
              open("description.txt", "w").write(pr["description"])'
            - commit-check --pr-title < title.txt
            - commit-check --ai-attribution-only < description.txt
```

Reading the fields in a step of their own makes a failed API read fail the
step, instead of piping empty text into the check. `--pr-title` and
`--ai-attribution-only` work as in the
[GitLab section](#merge-request-title-and-description). Editing a pull
request does not start a pipeline, so run the step again after an edit.

## Azure Pipelines

```yaml title="azure-pipelines.yml"
trigger: none

pr:
  branches:
    include: ["*"]

pool:
  vmImage: ubuntu-latest

steps:
  - checkout: self
    fetchDepth: 0
  - task: UsePythonVersion@0
    inputs:
      versionSpec: "3.13"
  - script: pip install commit-check
    displayName: Install Commit Check
  - script: commit-check --branch
    displayName: Check the branch name
  - script: |
      shas=$(git rev-list HEAD^1..HEAD^2) || exit 1
      status=0
      for sha in $shas; do
        commit-check --message --rev "$sha" --compact || status=1
      done
      exit $status
    displayName: Check the commit messages
```

- `trigger: none` keeps the pipeline to pull requests; on a plain push there
  is no source branch to check and no merge commit to read the range from.
- `fetchDepth: 0` turns off shallow fetch, which new pipelines have on by
  default.
- A pull request build checks out a merge commit whose first parent is the
  target branch and second the pull request, so `HEAD^1..HEAD^2` is exactly
  the commits the pull request adds.
- The branch name comes from `System.PullRequest.SourceBranch`, which is
  `refs/heads/feature/x` in Azure Repos and `feature/x` for a GitHub
  repository. Commit Check drops the `refs/heads/` prefix itself.
- In Azure Repos the `pr:` section is ignored. Pull request builds come from a
  [build validation branch policy](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies#set-build-validation)
  on the target branch, and `System.PullRequest.SourceBranch` is only set for
  builds a branch policy started.
