"""
aho bot.
"""
from aho import Config
from aho import Registry
from aho import base
from aho import color
from aho import utils
from aho.database import db, bind_database
from discord.ext import commands
import discord
import traceback

discord_intents = discord.Intents.default()
discord_intents.members = True
discord_intents.message_content = True
help_command = commands.DefaultHelpCommand(
        no_category = 'general'
        )
bot = commands.Bot(
        command_prefix=base.prefix,
        intents=discord_intents,
        help_command = help_command,
        )

base.bot = bot

def run(token):
    bind_database(Config().db_path)
    #orm.set_sql_debug(True)
    db.generate_mapping(create_tables=True)
    bot.description = Config().bot_description
    bot.run(token)

async def message_console_logger(message):
    timestamp = f"{color.blue}{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}{color.end}"
    guild = f"{color.cyan}{message.guild.name if message.guild else ':DC:'}{color.end}"
    channel = f"{color.darkcyan}#{message.channel.name if hasattr(message.channel, 'name') else ':DC:'}{color.end}"
    channel_id = f"{color.darkcyan}{message.channel.id if hasattr(message.channel, 'id') else ''}{color.end}"
    author = f"{color.green}@{message.author.name}{color.end}"
    content = message.content
    print(f"{timestamp} {guild} {channel} {channel_id} {author} {content}")
async def message_file_logger(message):
    timestamp = f"{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    guild = f"{message.guild.name if message.guild else ':DC:'}"
    channel = f"#{message.channel.name if hasattr(message.channel, 'name') else ':DC:'}"
    channel_id = f"{message.channel.id if hasattr(message.channel, 'id') else ''}"
    author = f"@{message.author.name}"
    content = message.content
    log_content = f"{timestamp} {guild} {channel} {channel_id} {author} {content}\n"
    with open(Config().log_file, 'a') as log_file:
        log_file.write(log_content)
Registry().add_processor(message_console_logger)
if Config().log_file:
    Registry().add_processor(message_file_logger)

async def command_processor(message):
    if message.author.bot:
        return
    await bot.process_commands(message)
Registry().add_processor(command_processor)

@bot.event
async def on_message(message):
    for processor in Registry().processors:
        await processor(message)

@bot.event
async def on_member_join(discord_member):
    base.update_user_and_member_meta(discord_member)
    roles_to_restore = base.roles_to_restore(discord_member)
    if roles_to_restore:
        existing_roles_to_restore = list(filter(
            lambda r: r in discord_member.guild.roles, roles_to_restore
            ))
        await discord_member.add_roles(
                *existing_roles_to_restore,
                reason="Restoring roles that user had before leaving guild."
                )
    joiner_role = base.joiner_role(discord_member)
    if joiner_role:
        await discord_member.add_roles(
                joiner_role,
                reason="Applying joiner role."
                )

@bot.event
async def on_member_update(before, after):
    base.update_user_and_member_meta(after)
    base.update_member_roles(after)

@bot.event
async def on_guild_join(discord_guild):
    for member in discord_guild.members:
        base.update_user_and_member_meta(member)
        base.update_member_roles(member)

@bot.event
async def on_command_error(ctx, error):
    lm = utils.LongMessage(ctx, 'error')
    lm.add_line(str(error))
    await lm.reply(ctx.message)
    raise error

@bot.event
async def on_ready():
    from aho import general
    from aho import cog_mod
    from aho import cog_rng
    from aho import cog_google_translate
    from aho import cog_openai_chat
    from aho import cog_emoji
    from aho import cog_points
    import aho.socket as socket
    #from aho import actions
    #from aho import leaderboard
    for cog in Registry().cogs:
        await bot.add_cog(cog(bot))
    print(f'Logged in as {bot.user.name} with id {bot.user.id}')
    await socket.start()
    print(f'Bound to the {Config().socket_file} socket')
    print('------')


