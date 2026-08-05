# Troubleshooting

## How to Skip Author Name Check

In some cases, Commit Check may fail due to an invalid `author_name`, as shown below:

```shell
check committer name.....................................................Failed
- hook id: check-author-name
- exit code: 1

Commit rejected by Commit-Check.

CC101 author-name check failed ==> 12
The committer name seems invalid
Suggest: git config user.name 'Your Name'
Docs: https://commit-check.com/rules/#cc101
```

To fix it, you can either update your Git config or temporarily skip the check using one of the following methods.

### Bypass All Hooks

Use the `--no-verify` flag to skip the pre-commit hook:

```shell
# Amend the commit without running hooks
git commit --amend --author="Xianpeng Shen <xianpeng.shen@gmail.com>" --no-edit --no-verify
```

### Bypass A Specific Hook

Alternatively, use the `SKIP=your-hook-name` environment variable, like below:

```shell
# Set the correct Git author name
git config user.name "Xianpeng Shen"

# Force amend while skipping the specified hook
SKIP=check-author-name git commit --amend --author="Xianpeng Shen <xianpeng.shen@gmail.com>" --no-edit
```
