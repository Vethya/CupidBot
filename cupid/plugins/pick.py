from pyrogram import filters
from cupid import app, config, BLACKLIST
import random
from .database import lastdb, gender_supportdb as genderdb, cachedb, statsdb, timedb, autopindb
from datetime import datetime, timedelta

@app.on_message(filters.text & filters.regex(r'^/pick') & ~filters.private)
async def pick_couple(client, m):
    aw = await m.reply_text('Picking a couple...')
    if await timedb.get_time(m.chat.id):
        then = datetime.strptime((await timedb.get_time(m.chat.id))['time'], '%Y-%m-%d %H:%M:%S.%f')
        pickable_time = then + timedelta(hours=24)
        if datetime.now() != pickable_time:
            delta = pickable_time - datetime.now()
            time = str(timedelta(seconds=delta.seconds)).split(':')
            hours = f"{time[0]} hours" if time[0] else ''
            minutes = f"{time[1]} minutes" if time[1] else ''
            seconds = f"and {time[2]} seconds" if time[2] else ''
            last_pick = await lastdb.get_last_pick(m.chat.id)
            await aw.edit_text(f"Today's couple have already been picked <a href={last_pick['link']}>here</a>. Please wait {hours} {minutes} {seconds} for a new couple to be pickable!")
            return
    else:
        await timedb.add_time(m.chat.id, str(datetime.now()))
    list_chat_members = []
    if await genderdb.is_gender_supported(m.chat.id):
        if not await cachedb.get_cache(m.chat.id):
            async for member in client.iter_chat_members(m.chat.id):
                if not member.user.is_bot and member is not None and member.user.id not in BLACKLIST and member.user.id in [user['user_id'] for user in await genderdb.list_gender_users()]:
                    list_chat_members.append(member.user.id)
            
            await cachedb.cache_members(m.chat.id, list_chat_members)
        else:
            list_chat_members = (await cachedb.get_cache(m.chat.id))['data']
        if len(list_chat_members) < 2:
            await aw.edit_text('Not enough gender registered user!')
            return
    else:
        if not await cachedb.get_cache(m.chat.id):
            async for member in client.iter_chat_members(m.chat.id):
                if not member.user.is_bot and member is not None and member.user.id not in BLACKLIST:
                    list_chat_members.append(member.user.id)
            await cachedb.cache_members(m.chat.id, list_chat_members)
        else:
            list_chat_members = (await cachedb.get_cache(m.chat.id))['data']
    first = await client.get_users(random.choice(list_chat_members))
    if not await statsdb.get_chat_user_stats(m.chat.id, first.id):
        await statsdb.add_stats(m.chat.id, first.id)
    else:
        first_stats = await statsdb.get_chat_user_stats(m.chat.id, first.id)
        await statsdb.update_stats(m.chat.id, first.id, first_stats['count']+1)
    first_gender = (await genderdb.get_gender(first.id))['gender']
    second = await client.get_users(random.choice(list_chat_members))
    if not await statsdb.get_chat_user_stats(m.chat.id, second.id):
        await statsdb.add_stats(m.chat.id, second.id)
    else:
        second_stats = await statsdb.get_chat_user_stats(m.chat.id, second.id)
        await statsdb.update_stats(m.chat.id, second.id, second_stats['count']+1) 
    second_gender = (await genderdb.get_gender(second.id))['gender']
    if second == first:
        while True:
            second = await client.get_users(random.choice(list_chat_members))
            if second != first:
                break
    elif first_gender == second_gender:
        while True:
            second_gender = await genderdb.get_gender((await app.get_users(random.choice(list_chat_members))).id)
            if second_gender != first_gender:
                break
    text = f"<a href='tg://user?id={first.id}'>{first.first_name}</a> ♥ <a href='tg://user?id={second.id}'>{second.first_name}</a>"
    await aw.edit_text(f"Today's couple is:\n{text}")
    await timedb.update_time(m.chat.id, str(datetime.now()))
    if await lastdb.get_last_pick(m.chat.id):
        await lastdb.update_last_pick(m.chat.id, text, f"t.me/c/{str(m.chat.id)[4:]}/{aw.message_id}")
    else:
        await lastdb.add_last_pick(m.chat.id, text, f"t.me/c/{str(m.chat.id)[4:]}/{aw.message_id}")
    if await autopindb.get_chat(m.chat.id):
        await aw.pin(disable_notification=True)
