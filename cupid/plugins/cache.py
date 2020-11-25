from pyrogram import filters
from cupid import app, sudo_only, admin_only
from .database import gender_supportdb as genderdb, cachedb

@app.on_message(filters.text & filters.regex(r'^/c(?: ache)?m(?: ember)?') & ~filters.private)
async def cache_member(client, m):
    aw = await m.reply_text('Caching members...')
    list_chat_members = []
    if await genderdb.is_gender_supported(m.chat.id):
        async for member in app.iter_chat_members(m.chat.id):
            if not member.user.is_bot and member is not None and member.user.id in [user['user_id'] for user in await genderdb.list_gender_users()]:
                list_chat_members.append(member.user.id)
    else:
        async for member in app.iter_chat_members(m.chat.id):
            if not member.user.is_bot and member is not None:
                list_chat_members.append(member.user.id)
    if not await cachedb.get_cache(m.chat.id):
        await cachedb.cache_members(m.chat.id, list_chat_members)
        await aw.edit_text('Successfully cached member list!')
    else:
        await cachedb.update_cache(m.chat.id, list_chat_members)
        await aw.edit_text('Successfully updated cached member list!')

@app.on_message(filters.text & filters.regex(r'^/clearc(?: ache)?'))
@sudo_only
async def clear_allcache(client, m):
    await cachedb.clear_cache()
    await m.reply_text('Successfully cleared all cache data!')
