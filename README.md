# RL-project

## How to link this GitHub to VSCode
1. Install Git, guide here: [Git Install](https://git-scm.com/install/)
2. In VSCode, go to `Extensions` or `Ctrl+Shift+X`, and install the extension: **GitHub Pull Requests**
3. In VSCode press the `Accounts` (in the bottom left of the screen) button and press the `Sign in with GitHub...` button
4. Press the `Copy and Continue to Browser`
5. Login to your GitHub account in the Browser
6. Continue
7. Paste your copied code
8. Authorize

## How to clone the repository
1. Open `Command Palette` with `Ctrl+Shift+P`, or from the top menu selecting `View -> Command Palette`
2. Type `Git: Clone`
3. Copy, paste, and enter this GitHub repository's link: **https://github.com/Eiwoh1243/RL-project**
4. Select where you want to save the cloned repository
5. Open the repository folder in VSCode

## How to use the repository
Go to `Source Control` or `Ctrl+Shift+G`

### Creating Branches
1. Press `... -> Branch -> Create Branch...` in the `CHANGES` dropdown menu
2. Enter a name for your branch
3. `Publish Branch` in the `GRAPH` drop-down menu, to publish the branch onto the repo (doesn't commit any changes)

### Switching between Branches
Any changes made to a branch (on your local device) will remain, even if they don't appear once the current working branch is changed to a different one.
1. Press `... -> Checkout to...` in the `CHANGES` dropdown menu
2. Type or Select the branch you want to switch to

### Commiting Changes
Commiting changes is only done on your local device, no changes are made on the repository until you Push the changes.
1. The button that says `Commit`; or open the drop-down menu and press `Commit` (if it isn't the default)
2. Write a message and save with `Ctrl+S`
3. Cancel by not writing any message

### Pushing Changes
1. Open the drop-down menu next to `Commit`, and press `Commit & Push`; or press the `Push` button in the `GRAPH` drop-down menu
2. Write a message and save with `Ctrl+S`

### Pulling from Repository
1. Press the `Pull` button in the `GRAPH` drop-down menu

### Staging
Staged changes are commited when `Commit` is pressed, unstaged changes do not.
1. `Right Click`/`Mouse2` a file, and press `Stage Changes` to stage changes. Or `Right Click`/`Mouse2` the `Changes` drop-down, and press `Stage All Changes` to stage all changes.
2. `Right Click`/`Mouse2` a file, and press `Unstage Changes` to unstage changes. Or `Right Click`/`Mouse2` the `Changes` drop-down, and press `Unstage All Changes` to unstage all changes.
 
### Uncommiting (and Discarding) Changes via Terminal
1. To uncommit all changes: `git reset HEAD~1`
2. To uncommit all changes, and stages them instead: `git reset --soft HEAD~1`
3. To uncommit all changes, and discard them: `git reset --hard HEAD~1`
4. Roll back to older commit, viewed by `git log --oneline` (e.g. `01df11e updating readme file`); using `git reset --hard 01df11e`

## Notice
It is best to have another member review the **Pull Request**, before merging with the **main** branch.

If you are working on the project's directory, but have VSCode opened to a different parent directory (e.g. `/Coursework/RL-project/...` instead of `/RL-project/...`), **DO NOT COMMIT ANY CHANGES** until you have changed your working directory. Doing so will commit all other folders and files in the parent directory to the branch.