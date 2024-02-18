"""
Emoji related commands.
"""
from aho import Registry
from aho import utils
from discord.ext import commands
import discord

class Emoji(commands.Cog, name="emoji"):
    """Emoji related commands."""

    @commands.command()
    async def getemoji(self, ctx, emoji: discord.PartialEmoji):
        '''Get URL of an emoji.'''
        # Check if the emoji is custom (has an URL)
        if emoji.is_custom_emoji():
            await ctx.message.reply(emoji.url)
        else:
            await ctx.message.reply("This command only works with custom emojis.")

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def addemoji(self, ctx, emoji: discord.PartialEmoji, new_name: str = None):
        '''Copy a custom emoji to the server from an existing emoji with an optional new name.'''
        if emoji.is_custom_emoji():
            # Use the provided new name if available, otherwise use the original emoji name
            emoji_name = new_name if new_name else emoji.name

            try:
                # Create a new custom emoji in the server
                new_emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=await emoji.read())
                await ctx.message.reply(f'{new_emoji} added')
            except discord.HTTPException as e:
                await ctx.message.reply(f'Failed to add emoji: {e}')
        else:
            await ctx.send("This command only works with custom emojis from other servers.")


Registry().add_cog(Emoji)

