"""
aho - a Discord bot.
"""
__version__ = "1.3.2"
__license__ = "BSD"
__year__ = "2023"
__author__ = "Predrag Mandic"
__author_email__ = "predrag@nul.one"
__copyright__ = f"Copyright {__year__} {__author__} <{__author_email__}>"

class AhoException(Exception):
    "Generic aho exception."
    pass

def Singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@Singleton
class Registry():
    cogs = []
    processors = []

    def add_cog(self, cog):
        self.cogs.append(cog)

    def add_processor(self, processor):
        self.processors.append(processor)

@Singleton
class Config():
    bot_name = "Aho"
    bot_description = "aho bot"
    default_prefix = "aho "
    debug = False
    log_file = None
    db_path = ":memory:"
    owner = None
    openai_api_key = None
    openai_system_message = None
    state = "active"
    socket_file = "./bot.sock"

class color:
    purple = "\033[95m"
    cyan = "\033[96m"
    darkcyan = "\033[36m"
    blue = "\033[94m"
    green = "\033[92m"
    yellow = "\033[93m"
    red = "\033[91m"
    bold = "\033[1m"
    underline = "\033[4m"
    end = "\033[0m"

