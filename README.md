# PyBuddies Discord Bot
This is our discord bot.

It is based on the unoffical API Discord.py.

We have a [Discord server](https://discord.gg/0rIb6L2p8joaD0lC), a [Subreddit](https://reddit.com/r/pybuddies), and a [Trello](https://trello.com/pybuddies) to keep organized and current.

## Getting started on GitHub

The recommended route for you go is to first fork the main repo:

![github-fork-arrow](http://i.imgur.com/9B0qqfF.png)

> Fork is the technical term for make a copy

*****

Next you should copy the `.git` link to your fork of the repo - as shown below - into your clipboard:

![github-fork-clone-url](http://i.imgur.com/X62tRex.png)

*****

Then you open up command prompt or your terminal, change your directory to wherever you want to download your fork of the bot to, and run this command:

`git clone https://github.com/RascalTwo/main_bot.git`

Obviously replace the shown URL with the one in your clipboard.

It will take no more then a few minutes...

```
Cloning into 'main_bot'...
remote: Counting objects: X, done.
remote: Total X (delta 0), pack-reused X
Receiving objects: %100 (X/X), Y KiB | 0 byte/s, done.
Receiving objects: %100 (Z/Z), done.
Checking connectivity... done.
```

*****

After doing that, simply change directory into the `main_bot` folder.

*****

That's It! You have successfully cloned your fork of the bot, and can now install the dependencies, run the bot yourself, and contribute!

## Installing Dependencies

There are many ways to install the dependencies listed above.

You first need to download and install [Python 3.5](https://www.python.org/downloads/release/python-350/).

> You can find your your version of python by running `python --version` in your command prompt/terminal

*****

Fortunatly, `pip` - the python package installer - comes with Python 3.5.

We have the bot setup so you don't have to install each package needed manually, so after cloning the bot onto your system, you can just run this command from the `main_bot` folder.

`pip install -r requirements.txt`

> The command may be `pip3 install -r requirements.txt` for some.

## Running the Bot

The only change you need to make to run the bot is within the `config.py` file. Simply add the email and password of the account the bot should use. You might want to make up a discord account just for the bot if you want to interact with it directly.

After that, just run the `bot.py` file with python and you're done! Your terminal will display the status of the bot, and every command ran by users. You can find your `user_id` that you can add to the `config.py` by running any command.

## Contributing

There are a few ways to contribute.

The recommended way is to make a branch for whatever feature/change you wish to implement, make the actual change, push your branch to your fork of the repo, and make a pull request to the main repo. There are tons of tutorials online that are written better, the only thing that makes this tutorial slightly better is the fact that it is specific to our bot.

So, the steps:

First you must be within the `main_bot` folder of your fork.

Then make sure you're on the master branch with this command:

`git branch -a`

This should return something like this:

```
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
```

The astiesk `*` shows you your current branch. If you're not on the master branch, you should run this command:

`git checkout master`

*****

Now that you're on the `master` branch, you can run this command to create a new branch:

`git branch branch-name`

Now the naming of branch is simple, the first word is what the branch is effecting, so either the name of a cog or simply `bot` would do.

The second word is the new feature and/or change being added.

*****

Now you've made a new branch, you need to change to it - you can go ahead and run `git branch -a` to see it added to the list of branches - by running this command:

`git checkout branch-name`

You can again run `git branch -a` to make sure the new branch you've made is now active.

*****

So now that you're on the new branch, you actually make your changes to existing files, add new files, whatever you wish until you're satisfied and want to have your changes/additions merged into the main repo.

*****

So now you want to `add` the new/changed files to your current branch. You can a list of all new files and changes by running this command:

`git status`

This will return something like this...

```
On branch branch-name
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

    modified:   config.py
    modified:   cogs/__init__.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)

    cogs/new_cog.py
```

Files listed under the `Changes not staged for commit:` section are changed files - this includes deleted and renamed files.

> As `config.py` contains your email and password, you want to ignore this file, NEVER run `git add config.py`, as this will make your email and password public when you push it.

Files listed under the `Untracked files:` section are new files.

So for each file you want to add to the branch, run this command:

`git add path_to/your_file.py`

*****

After doing so, `git status` will look like this...

```
On branch branch-name
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

    modified:   cogs/__init__.py
    new file:   cogs/new_cog.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

    modified:   config.py
```

Once all your files you wish are under the `Changes to be committed:` section, you're now ready to commit!

*****

Commiting is pretty simple. All you do is run this command:

`git commit -m "Commit Message."

Please try your best to describe what you did or what you added within your commit message. If there is no way to keep the commit message short, you
 can add a new line like so:

```
git commit -m "Top commit message, everyone can see me instantly." -m "Second line message, people have to click another time to see me." -m "Oh look, it's a third line!"
```

That's it! You can run `git log` to see your commit as the latest one.

> There are 100s of formats to see the git `graph` in your terminal, the most basic is this:

`git log --oneline --all --graph`

*****

Now you need to get your branch online to your Repo. You can do this by with this simple command:

`git push origin branch-name`

*****

After checking online that the push was made as you like, you can make a pull request to the main Repo by - after switching to the branch you wish - click the `New pull request` button as shown:

!github-new-pull-request](http://i.imgur.com/Eejnjff.png)

After checking that this is indeed the code you want to request to merge into master, create the pull request and you're done! You can now switch back to the Main repo and see your pull request available for discussion.