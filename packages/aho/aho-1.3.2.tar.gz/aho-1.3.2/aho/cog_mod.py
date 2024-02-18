"""
Moderator commands.
"""
from aho import Registry
from aho import utils
from discord.ext import commands
import discord

class Mod(commands.Cog, name="mod"):
    """Moderator commands."""

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount = commands.parameter(description="Lines to delete.", default="1")):
        """Delete N messages above.
        Usage: clear N
        """
        try:
            amount = int(amount)
        except:
            embed = utils.make_error("First argument needs to be number of messages to clear.")
            return await ctx.send(embed=embed)
        if amount < 1:
            embed = utils.make_error("I need a positive number of messages to clear.")
            return await ctx.send(embed=embed)
        if amount > 100:
            embed = utils.make_error("I refuse to clear more than 100 messages at once.")
            return await ctx.send(embed=embed)
        await ctx.message.delete()
        result = await ctx.channel.purge(limit=(amount))
        embed = utils.make_embed(msg_type="done")
        embed.title = "Clear"
        embed.description = f"Cleared {len(result)} messages in {ctx.channel.mention}."
        await utils.short_message(ctx, embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx,
            member: discord.Member = commands.parameter(description="Member tag or ID to be kicked."),
            *, reason: str = commands.parameter(description="Reason for the kick.", default = None),
            ):
        """Kick a member from guild.
        Usage: kick USER_TAG|USER_ID [REASON]
        """
        if member.guild_permissions.administrator:
            embed = utils.make_error("Can't kick an admin.")
            await ctx.send(embed=embed)
            return
        try:
            embed = utils.make_embed()
            embed.title = "Kick"
            embed.description = f"You are about to be kicked from **{ctx.guild.name}**."
            embed.add_field(name="Reason", value=reason)
            await member.send(embed=embed)
        except Exception as e:
            embed = utils.make_error(description=f"Could not DM {member.mention} about reasons for getting kicked.")
            embed.add_field(name="Info", value=e)
            await ctx.send(embed=embed)
        await ctx.guild.kick(member, reason=reason)
        embed = utils.make_embed('done')
        embed.title = 'Kick'
        embed.description = f"{member.mention} was kicked from the server!"
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(moderate_members=True)
    async def perms(self, ctx,
            user: discord.Member = commands.parameter(description="Member tag or ID to list roles for."), default=None):
        '''Member roles info.
        Usage: info [(USER_TAG|USER_ID)]
        Show user roles list in the guild.
        '''
        if user is None:
            user = ctx.author
        member = None
        try:
            member = ctx.guild.get_member(user.id)
        except:
            pass
        embed = utils.make_embed()
        embed.title = str(user)
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        if member:
            embed.description = member.mention
            perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
            embed.add_field(name="Guild permissions", value=perm_string or "None", inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx,
            user: discord.User = commands.parameter(description="User tag or ID to be banned."),
            *, reason: str = commands.parameter(description="Reason for the ban.", default = None),
            ):
        """Ban a member from guild.
        Usage: ban USER_TAG|USER_ID [REASON]
        """
        member = ctx.guild.get_member(user.id)
        if member:
            if member.guild_permissions.administrator:
                embed = utils.make_error("Can't ban an admin.")
                await ctx.send(embed=embed)
                return
            try:
                embed = utils.make_embed()
                embed.title = "Ban"
                embed.description = f"You are about to be banned from **{ctx.guild.name}**."
                embed.add_field(name="Reason", value=reason)
                await member.send(embed=embed)
            except Exception as e:
                embed = utils.make_error(description=f"Could not DM {member.mention} about reasons for getting banned.")
                embed.add_field(name="Info", value=e)
                await ctx.send(embed=embed)
        await ctx.guild.ban(user, reason=reason)
        embed = utils.make_embed('done')
        embed.title = 'Ban'
        embed.description = f"{user.mention} was banned from the server!"
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User = commands.parameter(description="User tag or ID to be unbanned.")):
        """Unban a user.
        Usage: unban USER_TAG|USER_ID
        """
        await ctx.guild.unban(user)
        embed = utils.make_embed('done')
        embed.title = "Ban lift"
        embed.description = f"Ban for {user.mention} has been lifted."
        await ctx.send(embed=embed)

Registry().add_cog(Mod)

