"""
translator - message processor.
"""
from aho import Config
from aho import Registry
from aho import base
from aho.database import get_or_create
from pony import orm
import emoji
import googletrans
import re

base.channel_meta_defaults["translate"] = ""

tr = googletrans.Translator()

@orm.db_session
def get_langs(message):
    channel = get_or_create(base.Channel, id=message.channel.id)
    langs = channel.meta.get("translate", None)
    if langs:
        return langs.split(",")

async def google_translator(message):
    if message.author.bot:
        return
    if not message.content:
        return
    if message.content.startswith(base.get_prefix(message)):
        return
    if not re.search(r"\w", message.content):
        return
    if bool(re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', message.content)):
        return
    if bool(re.match(r'^\s*(((:[a-zA-Z0-9_]+:)|(<:[a-zA-Z0-9_]+:[0-9]+>))\s*)+$', message.content)):
        return
    if bool(re.match(r'^[wW\s]*$', message.content)):
        return
    if bool(re.match(r'^$', message.content)):
        return
    langs = get_langs(message)
    if not langs:
        return
    response = ""
    detection = tr.detect(message.content)
    if Config().debug:
        print(f"translate: detected={detection.lang}, confidence={detection.confidence}")
    detected = None
    if type(detection.lang) == list:
        for d in detection.lang:
            if d in langs:
                detected = d
                break
        if not detected:
            detected = detection.lang[0]
    else:
        detected =  detection.lang
    if detected == "gn":
        detected = "en"
        if Config().debug:
            print("Changing detected from gn to en.")
    for language in langs:
        if detected != language:
            translation = tr.translate(message.content, src=detected, dest=language)
            if response:
                response += "\n"
            response += f"{translation.text}"
    if response:
        await message.reply(response)

Registry().add_processor(google_translator)

