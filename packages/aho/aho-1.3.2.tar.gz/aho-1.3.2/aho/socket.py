"""
aho socket service.
"""
from aho import Config
from aho import Registry
from aho import base
from aho import color
from aho import utils
from aho.database import db, bind_database
from discord.ext import commands
import discord
import traceback
import socket
import os
import asyncio
import threading

async def start():
    try:
        os.unlink(Config().socket_file)
    except OSError:
        if os.path.exists(Config().socket_file):
            raise
    threading.Thread(target=_start_socket_server, daemon=True).start()


def _start_socket_server():
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(Config().socket_file)
    server_socket.listen()
    
    while Config().state == "active":
        client_socket, _ = server_socket.accept()
        data = client_socket.recv(1024).decode('utf-8')
        if Config().debug:
            print(f"=socket received: {data}")
        try:
            cmd, args = data.split('|', 1)
        except ValueError as e:
            print(e)
            print(f"data received was: {data}")
            cmd="NONE"
        if cmd == "msg":
            channel_id, message = args.split('|', 1)
            asyncio.run_coroutine_threadsafe(send_message(int(channel_id), message), base.bot.loop)
        elif cmd == "get":
            try:
                entity, more_data = args.split('|', 1)
            except ValueError as e:
                print(e)
                print(f"data received was: {data}")
                entity = "NONE"
            entity_list = None
            if entity == "guilds":
                print_list(base.get_guild_id_name_list())
            elif entity == "channels":
                print_list(base.get_channel_id_name_type_list(more_data))
            elif entity == "members":
                print_list(base.get_member_id_name_nick_list(more_data))
            elif entity == "messages":
                try:
                    channel_id, limit = more_data.split('|', 1)
                except ValueError as e:
                    channel_id = more_data
                    limit = 10
                asyncio.run_coroutine_threadsafe(get_messages(int(channel_id), int(limit)), base.bot.loop)
            else:
                print(f"Entity {entity} not recognized.")
        else:
            print(f"Command {cmd} not recognized.")
        client_socket.close()

async def get_messages(channel_id, limit):
    print(f"channel id: {channel_id}")
    print(f"limit: {limit}")
    channel = base.bot.get_channel(channel_id)
    print(f"=channel {channel.name} messages:")
    message_user_id_name_content_list = []
    async for m in channel.history(limit=limit):
        message_user_id_name_content_list.append([
            m.author.id,
            m.author.name,
            m.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            m.content,
            ])
    print_list(message_user_id_name_content_list)

async def send_message(channel_id, message):
    channel = base.bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
        print("=message sent")
    else:
        print(f"=Channel {channel_id} not found.")

def print_list(l):
    for e in l:
        print(" | ".join([str(i) for i in e]))

