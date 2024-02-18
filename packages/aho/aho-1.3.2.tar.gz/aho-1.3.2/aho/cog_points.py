"""
Points commands.
"""
from aho import AhoException
from aho import Registry
from aho import base
from aho import utils
from aho.database import get_or_create
from discord.ext import commands
from pony import orm
import discord
import json


class Points(commands.Cog, name="points"):
    """Points commands."""

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(moderate_members=True)
    async def transaction(self, ctx,
            member: discord.Member = commands.parameter(description="Member tag or ID to have points changed."),
            amount: int = commands.parameter(description="Number of points, can be positive or negative."),
            *, reason: str = commands.parameter(description="Reason for the change.", default = None),
            ):
        """Remove or add points to a member.
        Usage: transaction USER_TAG|USER_ID POINTS [REASON]
        """
        change, balance = update_member_points(member, amount)
        try:
            embed = utils.make_embed()
            embed.title = "Transaction"
            embed.description = f"**{ctx.guild.name}**| Your points balance has changed by {change}. New balance: {balance}."
            embed.add_field(name="Reason", value=reason)
            await member.send(embed=embed)
        except Exception as e:
            embed = utils.make_error(description=f"Could not DM {member.mention} about the transaction.")
            embed.add_field(name="Info", value=e)
            await ctx.send(embed=embed)
        embed = utils.make_embed('done')
        embed.title = 'Transaction'
        embed.description = f"{member.mention} "
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)


@orm.db_session
def update_member_points(discord_member, amount):
    """Return tuple: openai_api_key, openai_system_message, message_log, log_length"""
    member = get_or_create(base.Member,
            user=get_or_create(base.User, id=discord_member.id),
            guild=get_or_create(base.Guild, id=discord_member.guild.id)
            )
    points = member.points
    points += amount
    if points < 0:
        raise AhoException("User doesn't have enough points.")
    member.points = points
    return amount, points


Registry().add_cog(Points)

