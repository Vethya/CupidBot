from pyrogram import filters
from cupid import app
from .database import lastdb as db

@app.on_message(filters.text & filters.regex(r'^/last') & ~filters.private)
async def last_pick(client, m):
    aw = await m.reply_text('Getting last couple...')
    text = await db.get_last_pick(m.chat.id)
    if text is None:
        await aw.edit_text('No last pick data stored for this chat yet!')
        return
    await aw.edit_text(f"Last picked couple is:\n{text['text']}")
