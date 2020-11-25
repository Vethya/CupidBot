from . import mongo

col = mongo.cli['Cupidbot']['stats']

async def add_stats(chat, user_id):
    return col.insert_one({'chat': chat, 'user_id': user_id, 'count': 1})

async def get_chat_user_stats(chat, user_id):
    return col.find_one({'chat': chat, 'user_id': user_id})

async def get_global_user_stats(user_id):
    count = 0
    for user in list(col.find({'user_id': user_id})):
        count += user['count']
    return count

async def get_chat_stats(chat):
    return col.find_one({'chat': chat})

async def update_stats(chat, user_id, count):
    return col.update_one({'chat': chat, 'user_id': user_id}, {'$set': {'chat': chat, 'user_id': user_id, 'count': count}})

async def get_top_users(chat):
    top = [i for i in col.find({'chat': chat})]
    top.sort(key=lambda i: i.get('count'), reverse=True)
    return top
