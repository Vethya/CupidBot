from . import mongo

col = mongo.cli['Cupidbot']['autopin_chats']

async def add_chat(chat):
    return col.insert_one({'chat': chat})

async def get_chat(chat):
    return col.find_one({'chat': chat})

async def rm_chat(chat):
    return col.delete_one({'chat': chat})
