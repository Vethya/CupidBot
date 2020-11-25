from pyrogram import filters
from cupid import app
from .database import statsdb as db

@app.on_message(filters.text & filters.regex(r'^/top(?: lovers)?') & ~filters.private)
async def chat_stats(client, m):
    aw = await m.reply_text('Getting top lovers...')
    if not await db.get_chat_stats(m.chat.id):
        await aw.edit_text('No top lovers data for this chat yet!')
        return
    stats = await db.get_top_users(m.chat.id)
    stats = stats[:10]
    text = 'Here are the top lovers in this chat:\n'
    number = 1
    for user in stats:
        first_name = (await app.get_users(user['user_id'])).first_name
        text += f"{number}. {first_name} ({user['count']})\n"
        number += 1

    await aw.edit(text)

@app.on_message(filters.text & filters.regex(r'^/mystats'))
async def mystats(client, m):
    aw = await m.reply_text('Retrieving your stats...', quote=True)
    if m.chat.type == 'private':
        if not await db.get_global_user_stats(m.from_user.id):
            await aw.edit_text('No picking data for you yet!')
            return
        data = await db.get_global_user_stats(m.from_user.id)
        await aw.edit_text(f"You've been chosen <b>{data}</b> times!")
    elif m.chat.type in ['group', 'supergroup']:
        if not await db.get_chat_user_stats(m.chat.id, m.from_user.id):
            await aw.edit_text('No picking data for you yet!')
            return
        data = await db.get_chat_user_stats(m.chat.id, m.from_user.id)
        await aw.edit_text(f"You've been chosen <b>{data['count']}</b> times in this chat!")
