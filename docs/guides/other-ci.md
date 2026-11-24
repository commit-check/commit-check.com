# GitLab CI, Bitbucket and Azure Pipelines

On GitHub, the [Action](github-actions.md) and the [App](github-app.md) check
every pull request for you. On GitLab CI and Bitbucket Pipelines one command
does that job: `commit-check-ci`, which comes with the package from 2.23.0
on. It finds the merge or pull request from the variables the CI system sets
and checks the source branch and every commit the request adds, against the
same `cchk.toml` as the hook and the Action. The title, the description, each
commit's author and the files it changes are one option away. On GitLab the
[Commit Check component](https://gitlab.com/explore/catalog/commit-check/commit-check)
in the CI/CD Catalog adds the job for you, and on Bitbucket the
[Commit Check pipe](https://bitbucket.org/commit-check/commit-check) runs it
in a step.

On Azure Pipelines, and on any other CI, the job is
[written by hand](#azure-pipelines).

## GitLab CI

```yaml title=".gitlab-ci.yml"
include:
  - component: gitlab.com/commit-check/commit-check/commit-check@2
```

The component adds one job, `commit-check`, to merge request pipelines. It
installs the latest commit-check 2.x from PyPI and runs `commit-check-ci`.
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

- The job clones the full history (`GIT_DEPTH: "0"`), for this job only. It
  needs every commit of the merge request and the commit they start from.
- The job fetches the target branch itself, which `require_rebase_target`
  ([CC202](../rules.md#cc202)) compares with. For a merge request from a fork
  it fetches from the target project. A pipeline that runs in a fork of a
  private project cannot fetch it: with that rule set the branch check fails
  there, and without the rule the branch name is checked as usual.
- In a merged results pipeline, `HEAD` is a merge commit GitLab made. The
  checks stop at the merge request's own last commit.
- `@2` follows the latest 2.x release of the component. To stay on one
  release, write it out: `@2.0.0`.

### Inputs

Each check has an input, named after the
[Action's input](github-actions.md#inputs) and on or off by default as it is
there:

| Input | Default | What it checks |
|---|---|---|
| `message` | `true` | The message of every commit the request adds. |
| `branch` | `true` | The name of the source branch, and `require_rebase_target` if it is set. |
| `author-name` | `false` | The author name of every commit. |
| `author-email` | `false` | The author email of every commit. |
| `files` | `false` | The files every commit changes, against the [`[files]` rules](../rules.md#push-rules). |
| `pr-title` | `false` | The title, with the message rules a one-line title can meet. |
| `pr-body-ai-attribution` | `false` | The description, against the AI attribution rules. |

```yaml
include:
  - component: gitlab.com/commit-check/commit-check/commit-check@2
    inputs:
      author-email: true
      branch: false
```

Four more inputs shape the job itself:

| Input | Default | What it does |
|---|---|---|
| `version` | `2.*` | The commit-check release to install: `2.*` for the latest 2.x, or an exact one such as `2.24.1`. |
| `image` | `python:3.13` | The image the job runs in. It needs Python 3.11 or newer with pip, and git, which `-slim` and `-alpine` images do not have. |
| `stage` | `test` | The stage the job runs in. |
| `job-name` | `commit-check` | The name of the job. |

### Writing the job yourself

A self-managed GitLab cannot include a component from gitlab.com. There, or
to call the command your own way, write the job out:

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

Each check input above is an option of `commit-check-ci` with the same name.
An option alone switches its check on, and `=false` switches one off:

```yaml
    - commit-check-ci --author-email --branch=false
```

With a clone that ends inside the merge request the job fails and names
`GIT_DEPTH`, rather than pass with commits unchecked. In a pipeline that is
not for a merge request the command checks the branch and the last commit
only, and says so.

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

GitLab passes both to the job, so two inputs are all it takes:

```yaml
include:
  - component: gitlab.com/commit-check/commit-check/commit-check@2
    inputs:
      pr-title: true
      pr-body-ai-attribution: true
```

In a job written by hand they are `--pr-title` and `--pr-body-ai-attribution`.

- `pr-title` checks the title with the message rules a one-line title can
  meet: everything `message` runs except a body (CC011), a sign-off (CC012)
  and an AI author (CC017). With squash merges the title is often the commit
  message that lands. A draft marker (`Draft:`, `[Draft]`, `(Draft)`) is not
  part of the title that is checked.
- `pr-body-ai-attribution` checks the description against your
  `ai_attribution` policy, and, when `[pull_request] ai_declaration_checkboxes`
  is set, that it ticks exactly one AI declaration box (CC501). GitLab task
  lists (`- [x]`, `* [x]`, `1. [x]`) are read like GitHub's.
- GitLab passes a job only the first 2700 characters of a description, so
  only that part is checked, and the job says so when it happens. Put the AI
  declaration boxes near the top of the merge request template, so a long
  description does not cut them off. To fail a description that was cut
  rather than check part of it, give the job a `before_script`. A job of the
  same name in your `.gitlab-ci.yml` is merged with the component's:

    ```yaml
    commit-check:
      before_script:
        - test "$CI_MERGE_REQUEST_DESCRIPTION_IS_TRUNCATED" != "true" || { echo "The description is over 2700 characters; GitLab passed only part of it"; exit 1; }
    ```

- Editing the title or description does not start a pipeline. Run the
  pipeline again from the merge request's **Pipelines** tab after an edit.

## Bitbucket Pipelines

```yaml title="bitbucket-pipelines.yml"
pipelines:
  pull-requests:
    '**':
      - step:
          name: Commit Check
          clone:
            depth: full
          script:
            - pipe: commit-check/commit-check:2.24.2
```

The pipe runs `commit-check-ci` from the commit-check release of the same
version, in an image of its own, so the step needs no `image` and no
install. Its output is the same as on GitLab.

- `depth: full` gives the step the pull request's whole history. With a clone
  that ends inside the pull request the step fails and names this setting,
  rather than pass with commits unchecked.
- Bitbucket merges the destination branch into the pull request before the
  step runs. The checks stop at `BITBUCKET_COMMIT`, the pull request's own
  last commit, so commits that only came in with that merge are not checked.
  The rebase check judges that commit too, not the merge.
- Outside a pull request pipeline, such as a `branches` pipeline, the pipe
  checks the branch and the last commit only.

Each check is a variable, with the same defaults as the
[component's inputs](#gitlab-ci):

| Variable | Default | What it checks |
|---|---|---|
| `MESSAGE` | `true` | The message of every commit the pull request adds. |
| `BRANCH` | `true` | The name of the source branch, and `require_rebase_target` if it is set. |
| `AUTHOR_NAME` | `false` | The author name of every commit. |
| `AUTHOR_EMAIL` | `false` | The author email of every commit. |
| `FILES` | `false` | The files every commit changes, against the [`[files]` rules](../rules.md#push-rules). |
| `PR_TITLE` | `false` | The title, with the message rules a one-line title can meet. |
| `PR_BODY_AI_ATTRIBUTION` | `false` | The description, against the AI attribution rules. |

```yaml
            - pipe: commit-check/commit-check:2.24.2
              variables:
                AUTHOR_EMAIL: 'true'
                BRANCH: 'false'
```

A setting from `cchk.toml` can come from a `CCHK_` variable in the same
place, such as `CCHK_SUBJECT_MAX_LENGTH: '72'`.

### Writing the step yourself

To pick the image or call the command your own way, install commit-check in
the step:

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

The variables above are options of `commit-check-ci`, as in a
[GitLab job written by hand](#writing-the-job-yourself): `AUTHOR_EMAIL: 'true'`
is `--author-email`.

### Pull request title and description

Bitbucket gives the step the pull request's id but not its title or
description, so the pipe reads them from the Bitbucket API. Create a
[repository access token](https://support.atlassian.com/bitbucket-cloud/docs/repository-access-tokens/)
with the **Pull requests: Read** scope, store it as a secured repository
variable named `BITBUCKET_ACCESS_TOKEN`, and switch the two checks on:

```yaml
            - pipe: commit-check/commit-check:2.24.2
              variables:
                PR_TITLE: 'true'
                PR_BODY_AI_ATTRIBUTION: 'true'
                BITBUCKET_ACCESS_TOKEN: $BITBUCKET_ACCESS_TOKEN
```

In a step written by hand they are `commit-check-ci --pr-title
--pr-body-ai-attribution`, and the variable reaches the command without
being named.

Without the token, or with one Bitbucket refuses, the two checks fail
and say why: a title that could not be read is never checked as empty text.
The two checks work as in the
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
