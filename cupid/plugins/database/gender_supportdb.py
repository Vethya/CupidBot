from . import mongo

col = mongo.cli['Cupidbot']

async def add_chat(chat):
    return col['gender_support_chats'].insert_one({'chat': chat})

async def is_gender_supported(chat):
    return True if col['gender_support_chats'].find_one({'chat': chat}) else False

async def rm_chat(chat):
    return col['gender_support_chats'].delete_one({'chat': chat})

async def list_gender_chats():
    return [i for i in col['gender_support_chats'].find({})]

async def set_gender(user_id, gender):
    return col['gender_support_users'].insert_one({'user_id': user_id, 'gender': gender})

async def update_gender(user_id, gender):
    return col['gender_support_users'].update_one({'user_id': user_id}, {'$set': {'user_id': user_id, 'gender': gender}})

async def get_gender(user_id):
    return col['gender_support_users'].find_one({'user_id': user_id})

async def list_gender_users():
    return [i for i in col['gender_support_users'].find({})]
