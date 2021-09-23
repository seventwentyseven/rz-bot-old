# What is rz bot
RZ bot or with original name thats unwrittable in repo name "Ż bot", is a bot for managing osu servers on gulag. Right now there's not too much in the code because im rewriting it for 727th time. I want it to be usable on every osu server made on gulag.

You can see our trello board here: https://trello.com/b/sZORcdeI/rz-bot

# Requirements
Bot has been tested on both windows and Ubuntu 18.04.
So here are things that you need:

- tzdata python package (If running on windows)
- sendgrid (If you're going to use this module, you'll also need sendgrid api key, you can get it [here](https://sendgrid.com). If you dont plan using our mailing module, disable it in config.
- Also make sure that your terminal supports colors or it will look extremelly bad. Example that supports it: Windows Terminal from Microsoft Store

# Working with code
I strongly recommend using BeterComments extension for VS Code, idk if it exists for other editors too.
Also as MIT license says, you can resell it, edit it anything you want. Just leave information that we created it, or at least the base. Be a nice person. Thanks :)

# Installation
I'm too lazy to write down every command here so just in short
```
Clone repo
download python3.9
execute python3.9 -m pip install -r ext/requirements.txt
import table in ext folder named discord.sql
implement patch located at ext/verificationpatch.md, how to do it? It's explained in this file.
copy ext/config.sample.py to base folder and rename it to config.py
run bot with python3.9 main.py
```
