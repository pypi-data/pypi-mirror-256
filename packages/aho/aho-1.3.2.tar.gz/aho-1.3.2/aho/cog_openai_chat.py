"""
openai chat - message processor.
"""
from aho import Config
from aho import Registry
from aho import base
from aho.database import get_or_create
from discord.ext import commands
from openai import OpenAI
from pony import orm
import json

default_system_message = (Config().openai_system_message or "").format(bot_name=Config().bot_name)
base.guild_meta_defaults["openai_message_log_length"] = "10"
#base.guild_meta_defaults["openai_api_key"] = None
base.guild_meta_defaults["openai_system_message"] = default_system_message
base.channel_meta_defaults["openai_message_log_length"] = "20"
base.channel_meta_defaults["openai_system_message"] = default_system_message + " You will see a username as a first line of every user post for each user."
base.channel_meta_defaults["openai_chat_enabled"] = "0"

@orm.db_session
def get_member_chat_details(ctx):
    """Return tuple: openai_api_key, openai_system_message, message_log, log_length"""
    if not ctx.message.guild:
        return None, None, None, None
    if not ctx.message.author:
        return None, None, None, None
    user = get_or_create(base.User, id=ctx.message.author.id)
    guild = get_or_create(base.Guild, id=ctx.guild.id)
    member = get_or_create(base.Member, user=user, guild=guild)
    key = guild.meta.get("openai_api_key", Config().openai_api_key)
    system = guild.meta.get("openai_system_message", Config().openai_system_message)
    log = json.loads(member.meta.get("openai_message_log", "[]"))
    log_length = int(guild.meta.get("openai_message_log_length"))
    return key, system, log, log_length

@orm.db_session
def save_member_message_log(ctx, message_log):
    user = get_or_create(base.User, id=ctx.message.author.id)
    guild = get_or_create(base.Guild, id=ctx.guild.id)
    member = get_or_create(base.Member, user=user, guild=guild)
    meta = member.meta
    meta["openai_message_log"] = json.dumps(message_log)
    member.meta = meta

@orm.db_session
def get_channel_chat_details(message):
    """Return tuple: openai_api_key, openai_system_message, message_log, log_length"""
    if not message.channel:
        return None, None, None, None
    guild = get_or_create(base.Guild, id=message.guild.id)
    key = guild.meta.get("openai_api_key", Config().openai_api_key)
    if not key:
        return None, None, None, None
    channel = get_or_create(base.Channel, id=message.channel.id)
    if channel.meta.get("openai_chat_enabled", None) != "1":
        return None, None, None, None
    system = channel.meta.get("openai_system_message",  Config().openai_system_message)
    log = json.loads(channel.meta.get("openai_message_log", "[]"))
    log_length = int(channel.meta.get("openai_message_log_length"))
    return key, system, log, log_length

@orm.db_session
def save_channel_message_log(message, message_log):
    channel = get_or_create(base.Channel, id=message.channel.id)
    meta = channel.meta
    meta["openai_message_log"] = json.dumps(message_log)
    channel.meta = meta

def openai_chat_completion(api_key, message, message_log, log_length, system_message = None):
    client = OpenAI(api_key=api_key)
    if not client:
        raise Exception("Failed to register OpenAI client.")
    messages = []
    if system_message.strip() != "":
        messages = [{"role": "system", "content": system_message}]
    message_log.append({"role": "user","content": message})
    message_log = message_log[-log_length:]
    messages.extend(message_log)
    if Config().debug:
        print(messages)
    response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            max_tokens=3800,
            stop=None,
            temperature=0.9,
        ).choices[0].message.content
    message_log.append({"role": "assistant","content": response})
    message_log = message_log[-log_length:]
    return message_log
 
class OpenAICog(commands.Cog, name="openai"):
    """OpenAI chat bot commands."""

    @commands.command()
    async def chat(self, ctx, *, message: str = commands.parameter(description="Message body.")):
        '''Talk to bot.
        Usage: chat Some message.
        Meta variables:
            guild:
            - openai_api_key
            - openai_system_message
            - openai_message_log_length
            member:
            - openai_message_log
        '''
        api_key, system_message, message_log, log_length = get_member_chat_details(ctx)
        if not api_key:
            raise ValueError("openai_api_key is not set in the guild metadata")
        new_message_log = openai_chat_completion(api_key, message, message_log, log_length, system_message)
        await ctx.message.reply(new_message_log[-1]["content"])
        save_member_message_log(ctx, new_message_log)

Registry().add_cog(OpenAICog)


async def openai_chat(message):
    if message.author.bot:
        return
    if not message.content:
        return
    if message.content.startswith(base.get_prefix(message)):
        return
    api_key, system_message, message_log, log_length = get_channel_chat_details(message)
    if not api_key:
        return
    user_name = message.author.nick or message.author.display_name or message.author.name
    content = f"{user_name}\n{message.content}"
    new_message_log = openai_chat_completion(api_key, content, message_log, log_length, system_message)
    await message.reply(new_message_log[-1]["content"])
    save_channel_message_log(message, new_message_log)

Registry().add_processor(openai_chat)

