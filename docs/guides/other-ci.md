# GitLab CI, Bitbucket and Azure Pipelines

On GitHub, the [Action](github-actions.md) and the [App](github-app.md) check
every pull request for you. On GitLab CI and Bitbucket Pipelines one command
does that job: `commit-check-ci`, which comes with the package from 2.23.0
on. It finds the merge or pull request from the variables the CI system sets
and checks the source branch and every commit the request adds, against the
same `cchk.toml` as the hook and the Action. The title, the description, each
commit's author and the files it changes are one option away.

On Azure Pipelines, and on any other CI, the job is
[written by hand](#azure-pipelines).

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
    - commit-check-ci
```

Every check is listed under a heading of its own, and one failure fails the
job:

```text
$ commit-check-ci
Branch
  passed
Commit ccdfc043 added the login form
✖ CC001 message failed: added the login form
  The commit message should follow Conventional Commits. See https://www.conventionalcommits.org
  Suggest: Use <type>(<scope>): <description>, where <type> is one of: feat, fix, docs, style, refactor, test, chore, perf, build, ci, revert
  Docs:    https://commit-check.com/rules/#cc001

Commit 20119d2e fix: trim the user name
  passed

1 of 3 failed.
```

- `GIT_DEPTH: "0"` turns shallow cloning off, for this job only. The command
  needs every commit of the merge request and the commit they start from.
  With a clone that ends inside the merge request the job fails and names
  this setting, rather than pass with commits unchecked.
- The command fetches the target branch itself, which
  `require_rebase_target` ([CC202](../rules.md#cc202)) compares with. For a
  merge request from a fork it fetches from the target project. A pipeline
  that runs in a fork of a private project cannot fetch it: with that rule
  set the branch check fails there, and without the rule the branch name is
  checked as usual.
- In a merged results pipeline, `HEAD` is a merge commit GitLab made. The
  checks stop at the merge request's own last commit.
- `rules` keeps the job to merge request pipelines. In any other pipeline the
  command checks the branch and the last commit only, and says so.
- The `python` image ships with git. A `-slim` image does not, and needs it
  installed first.

### Options

Each check has an option, named after the
[Action's input](github-actions.md#inputs) and on or off by default as it is
there:

| Option | Default | What it checks |
|---|---|---|
| `--message` | on | The message of every commit the request adds. |
| `--branch` | on | The name of the source branch, and `require_rebase_target` if it is set. |
| `--author-name` | off | The author name of every commit. |
| `--author-email` | off | The author email of every commit. |
| `--files` | off | The files every commit changes, against the [`[files]` rules](../rules.md#push-rules). |
| `--pr-title` | off | The title, with the message rules a one-line title can meet. |
| `--pr-body-ai-attribution` | off | The description, against the AI attribution rules. |

An option alone switches its check on, and `=false` switches one off:

```yaml
    - commit-check-ci --author-email --branch=false
```

### Making a failed check block the merge

Two things decide whether a failed check stops the merge request:

- **Pipelines must succeed** (Settings > Merge requests > Merge checks) is
  what makes a failed pipeline block the merge. Without it GitLab shows the
  failure and still lets the request merge.
- **Your other jobs have to run in the merge request pipeline too.** Jobs
  with no `rules` of their own run in branch pipelines only, so GitLab starts
  a second pipeline for each merge request, with the `commit-check` job alone
  in it. That pipeline is the one the merge request shows and the one
  **Pipelines must succeed** looks at: a failed test in the branch pipeline
  no longer blocks the merge. These rules start one pipeline for a merge
  request, and jobs with no `rules` run in it:

    ```yaml
    workflow:
      rules:
        - if: $CI_PIPELINE_SOURCE == "merge_request_event"
        - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS && $CI_PIPELINE_SOURCE == "push"
          when: never
        - if: $CI_COMMIT_BRANCH
        - if: $CI_COMMIT_TAG
    ```

    A job with `rules` of its own that only allow branch pipelines
    (`if: $CI_COMMIT_BRANCH`, for example) stays out of the merge request
    pipeline until its rules allow `merge_request_event` too. If your jobs
    already run in merge request pipelines, there is nothing to change.

### Merge request title and description

GitLab passes both to the job, so two options are all it takes:

```yaml
    - commit-check-ci --pr-title --pr-body-ai-attribution
```

- `--pr-title` checks the title with the message rules a one-line title can
  meet: everything `--message` runs except a body (CC011), a sign-off (CC012)
  and an AI author (CC017). With squash merges the title is often the commit
  message that lands. A draft marker (`Draft:`, `[Draft]`, `(Draft)`) is not
  part of the title that is checked.
- `--pr-body-ai-attribution` checks the description against your
  `ai_attribution` policy, and, when `[pull_request] ai_declaration_checkboxes`
  is set, that it ticks exactly one AI declaration box (CC501). GitLab task
  lists (`- [x]`, `* [x]`, `1. [x]`) are read like GitHub's.
- GitLab passes a job only the first 2700 characters of a description, so
  only that part is checked, and the job says so when it happens. Put the AI
  declaration boxes near the top of the merge request template, so a long
  description does not cut them off. To fail a description that was cut
  rather than check part of it, add before the `commit-check-ci` line:

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
            - commit-check-ci
```

- `depth: full` gives the step the pull request's whole history. With a clone
  that ends inside the pull request the step fails and names this setting,
  rather than pass with commits unchecked.
- Bitbucket merges the destination branch into the pull request before the
  step runs. The checks stop at `BITBUCKET_COMMIT`, the pull request's own
  last commit, so commits that only came in with that merge are not checked.
  The rebase check judges that commit too, not the merge.
- The output and the [options](#options) are the same as on GitLab.

### Pull request title and description

Bitbucket gives the step the pull request's id but not its title or
description, so the command reads them from the Bitbucket API. Create a
[repository access token](https://support.atlassian.com/bitbucket-cloud/docs/repository-access-tokens/)
with the **Pull requests: Read** scope, store it as a secured repository
variable named `BITBUCKET_ACCESS_TOKEN`, and switch the two checks on:

```yaml
            - commit-check-ci --pr-title --pr-body-ai-attribution
```

Without the variable, or with a token Bitbucket refuses, the two checks fail
and say why: a title that could not be read is never checked as empty text.
`--pr-title` and `--pr-body-ai-attribution` work as in the
[GitLab section](#merge-request-title-and-description). Editing a pull
request does not start a pipeline, so run the step again after an edit.

## Azure Pipelines

`commit-check-ci` knows GitLab's and Bitbucket's variables. Anywhere else it
checks the branch and the last commit only, so on Azure Pipelines, or a CI of
your own, the job calls `commit-check` itself. Commit Check is a Python
package with no runtime dependencies: any runner that can `pip install` can
run it.

Two things are different from running it on your own machine, and the
example below handles both:

- **The checkout can be a detached HEAD**, as it is on Azure, and then git
  has no branch to report. `commit-check --branch` reads the name from the
  CI's own variables instead, the pull request's source branch first, so the
  job calls it as is.
- **A pull request has more than one commit.** `--rev` checks one commit, so
  the job loops over the commits the pull request adds, as in
  [Checking a range of commits](../example.md#checking-a-range-of-commits).
  The loop needs the history those commits sit on, so the example turns
  shallow cloning off. If the range cannot be read, the job fails rather than
  passing with nothing checked.

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
- Add `--author-name --author-email` to the `commit-check` call in the loop
  to check each commit's author as well, and `--files` to check the files
  each commit adds (configured in the `[files]` section).
- The branch check also covers `require_rebase_target` (CC202), which needs
  the target branch in the clone as `origin/<branch>`. Without it the rule
  reports itself as skipped (`rebase target 'main' not found`) and the job
  passes.

!!! note "On 2.18.2 or older"

    Releases before 2.18.3 read only GitHub's variables, so on a detached
    checkout `--branch` judges `HEAD`, which is always allowed, and passes
    whatever the branch is called. Pipe the name in instead: a value piped
    into `--branch` on its own is the name it checks.

    ```console
    $ echo "${SYSTEM_PULLREQUEST_SOURCEBRANCH#refs/heads/}" | commit-check --branch
    ```
