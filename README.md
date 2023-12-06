# Minimal-Whitelister

Pretty barebones, but functional discord bot to whitelist members of a discord server into a Pterodactyl-based Minecraft instance.

## Features

- Centralized Database: Checks the user's commands to always only have one whitelisted nick per Discord user.
- Automatic Role: Gives the user a certain role in the Discord server to distinguish who has been whitelisted.
- User Nicks: Set the member's nick to their Minecraft one that's been set by them.

## Setup

1. Clone the repository. `git clone https://github.com/pgiuli/minimal-whitelister`
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Set up your environment variables in a `.env` file following the `skeleton.env`
4. Run `python main.py` to start the bot.

## Commands

- `/ping`: Checks if the bot is running.
- `/whitelist <username>`: Adds a user to the Minecraft server whitelist.
- `/unwhitelist <username>`: Removes a user from the Minecraft server whitelist.

## Contributing

Please open an issue to discuss potential changes/additions.

## Setting up with a Python Virtual Environment (venv)

1. Make sure you have Python virtual environments installed on your system. Run `pip install venv`
2. Create a virtual environment. `python3 -m venv bot-env`
3. Activate the environment on your terminal. `source bot-env/bin/activate` (You can leave this environment running `deactivate` on your shell.)
4. Install the packages. `pip install -r requirements.txt`
5. Set up your environment variables in a `.env` file following the `skeleton.env`
6. Run `python main.py` to start the bot.