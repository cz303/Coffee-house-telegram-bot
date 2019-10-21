from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)

db = client['gh_coffee_db']

db.order_lists.delete_many({})

def check_and_add_user(message):
    if db.users.find_one({'user_id': message.from_user.id}) == None:
        new_user = {
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'user_id': message.from_user.id,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'state': 'Старт'
        }
        db.users.insert_one(new_user)
    return


def get_current_state(user_id):
    user = db.users.find_one({'user_id':user_id})
    return user['state']


def set_state(user_id, state_value):
    db.users.update_one({'user_id': user_id}, {"$set": {'state': state_value}})


def new_list(message, dt):
    new_list = {
                'date': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name,
                'user_id': message.from_user.id,
        }
    db.order_lists.insert_one(new_list)
    return


def set_category(datetime, user_id, message):
    db.order_lists.update_one({"$and": [{'date': datetime}, {'user_id': user_id}]}, {"$push": {"category": message.text}})


def delete_category(datetime, user_id):
    db.order_lists.update_one({"$and": [{'date': datetime}, {'user_id': user_id}]}, {"$pop": {"category": 1 }})


def set_item(datetime, user_id, message):
    db.order_lists.update_one({"$and": [{'date': datetime}, {'user_id': user_id}]}, {"$push": {"item": message.text}})


def delete_item(datetime, user_id):
    db.order_lists.update_one({"$and": [{'date': datetime}, {'user_id': user_id}]}, {"$pop": {"item": 1 }})


def set_item_size(datetime, user_id, message):
    db.order_lists.update_one({"$and": [{'date': datetime}, {'user_id': user_id}]}, {"$push": {"item_size": message.text}})


def set_tea_type(datetime, user_id, message):
    db.order_lists.update_one({"$and": [{'date': datetime}, {'user_id': user_id}]}, {"$push": {"tea_type": message.text}})


def get_item(datetime, user_id):
    cursor = db.order_lists.find({'date': datetime, 'user_id': user_id})
    for result_object in cursor:
        order = 'Ваш заказ: ' + '\n                 '.join('% s % s' % i for i in zip(result_object['item'], result_object['item_size']))
        return order