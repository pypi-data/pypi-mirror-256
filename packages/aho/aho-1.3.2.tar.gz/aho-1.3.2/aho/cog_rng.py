"""
Dice and random tools commands.
"""
from aho import Registry
from aho import utils
from discord.ext import commands
import discord
import random

class Rng(commands.Cog, name="rng"):
    """Randoms."""

    @commands.command()
    async def roll(self, ctx, dice: str = commands.parameter(description="Die type.", default="1d6")):
        """Roll a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            embed = utils.make_error("Format has to be in **NdN**!")
            embed.add_field(
                    name="More on dice notation",
                    value="More info can be found here: https://en.wikipedia.org/wiki/Dice_notation"
                    )
            return await ctx.send(embed=embed)
        if rolls > 100 or limit > 100:
            embed = utils.make_error("I'm diced out!")
            embed.add_field(
                    name="Info",
                    value="Numbers of dice and sides can be up to 100."
                    )
            return await ctx.send(embed=embed)
        outcomes = [random.randint(1, limit) for r in range(rolls)]
        result = '+'.join([str(o) for o in outcomes])
        if rolls > 1:
            result += f" = {sum(outcomes)}"
        embed = utils.make_embed(author=ctx.message.author)
        embed.add_field(name=f"Rolled 🎲{dice}", value=f"Got: {result}")
        return await ctx.send(embed=embed)
 
Registry().add_cog(Rng)

