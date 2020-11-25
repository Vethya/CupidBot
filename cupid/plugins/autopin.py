from pyrogram import filters
from cupid import app, admin_only
from .database import autopindb as db

@app.on_message(filters.text & filters.regex(r'^/a(?: uto)?p(?: in)? (.+)') & ~filters.private)
@admin_only
async def auto_pin(client, m):
    options = ['on', 'off']
    match = m.matches[0].group(1)
    if match not in options:
        await m.reply_text('Invalid option!')
        return
    if match == options[0]:
        if await db.get_chat(m.chat.id):
            await m.reply_text('Autopin is already enabled in this chat!')
            return
        else:
            await db.add_chat(m.chat.id)
            await m.reply_text('Autopin successfully enabled!')
    if match == options[1]:
        if not await db.get_chat(m.chat.id):
            await m.reply_text('Autopin is already disabled in this chat!')
            return
        else:
            await db.rm_chat(m.chat.id)
            await m.reply_text('Autopin successfully disabled!')
