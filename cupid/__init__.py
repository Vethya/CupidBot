import logging
import traceback
import time
from pyrogram import Client
import yaml
import os
import functools

with open('config.yaml') as config:
    config = yaml.safe_load(config)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BLACKLIST = [777000, 1087968824]

def sudo_only(func):
    @functools.wraps(func)
    async def wrapper(client, m):
        user_id = m.from_user.id
        if user_id in config['config']['sudo_id']:
            await func(client, m)
    return wrapper

def admin_only(func):
    @functools.wraps(func)
    async def wrapper(client, m):
        user_status = (await client.get_chat_member(m.chat.id, m.from_user.id)).status
        if user_status in ['creator', 'administrator']:
            await func(client, m)
    return wrapper

app = Client(
            'cupidbot',
            api_id=config['telegram']['api_id'],
            api_hash=config['telegram']['api_hash'],
            plugins={'root': os.path.join(__package__, 'plugins')},
            parse_mode='html',
            bot_token=config['telegram']['bot_token']
        )

app.run()
