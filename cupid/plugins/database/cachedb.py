from . import mongo

col = mongo.cli['Cupidbot']['cache_data']

async def cache_members(chat, data):
    return col.insert_one({'chat': chat, 'data': data})

async def get_cache(chat):
    return col.find_one({'chat': chat})

async def update_cache(chat, data):
    return col.update_one({'chat': chat}, {'$set': {'chat': chat, 'data': data}})

async def clear_cache():
    return col.delete_many({})

async def clear_chat_cache(chat):
    return col.delete_one({'chat': chat})
