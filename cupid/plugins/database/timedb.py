from . import mongo

col = mongo.cli['Cupidbot']['timer']

async def add_time(chat, time):
    return col.insert_one({'chat': chat, 'time': time})

async def get_time(chat):
    return col.find_one({'chat': chat})

async def update_time(chat, time):
    return col.update_one({'chat': chat}, {'$set': {'chat': chat, 'time': time}})
