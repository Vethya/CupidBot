from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from cupid import app

@app.on_message(filters.text & filters.regex(r'^/(start|alive)'))
async def start(client, m):
    await m.reply_text(
            "Hello! I'm a bot that <b>picks couple</b> in your group. This bot is highly inspired by @SHIPPERINGbot :). Do /help to see the available commands!",
            reply_markup=InlineKeyboardMarkup(
                    [
                            [InlineKeyboardButton('Pyrogram', url='docs.pyrogram.org'), InlineKeyboardButton('Source Code', url='github.com/Vethya/CupidBot')]
                        ]
                )
            )
