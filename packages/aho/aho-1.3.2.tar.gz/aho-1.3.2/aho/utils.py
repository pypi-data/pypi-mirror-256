"""
Discord embeds and other helper functions.
"""
from discord.ext import commands
import discord
import time

limits = {
        'title': 256,
        'description': 2048,
        'fields': 25,
        'field.name': 256,
        'field.value': 256,
        'footer.text': 2048,
        'author.name': 256,
        }

def make_embed(msg_type='info', author=None):
    color_from_type = {
            "info": 0x000000,
            "done": 0x00ff00,
            "ok": 0x00ff00,
            "warn": 0xffff00,
            "warning": 0xffff00,
            "error": 0xff0000,
            "critical": 0xff0000,
            "fun": 0xaa00ff,
            }
    embed = discord.Embed(color=color_from_type[msg_type])
    if author:
        embed.set_author(name=author.name, icon_url=author.avatar.url)
    return embed

def make_error(description=""):
    embed = make_embed(msg_type='error')
    embed.title="❗Error"
    embed.description = description
    return embed

async def short_message(messageable, embed, duration: float=5.0):
    message = await messageable.send(embed=embed)
    time.sleep(duration)
    await message.delete()

class LongMessage():
    ctx = None
    content = None
    msg_type = None
    author = None
    title = None
    icon = None
    thumbnail = None
    image = None
    type_color = {
            "info": 0x000000,
            "done": 0x00ff00,
            "ok": 0x00ff00,
            "warn": 0xffff00,
            "warning": 0xffff00,
            "error": 0xff0000,
            "critical": 0xff0000,
            "fun": 0xaa00ff,
            }

    def __init__(self, ctx=None, msg_type='info'):
        self.ctx = ctx
        self.msg_type = msg_type.lower()
        self.author = None
        self.title = ''
        self.icon = None
        self.thumbnail = None
        self.image = None
        self.content = commands.Paginator(prefix="", suffix="")
        if self.msg_type == 'error':
            self.title="❗Error"
            self.content = commands.Paginator()
        if self.msg_type in ('warn', 'warning'):
            self.title="⚠️Warning"
   
    def add_line(self, line):
        self.content.add_line(line)

    def add_lines(self, lines):
        for line in lines:
            self.content.add_line(line)

    def compose(self):
        embeds = []
        for page in self.content.pages:
            embed = discord.Embed(color=self.type_color[self.msg_type])
            embed.description = page
            embeds.append(embed)
        i = 0
        if len(embeds) > 1:
            for embed in embeds:
                i += 1
                embed.set_footer(text=f"{i}/{len(embeds)}")
        if self.author:
            embeds[0].author = author
        if self.title:
            embeds[0].title = self.title
        if self.thumbnail:
            embeds[0].set_thumbnail(url=self.thumbnail)
        if self.image:
            embeds[-1].set_image(url=self.image)
        return embeds
    
    async def reply(self, message=None):
        embeds = self.compose()
        if not message:
            message = self.ctx.message
        await message.reply(embed = embeds[0])
        for embed in embeds[1:]:
            await message.channel.send(embed = embed)

    async def send(self, messageable=None):
        embeds = self.compose()
        if not messageable:
            messageable = self.ctx 
        for embed in embeds:
            await messageable.send(embed=embed)


