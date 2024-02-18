# aho

General purpose Discord bot.

## Installation

### Requirements

- python3 (>=3.11.2) with pip
- virtualenv

### Clone and install in virtualenv

- `git clone git@gitlab.com:nul.one/aho.git`
- `cd aho`
- setup and enable virtualenv with correct version of python
- `pip install ./aho`

### Install from pypi

`pip install aho`

__Note that running aho bot will create a socket file in current directory.__

## Usage

- `aho --help` - show available commands
- `aho run --help` - show options for running

You can run the bot with these minimal options:

`aho run -t DISCORD_AUTHORIZATION_TOKEN --database SQLITE_DB_FILE_PATH`

### Additional run options and environment varibles

Each of these variables can be set using corresponding env variable. If both command line option and env variable are present, the command line option will be used.

- `-t, --token` or export `TOKEN` Discord bot authorization token.
- `-o, --owner` or export `OWNER` Bot owner (dev) Discord user ID.
- `--database` Path to sqlite database file. If not provided, it will use ephemeral database in ram.
- `--prefix` or export `DEFAULT_PREFIX` Default prefix in guilds. Each guild prefix can be configured in the guild itself.
- `--description` or export `BOT_DESCRIPTION` Bot description that shows up in guild commands help printout.
- `-n, --name` or export `BOT_NAME` Bot name that shows up in guild commands help printout.
- `--openai` or export `OPENAI_API_KEY` OpenAI API secret key.
- `--openai-system-message` or export `OPENAI_SYSTEM_MESSAGE` Default ChatGPT system message if you want to customize it.
- `-l, --log-file` Log file path.

## Features

These are the features as used from Discord. All of these should start with a bot prefix (default is `aho `) specific for each guild.

### Metadata

Metadata is a list of key/value pairs associated with either a guild, channel, user or member. You can create any key/value pair. Some specific keys are used by other extensions and features. Having an unrestricted key/value pair simplifies configuration of existing features or adding new features in the future.  
  
Here is a list of commands for manipulating metadata:

- `meta (guild|CHANNEL_TAG|MEMBER_TAG) (get|set) KEY [VALUE]` This will get the value of a key for selected entity or set the new value.

The guild as an entity is just a literal word "guild" or "g" for short. There is no tag for a guild. E.g. `meta g set prefix ~`.

If you want to delete a key/value entry, use set command without the value. E.g. `meta g set openai_api_key`.

To list keys/vlues, omit key when getting. E.g. `meta #general get`.

__User meta__

This is separate command to manipulate user specific metadata as opposed to a member. Member is user entity tied to a guild. User metadata is same across all guilds for a specific user. As such, this command is restricted to a bot owner (see `--owner` option in instructions on how to run the bot).

The command is similar to how `meta` works:

- `umeta (MEMBER_TAG|DISCORD_USER_ID) (get|set) KEY [VALUE]`

### Moderation commands

These commands are used for user/channel/guild moderation and are available to users with those specific permissions.

- `ban (MEMEBER_TAG|DISCORD_USER_ID) [REASON]` ban a user.
- `unban (MEMEBER_TAG|DISCORD_USER_ID)` lift a user ban.
- `kick (MEMEBER_TAG|DISCORD_USER_ID) [REASON]` kick a user from guild.
- `perms (MEMEBER_TAG|DISCORD_USER_ID)` display member permissions in guild.
- `clear [N]` delete N lines (defaults to 1) right above in the current channel.

### OpenAI (ChatGPT) chat

There are 2 modes of chatting with ChatGPT bot: using chat command and using a chat specific channel. ChatGPT 3.5 is being used as of the time of writing this manual.

__Chat command__

Guild level metadata values should be configured:

- `openai_api_key` Put your OpenAI API key here. Alternatively, you can specify this value when running the bot with `--openai` option or exporting `OPENAI_API_KEY` environment variable. Note that by doing so the api will be enabled by default on all guilds. I recommend having a specific setting in metadata for each guild if your discord bot is publically available.
- `openai_system_message` This is optional and is used if you want to customize your ChatGPT experience.

Using a `chat` command, e.g. `chat Hello! Can you tell me the radius of Earth?` will initiate a respons from the bot in all channels.

__Chat channel__

You can configure one channel that will always initiate a response from a bot, no commands need to be used in it. To configure a channel for this, set these meta variables at the channel level:

- `openai_chat_enabled` Set it to `1` to start using this channel as dedicated for a chatbot interraction.
- `openai_system_message` Optional, same as for `chat` command. Each dedicated channel can have specific ChatGPT customization.

You still need an `openai_api_key` set at the guild level for this dedicated channel chat to work.

### Points

Members who have permission to manage other members can use the point system. Point system is used to award other members for any deeds or to promote competitive environment. It's up to you on how you will use this feature.

- `transaction (MEMBER_TAG|DISCORD_USER_ID) AMOUNT [DESCRIPTION]` Add (or remove by adding negative AMOUNT) points to a member.

Points can be visible in the member info (see info command).

### Member Info

Use this command to see following information about a member:

- number of points
- guild joining date and joining position
- guild roles
- discord account creation date

Use it as so `info ` If you don't provide a member tag or ID, it will show your own info.

### Roll

Roll dice in NdN format, first number being number of dice and second being number of sides on each die.

- `roll [NdN]` Default is 1d6 which you can use without arguments.

### Emoji

- `addemoji EMOJI NAME` Copy an existing emoji (that you can access from another server with Discord premium) and add it to the current server under a new NAME.
- `getemoji EMOJI` Get a link to the emoji image or animation.

### General purpose commands

- `help [command]` Show usage of specific command. If you don't specify a command, it will list all commands with short description.
- `avatar [MEMBER_TAG|DISCORD_USER_ID]` It will reply with a member avatar image. If you don't provide a member tag or ID, it will show your own avatar.
- `embed "Some Title" Some message.` This will create an embeded message in a current channel and delete your command message. Used to create emphasized messages.
- `info [MEMBER_TAG|DISCORD_USER_ID]` Show member info, including number of points, guild joining date and position, guild roles and discord account creation date. If you don't specify a member, your own info will be shown.
- `prefix NEW_PREFIX` Set new Discord bot prefix at a guild level.
- `version` Display the current bot version.

## Versioning and compatibility

Starting from version `1.3.0` the versions will follow [Semantic versioning v2.0.0](https://semver.org).

## License

[3-Clause BSD License](https://opensource.org/license/bsd-3-clause/) which you can see in the LICENSE file.

