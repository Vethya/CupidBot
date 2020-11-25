from . import mongo

col = mongo.cli['Cupidbot']['last_pick']

async def add_last_pick(chat, text, link):
    return col.insert_one({'chat': chat, 'text': text, 'link': link})

async def get_last_pick(chat):
    return col.find_one({'chat': chat})

async def update_last_pick(chat, text, link):
    return col.update_one({'chat': chat}, {'$set': {'chat': chat, 'text': text, 'link': link}})
