'''
aho base classes and meta data.
'''
from aho import Config
from aho import Registry
from aho import utils
from aho.database import db, get_or_create
from discord.ext import commands
from pony import orm
import discord
import json
import typing

bot = None # will be set from bot module after import

user_meta_defaults = {
    "_seen_user_names": [],
    "_seen_display_names": [],
    }
class User(db.Entity):
    id = orm.PrimaryKey(int, size=64, auto=False)
    memberships = orm.Set("Member", reverse='user')
    _meta = orm.Required(str, default='{}')

    @property
    def meta(self):
        d = json.loads(self._meta)
        for x in user_meta_defaults:
            d.setdefault(x, user_meta_defaults[x])
        return d

    @meta.setter
    def meta(self, meta):
        self._meta= json.dumps(meta)

    async def get_object(self):
        return await bot.fetch_user(self.id)

guild_meta_defaults = {
    "keep_roles": "0",
    "joiner_role": None,
    }
class Guild(db.Entity):
    id = orm.PrimaryKey(int, size=64, auto=False)
    prefix = orm.Required(str, default=Config().default_prefix, autostrip=False)
    members = orm.Set("Member", reverse='guild')
    _meta = orm.Required(str, default='{}')

    @property
    def meta(self):
        d = json.loads(self._meta)
        for x in guild_meta_defaults:
            d.setdefault(x, guild_meta_defaults[x])
        return d

    @meta.setter
    def meta(self, meta):
        self._meta= json.dumps(meta)

    async def get_object(self):
        return await bot.fetch_guild(self.id)

channel_meta_defaults = {
    }
class Channel(db.Entity):
    id = orm.PrimaryKey(int, size=64, auto=False)
    _meta = orm.Required(str, default='{}')

    @property
    def meta(self):
        d = json.loads(self._meta)
        for x in channel_meta_defaults:
            d.setdefault(x, channel_meta_defaults[x])
        return d

    @meta.setter
    def meta(self, meta):
        self._meta= json.dumps(meta)

    async def get_object(self):
        return await bot.fetch_channel(self.id)

member_meta_defaults = {
    "_seen_nick_names": [],
    }
class Member(db.Entity):
    user = orm.Required(User, reverse='memberships')
    guild = orm.Required(Guild, reverse='members')
    orm.composite_key(user, guild)
    points = orm.Required(int, default=0)
    _meta = orm.Required(str, default='{}')
    _roles = orm.Required(str, default='[]')

    @property
    def meta(self):
        d = json.loads(self._meta)
        for x in member_meta_defaults:
            d.setdefault(x, member_meta_defaults[x])
        return d

    @meta.setter
    def meta(self, meta):
        self._meta= json.dumps(meta)

    @property
    def roles(self):
        roles_tuple = tuple(json.loads(self._roles))
        return roles_tuple

    @roles.setter
    def roles(self, roles_tuple):
        self._roles = json.dumps(roles_tuple)

    async def get_object(self):
        discord_guild = await bot.fetch_guild(self.guild.id)
        return await discord_guild.fetch_member(self.user.id)

@orm.db_session
def update_member_roles(guild_member):
    member = get_or_create(Member,
            user=get_or_create(User, id=guild_member.id),
            guild=get_or_create(Guild, id=guild_member.guild.id)
            )
    member.roles = tuple(map(lambda r: r.mention, guild_member.roles[1:]))

@orm.db_session
def update_user_and_member_meta(guild_member):
    user = get_or_create(User, id=guild_member.id)
    guild = get_or_create(Guild, id=guild_member.guild.id)
    member = get_or_create(Member, user=user, guild=guild)
    member_meta = member.meta
    nick_name = guild_member.nick
    if nick_name not in member_meta["_seen_nick_names"]:
        member_meta["_seen_nick_names"].append(nick_name)
    member.meta = member_meta
    user_meta = user.meta
    user_name = f"{guild_member.name}#{guild_member.discriminator}"
    display_name = guild_member.display_name
    if user_name not in user_meta["_seen_user_names"]:
        user_meta["_seen_user_names"].append(user_name)
    if display_name not in user_meta["_seen_display_names"]:
        user_meta["_seen_display_names"].append(display_name)
    user.meta = user_meta

@orm.db_session
def roles_to_restore(guild_member):
    guild=get_or_create(Guild, id=guild_member.guild.id)
    if not int(guild.meta.get('keep_roles', "0")):
        return
    user=get_or_create(User, id=guild_member.id)
    member = get_or_create(Member, user=user, guild=guild)
    roles_to_restore = []
    for role in member.roles:
        for guild_role in guild_member.guild.roles:
            if role == guild_role.mention:
                roles_to_restore.append(guild_role)
    return roles_to_restore

@orm.db_session
def joiner_role(guild_member):
    guild = get_guild(guild_member.guild.id)
    joiner_role = guild.meta.get('joiner_role', None)
    if joiner_role:
        for role in guild_member.guild.roles:
            if role.mention == joiner_role:
                return role

@orm.db_session
def prefix(bot, message): # used only when creating bot
    if not message.guild:
        return Config().default_prefix
    guild = get_or_create(Guild, id=message.guild.id)
    return guild.prefix

@orm.db_session
def get_prefix(message): # used in message processors to avoid processing commands
    if not message.guild:
        return Config().default_prefix
    guild = get_or_create(Guild, id=message.guild.id)
    return guild.prefix

@orm.db_session
def get_guild(guild_id):
    guild = Guild.get(id=guild_id)
    return guild

@orm.db_session
def get_channel(channel_id):
    channel = Channel.get(id=channel_id)
    return channel

@orm.db_session
def get_member_by_ids(user_id, guild_id):
    user = User.get(id=user_id)
    guild = Guild.get(id=guild_id)
    if not user or not guild:
        return
    member = Member.get(
            user=user,
            guild=guild
            )
    return member

@orm.db_session
def get_guild_id_name_list():
    guild_id_list = [id for id in orm.select(e.id for e in Guild)]
    guild_id_name_list = []
    for gid in guild_id_list:
        guild = bot.get_guild(gid)
        guild_id_name_list.append([gid,guild.name])
    return guild_id_name_list

def get_channel_id_name_type_list(guild_id):
    guild = bot.get_guild(int(guild_id))
    channel_id_name_type_list = []
    if guild:
        for c in guild.channels:
            channel_id_name_type_list.append([c.id, c.name, c.type])
    return channel_id_name_type_list

def get_member_id_name_nick_list(guild_id):
    guild = bot.get_guild(int(guild_id))
    member_id_name_nick_list = []
    if guild:
        for m in guild.members:
            member_id_name_nick_list.append([m.id, m.name + (f"#{m.discriminator}" if m.discriminator != "0" else ""), m.nick])
    return member_id_name_nick_list

@orm.db_session
def get_channel_list(guild_id):
    return [g.mame for g in Guild.select()]

def data_limiter(data: str, length: int = 100):
    str_data = json.dumps(data)
    if len(str_data) > length:
        return "[...]" + str_data[-length:]
    return str_data

class Metadata(commands.Cog, name="metadata"):
    """View or update meta data."""

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def meta(self, ctx,
            entity: typing.Union[discord.TextChannel, discord.Member, str] = commands.parameter(description="guild|CHANNEL|USER"),
            action: str = commands.parameter(description="get|set", default="get"),
            variable: str = commands.parameter(description="Variable name.", default=None),
            value: str = commands.parameter(description="New value for variable. Leave empty to delete or reset to default.", default=None)
            ):
        '''Display or update meta data for an entity.
        Usage: meta ENTITY get|set VARIABLE [VALUE]
        '''
        if Config().debug:
            print(locals())
        if action not in ("get", "set"):
            raise ValueError(f"Need to use 'get' or 'set' action. Provided: {str(action)}")
        local_entity = self.meta_get_local_entity(ctx, entity)
        meta = local_entity.meta
        
        if action == "get":
            embed = utils.make_embed(msg_type="info")
            if variable is None:
                # show all meta
                embed.title = f"{(await local_entity.get_object()).name} meta"
                meta_list = ""
                for key in sorted(meta):
                    meta_list += f"{key}: {data_limiter(meta[key])}\n"
                embed.add_field(name="Variables", value=f"{meta_list}")
                return await ctx.send(embed=embed)
            else:
                # show one value
                embed.add_field(name=variable, value=f"{data_limiter(meta.get(variable, '<null>'),800)}")
                return await ctx.send(embed=embed)
        elif action == "set":
            if variable is None:
                raise ValueError("Variable name not provided.")
            if value is None:
                del(meta[variable])
            else:
                meta[variable] = value
            self.meta_update_local_entity(local_entity, meta)
            return await ctx.message.add_reaction("✅")

    @orm.db_session
    def meta_get_local_entity(self, ctx, entity):
        local_entity = None
        if type(entity) == discord.TextChannel:
            local_entity = get_or_create(Channel, id=entity.id)
        elif type(entity) in (discord.Member, discord.User):
            local_entity = get_or_create(Member,
                    user=get_or_create(User, id=entity.id),
                    guild=get_or_create(Guild, id=ctx.guild.id)
                    )
        elif type(entity) == str: # guild?
            if entity.lower() in ("guild", "g"):
                local_entity = get_or_create(Guild, id=ctx.guild.id)
            elif entity == ".":
                local_entity = get_or_create(Channel, id=ctx.channel.id)
            else:
                raise ValueError(f"Unknown entity: {str(entity)}")
        else:
            raise ValueError(f"Unknown entity: {str(entity)}")
        return local_entity

    @orm.db_session
    def meta_update_local_entity(self, entity, meta):
        db_entity = get_or_create(type(entity), id=entity.id)
        db_entity.meta = meta
 
Registry().add_cog(Metadata)

class Dev(commands.Cog, name="dev"):
    """Bot dev commands."""

    async def cog_check(self, ctx):
        return str(ctx.message.author.id) == str(Config().owner)

    @commands.command()
    async def umeta(self, ctx,
            user: discord.User = commands.parameter(description="Discord user tag or ID."),
            action: str = commands.parameter(description="get|set", default="get"),
            variable: str = commands.parameter(description="Variable name.", default=None),
            value: str = commands.parameter(description="New value for variable. Leave empty to delete or reset to default.", default=None)
            ):
        '''Display or update meta data for a discord user.
        Usage: meta USER get|set VARIABLE [VALUE]
        '''
        if Config().debug:
            print(locals())
        if action not in ("get", "set"):
            raise ValueError(f"Need to use 'get' or 'set' action. Provided: {str(action)}")
        local_entity = self.meta_get_local_user(ctx, user)
        meta = local_entity.meta
        
        if action == "get":
            embed = utils.make_embed(msg_type="info")
            if variable is None:
                # show meta
                embed.title = f"{(await local_entity.get_object()).name} meta"
                meta_list = ""
                for key in sorted(meta):
                    meta_list += f"{key}: {meta[key]}\n"
                embed.add_field(name="Variables", value=f"{meta_list}")
                return await ctx.send(embed=embed)
            else:
                # show one value
                embed.add_field(name=variable, value=f"{meta.get(variable, '<null>')}")
                return await ctx.send(embed=embed)
        elif action == "set":
            if variable is None:
                raise ValueError("Variable name not provided.")
            if value is None:
                del(meta[variable])
            else:
                meta[variable] = value
            self.meta_update_local_entity(local_entity, meta)
            return await ctx.message.add_reaction("✅")

    @orm.db_session
    def meta_get_local_user(self, ctx, user):
        local_user = None
        if type(user) == discord.User:
            local_user = get_or_create(User, id=user.id)
        return local_user

    @orm.db_session
    def meta_update_local_entity(self, entity, meta):
        db_entity = get_or_create(type(entity), id=entity.id)
        db_entity.meta = meta

Registry().add_cog(Dev)

