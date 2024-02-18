"""
aho bot main module.
"""
from aho import AhoException
from aho import Config
import aho as app
import click
import discord
import os
import socket
import sys

@click.group()
@click.version_option(version=app.__version__,
    message=f"%(prog)s %(version)s - {app.__copyright__}")
@click.option('-d', '--debug', is_flag=True,
    help="Enable debug mode with output of each action in the log.")
@click.pass_context
def cli(ctx, **kwargs): # pragma: no cover
    if ctx.params.get('debug'):
        print("Starting in debug mode. Errors shown in Discord will contain stack trace.")
        Config().debug = True

@cli.command()
@click.option('-t', '--token', required=False,
    help="Authorization token. If not provided, it will read TOKEN env var.")
@click.option('--openai', required=False,
    help="OpenAI API secret key. If not provided, it will read OPENAI_API_KEY env var.")
@click.option('-o', '--owner', required=False,
    help="Bot owner (dev) Discord user ID. If not provided, it will read OWNER env var.")
@click.option('--database', required=False,
    help="Path to sqlite database file. If not provided, will use ram.")
@click.option('--prefix', required=False, default='aho',
    help="Default prefix.")
@click.option('--description', required=False,
    help="Bot description.")
@click.option('-n', '--name', required=False,
    help="Bot name.")
@click.option('--openai-system-message', required=False, default='',
    help="Default OpenAI system message.")
@click.option('-l', '--log-file', required=False, default=None,
    help="Log file path.")
def run(**kwargs): # pragma: no cover
    "Run bot service."
    default_prefix = kwargs['prefix'] or os.getenv('DEFAULT_PREFIX')
    if default_prefix:
        Config().default_prefix = default_prefix + " "
    bot_description = kwargs['description'] or os.getenv('BOT_DESCRIPTION')
    if bot_description:
        Config().bot_description = bot_description
    bot_name = kwargs["name"] or os.getenv('BOT_NAME')
    if bot_name:
        Config().bot_name = bot_name
    token = os.getenv('TOKEN')
    if kwargs['token']:
        token = kwargs['token']
    if not token:
        raise AhoException("No token provided.")
    owner = os.getenv('OWNER')
    if kwargs['owner']:
        owner = kwargs('OWNER')
    Config().owner = owner
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if kwargs['openai']:
        openai_api_key = kwargs('openai')
    Config().openai_api_key = openai_api_key
    openai_system_message = kwargs['openai_system_message'] or os.getenv('OPENAI_SYSTEM_MESSAGE')
    Config().openai_system_message = openai_system_message
    if kwargs['log_file']:
        Config().log_file = kwargs["log_file"]
    if kwargs['database']:
        db_path = os.path.abspath(os.path.expanduser(kwargs['database']))
        Config().db_path = db_path
    from aho import bot
    try:
        bot.run(token)
    except KeyboardInterrupt:
        Config().state = "shutdown"
        sys.exit(0)

def send_socket_command(command):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(Config().socket_file)
        sock.sendall(command.encode('utf-8'))

@cli.command()
@click.argument('channel_id', type=int, required=True)
@click.argument('message', type=str, nargs=-1, required=True)
def msg(**kwargs): #pragma: no cover
    "Send a message to a channel."
    command = f'msg|{kwargs["channel_id"]}|{" ".join(kwargs["message"])}'
    send_socket_command(command)

@cli.command()
@click.argument('entity', type=click.Choice(['guilds', 'channels', 'members', "messages"]))
@click.argument('data', type=str, nargs=-1, required=False, default=None)
def get(**kwargs): #pragma: no cover
    "Print guilds, channels or members with IDs and names."
    command = f'get|{kwargs["entity"]}|{"|".join(kwargs["data"])}'
    send_socket_command(command)


if __name__ == '__main__': # pragma: no cover
    cli()

