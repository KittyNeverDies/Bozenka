<div align="center">

<img src="images/header.png">

[![CodeFactor](https://www.codefactor.io/repository/github/kittyneverdies/bozenka/badge)](https://www.codefactor.io/repository/github/kittyneverdies/bozenka)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![Issues](https://img.shields.io/github/issues-raw/tterb/PlayMusic.svg?maxAge=25000)](https://github.com/kittyneverdies/bozenka/issues)  

[Telegram Channel](https://t.me/bozodevelopment/) | [Website](kittyneverdies.github.io/BozenkaWeb/)


</div>


### Current progress of development

<details><summary>Telegram Instance</summary>

List of features in Telegram instance working right now

- [ ] Group
  - [ ] Administration
    - [x] Ban & Unban commands
    - [x] Mute & Unmute commands
    - [x] Pin & Unpin & Unpin all commands
    - [ ] Bad words & Spam filter
    - [x] Setup command 
    - [x] Welcome message to administrators after adding bot to chat.
    - [x] Work with inline keyboard
  - [x] Work with telegram topics
    - [x] Close & Open Topics
    - [x] Hide general topic
    - [x] Rename topics
    - [x] Work with inline keyboard
  - [x] Users
    - [x] Show information about chat (/info)
    - [x] Welcome messages
    - [x] Generating invites
    - [x] Start command menu (/start)
- [ ] Fun
  - [ ] GPT / LLM / AI generation
    - [x] Libraries 
      - [x] Gpt4All
        - [ ] Memory based support information, does this model can be launched on server
      - [x] Gpt4Free
        - [x] Select Providers & Models
        - [x] Select Models only
        - [ ] Image generation
      - [ ] PyTorch / Diffusers / TenserFlow
        - [ ] Work with custom models
    - [ ] UI
      - [x] Inline keyboard support
      - [ ] Using tutorial.
      - [ ] Regenerate and complete text
      - [ ] Inline image generation
    - [x] Threads and Topic of dialog support (Already by new aiogram)
- [x] Code
  - [x] Logging support
  - [x] Features descriptions
  - [x] Custom Filters
  - [x] Middlewares
  - [x] Database

### This part of project made with

-  [Aiogram python library](https://github.com/aiogram/aiogram) and with their community support.
-  [GPT4Free](https://github.com/xtekky/gpt4free), [Gpt4All](https://github.com/nomic-ai/gpt4all), [SqlAlchemy](https://github.com/sqlalchemy/sqlalchemy/) python libraries
- With our love & your support <3
</details>


### Positive / Negative things in the project?

**Positive:** 
- The project is open source and licensed under the GPL-V3, you can influence the development of this project by creating pull requests and issues.
- The whole project is structured by folders, classes, the code has a large number of comments for community
- The database is PostgreSQL + SQLAlchemy, when writing data to two users at the same time, nothing is lost, everything is asynchronous

**Negative**:
- The code needs major fixes and improvements; bugs are not excluded. The project is still under development.
- GPT4All and other neural network libraries in the future will require powerful hardware (RAM of at least 16 GB) is one of the reasons why there won't be an official version running both. You need to run the bot yourself, and preferably on a server.
- No offical public launched instance of bozenka on platforms

### Any public launched instances?
No, at least not for now. There will be only beta tests, in which the bot will run on a server for one to two weeks. \
You are need to launch it by yourself.

### Installation
Bozenka was created using python, please, be sure you have installed it in your system with pip.

1. Install all requirements for bozenka by writing this command: `pip install requirements.txt`
2. Create PostgeSQL database, write all you enter information
3. Create enviroment this enviroment variables:
    - `tg_bot_token` - your telegram bot token
    - `kadinsky_api` - api of kadinsky & `kadinsky_secret` - api secret of kadinsky
    - `db_host`, `db_name`, `db_password`, `db_port`, `db_username`, all of this for PostgreSQL database
4. Create all rows by alembic:
   - Create revision: `alembic revision --n="Bozenka main migration" --autogenerate`
   - Upgrade your database: `alembic upgrade head`
5. Launch `run.py` file, it should launch bozenka on your machine.
