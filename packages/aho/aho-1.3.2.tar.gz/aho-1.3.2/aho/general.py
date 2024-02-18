"""
General commands.
"""
from aho import base
from aho import utils
from aho.bot import bot
from aho.database import get_or_create
from discord.ext import commands
from pony import orm
import aho
import discord


@bot.command()
async def version(ctx):
    """Display bot version."""
    await ctx.send(aho.__version__)

@bot.command()
async def embed(ctx,
        title: str = commands.parameter(description="Message title."),
        *, message: str = commands.parameter(description="Message body."),
        ):
    '''Embed a message.
    Usage: embed "Some title" Some message.
    Bot will send your embeded message in same channel and delete the original.
    '''
    if not title or not message:
        error = utils.make_error(description="Missing arguments. Usage: embed \"Some Title\" Some message.")
        return await ctx.send(embed=embed)
    embed = utils.make_embed(author=ctx.message.author)
    embed.title = title
    embed.description = message
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command()
async def avatar(ctx, user: discord.User = commands.parameter(description="User tag or ID.", default=None)):
    '''Display user avatar.
    Usage: avatar [USER_TAG|USER_ID]
    '''
    if user is None:
        user = ctx.author
    if user.avatar:
        return await ctx.send(user.avatar.url)
    return await ctx.send(f"User {user.name} has no avatar.")

@bot.command()
async def info(ctx, user: discord.User = commands.parameter(description="User tag or ID.", default=None)):
    '''User info.
    Usage: info [(USER_TAG|USER_ID)]
    Show user information.
    '''
    if user is None:
        user = ctx.author
    member = None
    try:
        member = ctx.guild.get_member(user.id)
    except:
        pass
    date_format = "%Y-%m-%d %H:%M"
    embed = utils.make_embed()
    embed.title = str(user)
    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)
    if member:
        embed.description = member.mention
        embed.add_field(name="📅 Joined", value=member.joined_at.strftime(date_format))
        embed.add_field(name="🪙 Points", value=get_points(member))
        if len(member.roles) > 1:
            role_string = ' '.join([r.mention for r in member.roles][1:])
            embed.add_field(name=f"🏷️ Roles [{len(member.roles)-1}]", value=role_string, inline=False)
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        if not member.bot:
            embed.add_field(name="#️⃣ Join position", value=str(  list(filter(lambda x: not x.bot, members)).index(member)  +1))
        embed.add_field(name="📄 Registered", value=user.created_at.strftime(date_format))
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)

@orm.db_session
def prefix_set(ctx, new_prefix):
    guild = get_or_create(base.Guild, id=ctx.guild.id)
    guild.prefix = new_prefix

@orm.db_session
def get_points(discord_member):
    member = get_or_create(base.Member,
            user=get_or_create(base.User, id=discord_member.id),
            guild=get_or_create(base.Guild, id=discord_member.guild.id)
            )
    return member.points

@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, prefix: str = commands.parameter(description="New prefix.")):
    '''Set new prefix.'''
    prefix_set(ctx, prefix)
    embed = utils.make_embed(msg_type="done")
    embed.title = "Prefix"
    embed.add_field(name="New prefix set:", value=prefix)
    return await ctx.send(embed=embed)


