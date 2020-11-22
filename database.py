import pymongo
import pprint
from datetime import datetime, timedelta


class Database:

    def __init__(self):
        self.conn = self.establish_connection()
        self.db = self.conn['todo_manager']


    # mongodb connection establishment with uri
    def establish_connection(self):
        try:
            return pymongo.MongoClient(
                "mongodb+srv://admin:admin@todo-manager.sivgr.mongodb.net/test?"
                "authSource=admin&replicaSet=atlas-osjex7-shard-0"
                "&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=true"
            )
        except Exception as error:
            print('Error while establishing connection - ', error)

    # verify user
    def get_user_by_mail(self, email=None):
        try:
            print('get user by mail - Database')
            collection = self.db['todo_user']
            return list(collection.find({'email': email}, {'_id': 0}))
        except Exception as error:
            print('Error while getting user by mail - ', error)

    # get total number of users in collection
    def get_user_count(self):
        try:
            print('get_user_count - Database')
            collection = self.db['todo_user']
            return list(collection.aggregate([
                {
                    '$group': {'_id': None, 'count': {'$max': '$user_id'}}
                }
            ]))
        except Exception as error:
            print('Error while getting total number of users - ', error)

    # get total number of tasks for given user
    def get_user_tasks_count(self, user_id=None):
        try:
            print('get_user_tasks_count - Database')
            collection = self.db['todo_data']
            return list(
                collection.aggregate([
                    {'$match': {'user_id': user_id}},
                    {'$unwind': "$todo"},
                    {'$group': {'_id': None, 'count': {'$max': '$todo.task_id'}}}
                ])
            )
            # return ""
        except Exception as error:
            print('Error while getting total number of tasks for user - ', str(user_id), ' - ', error)

    # add new user
    def add_user(self, data=None):
        try:
            print('add_user - Database')
            collection = self.db['todo_user']
            return collection.insert(data)
        except Exception as error:
            print('Error while adding user - ', error)

    # add new task for a user
    def add_task(self, user_id=None, data=None):
        try:
            print('add_task - Database')
            collection = self.db['todo_data']
            return collection.find_and_modify(
                query={'user_id': user_id},
                update={'$push': {'todo': {'$each': data}}},
                new=True
            )
        except Exception as error:
            print('Error while adding task for user - ', str(user_id), ' :- ', error)

    # update the task for given user and respective task
    def update_task(self, user_id=None, task_id=None, data=None):
        try:
            print('update_task - Database')
            collection = self.db['todo_data']
            modified_data = {}
            for key, value in data.items():
                modified_data['todo.$.' + key] = value
            return collection.update_one(
                {'user_id': user_id, 'todo.task_id': task_id},
                {'$set': modified_data}
            )
        except Exception as error:
            print('Error while updating task', str(task_id), ', for user ', str(user_id), ' :- ', error)

    # delete the task with given id for a user
    def delete_task(self, user_id=None, task_id=None):
        try:
            print('delete_task - Database')
            collection = self.db['todo_data']
            return collection.update_one(
                {'user_id': user_id},
                {'$pull': {'todo': {'task_id': task_id}}}
            )
        except Exception as error:
            print('Error while deleting task ', str(task_id), ', of user ', str(user_id), ' :- ', error)

    # delete all tasks for given user
    def delete_all_tasks(self, user_id=None):
        try:
            print('delete_all_tasks - Database')
            collection = self.db['todo_data']
            return collection.update(
                {'user_id': user_id},
                {'$unset': {'todo': ''}}
            )
        except Exception as error:
            print('Error while deleting all tasks for user - ', str(user_id), ' :- ', error)

    # get all tasks for given user
    def get_users_alltasks(self, user_id=None):
        try:
            print('get_users_alltasks Database')
            collection = self.db['todo_data']
            return list(collection.find({'user_id': user_id}, {'_id': 0, 'todo': 1}))
        except Exception as error:
            print('Error while retrieving all tasks for user ', str(user_id),' - ', error)

    # get particular task for a given user
    def get_user_task(self, user_id=None, task_id=None):
        try:
            print('get_user_task Database')
            collection = self.db['todo_data']
            return list(collection.find({'user_id': user_id, 'todo.task_id': task_id}, {'_id': 0, 'todo.$': 1}))
        except Exception as error:
            print('Error while retrieving task - ', str(task_id), ', for user - ', str(user_id), ' :- ', error)

    # get user
    def get_user(self, user_id=None):
        try:
            collection = self.db['todo_data']
            return list(collection.find({'user_id': user_id}, {'_id': 0}))
        except Exception as error:
            print('Error while retrieving user ', str(user_id), ' - ', error)

    # get all users
    def get_all_users(self):
        try:
            collection = self.db['todo_data']
            response = list(collection.find({}, {'_id': 0}).sort('user_id', 1))
            return response
        except Exception as error:
            print('Error while retrieving all users - ', error)

    # update user
    def update_user(self, user_id=None, data=None):
        try:
            print('update_user - Database')
            collection = self.db['todo_data']
            # modified_data = {}
            return collection.update_one(
                {'user_id': user_id},
                {'$set': data}
            )
        except Exception as error:
            print('Error while updating user ', str(user_id), ' :- ', error)

    # delete given user
    def delete_user(self, user_id=None):
        try:
            print('delete_user Database')
            data_collection = self.db['todo_data']
            user_collection = self.db['todo_user']
            data_collection.delete_one(
                {'user_id': user_id},
            )
            return user_collection.delete_one((
                {'user_id': user_id}
            ))
        except Exception as error:
            print('Error while deleting user ', str(user_id), ' :- ', error)

# db = Database()
# print(db.get_users_alltasks(user_id=4))
# print(db.get_user_task(user_id=4, task_id=1))
# db.delete_user(user_id=3)
# update_user = {
#     'last_name': 'N A G S'
# }
# db.update_user(user_id=2, data=update_user)
# print(db.get_user_count())
# task_count = list(db.get_user_tasks_count(user_id=1))
# task_count = task_count[0]['count'] if task_count else 0
# print(task_count)
# add_user = {
#             'user_id': 1,
#             'first_name': 'Chinmay',
#             'last_name': 'Gopal',
#             'todo': [
#                 {
#                     'task_id': 1,
#                     'task': 'Complete database part',
#                     'priority': 'high',
#                     'due_date': datetime.today() + timedelta(days=1),
#                     'category': 'projects',
#                     'created_date': datetime.today()
#                 },
#             ]
#         }
# print('Data added with id: ', db.add_user(add_user))
# add_task = {
#     'task_id': 2,
#     'task': 'establish database',
#     'priority': 'high',
#     'due_date': datetime.today() + timedelta(days=1),
#     'category': 'projects',
#     'created_date': datetime.today()
# }
# print(db.add_task(user_id=1, data=add_task))
# update_task = {
#     'task': 'Setup db',
#     'priority': 'high',
#     'last_modified': datetime.today()
# }
# result = db.update_task(user_id=1, task_id=1, data=update_task)
# db.delete_task(user_id=2, task_id=1)
# db.delete_all_tasks(user_id=1)
# pprint.pprint(db.get_user(user_id=1))