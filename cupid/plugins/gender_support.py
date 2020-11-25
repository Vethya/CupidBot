from pyrogram import filters
from cupid import app, config
from .database import gender_supportdb as db

@app.on_message(filters.text & filters.regex(r'^/g(?: ender)?s(?: upport)? (.+)') & ~filters.private)
async def gender_support_switch(client, m):
    options = ['on', 'off']
    match = m.matches[0].group(1)
    if match not in options:
        await m.reply_text('Invalid options!')
        return
    if match == options[0]:
        if await db.is_gender_supported(m.chat.id):
            await m.reply_text('Gender Support is already enabled in this chat!')
            return
        await db.add_chat(m.chat.id)
        await m.reply_text('Gender Support successfully enabled!')
    if match == options[1]:
        if not await db.is_gender_supported(m.chat.id):
            await m.reply_text('Gender Support is already disabled in this chat!')
            return
        await db.rm_chat(m.chat.id)
        await m.reply_text('Gender Support successfully disabled!')

@app.on_message(filters.text & filters.regex(r'^/register (.+)') & ~filters.private)
async def register_gender(client, m):
    if await db.get_gender(m.from_user.id):
        if m.matches[0].group(1) not in ['male', 'female']:
            await m.reply_text('Invalid gender specified!')
            return

        await m.reply_text('Gender successfully updated!')
    else:
        if m.matches[0].group(1) not in ['male', 'female']:
            await m.reply_text('Invalid gender specified!')
            return
        await db.set_gender(m.from_user.id, m.matches[0].group(1))
        await m.reply_text('Gender successfully set!')

@app.on_message(filters.text & filters.regex(r'^/mygender'))
async def my_gender(client, m):
    aw = await m.reply_text('Getting your registered gender...')
    gender = await db.get_gender(m.from_user.id)
    if not gender:
        await aw.edit_text("You haven't register your gender yet!")
        return
    await aw.edit_text(f"You registered gender is <b>{gender['gender']}</b>!")
