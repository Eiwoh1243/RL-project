# **RL-project**
> Below describes how this project is to be done (I'm writing this on the fly as time goes on).
>>
>> **GitHub & VSCode**
>>
>> Guide regarding linking GitHUb and VSCode, and using/managing the repository mostly through from VSCode.
>
>> **Project Organisation**
>>
>> Guide regarding project organisation/management, similar to using Figma, but just only requires GitHub and VSCode. And should be more easier to use.
>
>> **Basics of Testing**
>>
>> Guide regarding the basic method for testing, that we will be using. It will likely not be too complex or extensive, just enough that errors are easily caught and tracable; for debugging purposes.

<br><br>

# **GitHub & VSCode**

> ## **Note**
> It is best to have another member review the **Pull Request**, before merging with the **main** branch.
>
> Additionally, if you **Want** to be create a pull request, instead of just pushing the code; you **Need** to **Create and Work** within a different branch.

> ## **How to link this GitHub repo to VSCode**
> 1. Install Git, guide here: [Git Install](https://git-scm.com/install/)
> 2. In VSCode, go to `Extensions` or `Ctrl+Shift+X`, and install the extension: **GitHub Pull Requests**
> 3. In VSCode press the `Accounts` (in the bottom left of the screen) button and press the `Sign in with GitHub...` button
> 4. Press the `Copy and Continue to Browser`
> 5. Login to your GitHub account in the Browser
> 6. Continue
> 7. Paste your copied code
> 8. Authorize

> ## **How to Clone the Repository**
> 1. Open `Command Palette` with `Ctrl+Shift+P`, or from the top menu > > selecting `View -> Command Palette`
> 2. Type `Git: Clone`
> 3. Copy, paste, and enter this GitHub repository's link: **https://github.com/Eiwoh1243/RL-project**
> 4. Select where you want to save the cloned repository
> 5. Open the repository folder in VSCode

> ## **How to Use the Repository**
> Go to `Source Control` or `Ctrl+Shift+G`
> 
> ### **Creating Branches**
> 1. Press `... -> Branch -> Create Branch...` in the `CHANGES` dropdown menu
> 2. Enter a name for your branch
> 3. `Publish Branch` in the `GRAPH` drop-down menu, to publish the branch onto the repo (doesn't commit any changes)
> 
> ### **Switching between Branches**
> Any changes made to a branch (on your local device) will remain, even if they don't appear once the current working branch is changed to a different one.
> 1. Press `... -> Checkout to...` in the `CHANGES` dropdown menu
> 2. Type or Select the branch you want to switch to
> 
> ### **Commiting Changes**
> Commiting changes is only done on your local device, no changes are made on the repository until you Push the changes.
> 1. The button that says `Commit`; or open the drop-down menu and press `Commit` (if it isn't the default)
> 2. Write a message and save with `Ctrl+S`
> 3. Cancel by not writing any message
> 
> ### **Pushing Changes**
> 1. Open the drop-down menu next to `Commit`, and press `Commit & Push`; or press the `Push` button in the `GRAPH` drop-down menu
> 2. Write a message and save with `Ctrl+S`
> 
> ### **Pulling from Repository**
> 1. Press the `Pull` button in the `GRAPH` drop-down menu
> 
> ### **Staging**
> Staged changes are commited when `Commit` is pressed, unstaged changes do not.
> 1. `Right Click`/`Mouse2` a file, and press `Stage Changes` to stage changes. Or `Right Click`/`Mouse2` the `Changes` drop-down, and press `Stage All Changes` to stage all changes.
> 2. `Right Click`/`Mouse2` a file, and press `Unstage Changes` to unstage changes. Or `Right Click`/`Mouse2` the `Changes` drop-down, and press `Unstage All Changes` to unstage all changes.
> 
> ### **Uncommiting Changes via Terminal**
> 1. To uncommit all changes: `git reset HEAD~1`
> 2. To uncommit all changes, and stages them instead: `git reset --soft HEAD~1`
> 3. To uncommit all changes, and discard them: `git reset --hard HEAD~1`
> 4. Roll back to older commit, viewed by `git log --oneline` (e.g. `01df11e updating readme file`); using `git reset --hard 01df11e`
> 5. If the commit has been done to the repo, then run `git revert HEAD`, and re-commit; the staged files contain the reverted versions of the commited changes, so commiting them undos the changes
> 
> ### **Discarding Changes**
> 1. `Right Click`/`Mouse2` a file, and press `Discard Changes`. Or `Right Click`/`Mouse2` the `Changes` drop-down, and press `Discard All Changes` to discard all changes.
> 
> ### **Close Repository**
> This is useful so that VSCode doesn't automatically try to detect your personal/parent directory as a repository.
> 1. Ensure `SOURCE CONTROL -> ... -> Repositories` is ticked
> 2. `Right Click`/`Mouse2` the repository that appears, and press `Close Repository`
> 
> ### **VSCode Workspaces**
> As means to having both your personal/parent, and git repo folders present and non-conflicting.
> 1. Do `File -> Add Folder to Workspace...` twice, one for the personal/parent folder, and the other for your git repo folder
> 2. Do `File -> Save Workspace As...`, and save it somewhere reasonable
> 3. Do `File -> Open Workspace from File...`, and select the newly created workspace
> 4. Ensure `RL-project` is selected in the `REPOSITORIES` drop-down menu, in `Source Control`
> 5. Enjoy being able to work with a workspace, that allows you to have both your personal/parent and git repo folder present

> ## **Create a Virtual Environment**
> If you want a indepedent environment to other project in your PC create the virtual enviroment. 
> 1. Put `python -m venv .venv`  in the terminal 
> 2. Activate it by `.\.venv\Scripts\Activate.ps1` in the terminal
> 3. Deactivate iy by `deactivate` in the terminal

<br><br>

# **Project Organisation**

> ## **Note**
> It is usually easier to work within GitHub's provided 'project organisation' feature; primarily between the `Issues` and `Projects` tabs for the repository. The guide will specifically be describing how to use it; if you have experience with doing any of the actions below, solely from VSCode, that is fine.
>
> The sections are separated by **Regular Guide** and **Owner Guide**, just because there are some actions that can only be done by the owner of the repo. If you need something done, that can only be done by the owner, contact them to get that issue sorted.
>
> Yes, this is essentially Figma, Jira, Trello and whatever; but instead of using two websites (GitHub and other), we are using one. Additionally, this guide **Will Not be Extensive**, we do not need some advanced workflow; just suitable enough to stay organised.

> ## **Regular Guide**
> ### **GitHub `Issues` Tab**
> 1. Go to the GitHub repository
> 2. Press the `Issues` tab in the top-menu
> 
> ### **GitHub `Projects` Tab**
> 1. Go to the GitHub repository
> 2. Press the `Projects` tab in the top-menu
> 3. The tab you will currently be at is the `Backlog` tab
> 
> ### **Creating Issues**
> 1. `[Option A]` Press the green `New Issue` button in `Issues`
> 2. `[Option B]` Press the `Add Item` button in `Projects`, within any of the `Backlog` columns
> 3. Add a title, description, and any optional labels
> 4. Press the green `Create` button, or use `Ctrl+Enter`
> 
> ### **Editing Issues**
> 1. Press the name of the issue, in either `Issues` or `Projects`
> 2. Edit the issue's title, description, etc.
> 3. `[Optional]` Add a comment
> 
> ### **`[Optional]` Using `Roadmap`**
> 1. Select the `Roadmap` tab
> 2. Double-click a location on the roadmap, for a given issue, to create a 'time frame'/box for the issue
> 3. Drag the ends of the issue's 'time frame' to extend or reduce the duration; Double-click-and-drag the issue to move the 'time frame' forward of backwards in time.
> 
> ### **Moving Issues**
> 1. `[Option A]` In the issue editory from `Issues`, within the `Projects` section, select the new `Status`/location for the issue using the drop-down menu.
> 2. `[Option B]` In `Projects`, click-and-drag the card of the issue to move, to between the `Status` columns. And or within the `Priority Board` tab, up-and-down between different **Priority** tags

> ## Owner Guide
> ### Creating a Project
> 1. Go to the GitHub repository
> 2. Press the `Projects` tab in the top-menu 
> 3. Press the green `New Project` button
> 4. Select a preset, **Primarilly** the **Kanban** preset
> 
> ### Modify the Project's Settings
> 1. Press the `...` at the top-right
> 2. Press the `Settings` button
> 3. Modify settings regarding `Status`, `Priority`, etc.

<br><br>

# **Basics of Testing**

> ## **Note**
> This guide will assume that we will be developing using Python. This may be workable in other cases, but if it doesn't then it is best to ask the other members, or search online how to get it working.
> 
> It will also not be extensive, again; since like mentioned, this will mostly be used to detect and trace back errors, so that debugging will be easier.
>
> But a **Further Guide** is available in the `/tests/README.md` file, if needed.

> ## Installing `pytest`
> 1. `[Optional]` Activate/Use a virtual environment, where the `pytest` library will be installed; instead system-wide on your device.
> 2. Run `pip install pytest` in the terminal
> 3. Also run `pip install pytest-cov` in the terminal (for creating a coverage report)
> 4. `[Optional]` Verify the installation with `pytest --version`
> 
> ## Basic Usage
> 1. Run `pytest` in the terminal, to run all test code in `/tests`
> 2. This will also run automatically when you commit code
> 3. `[Optional]` To view the HTML coverage report proper, select the `.coverage` file, and press `Go Live` at the bottom-right to start a live server. **Note** you will need to install the VSCode extension that allows this called `Live Server` by `ritwickdey`. Once opened, select the `htmlcov` directory to view the coverage report.