import pprint
import json
from bson import json_util

from database import Database
from datetime import datetime, timedelta


class Service:

    # convert datetime object to str
    @staticmethod
    def my_convertor(o):
        if isinstance(o, datetime):
            return o.__str__()

    # add created_date, last_modified in request body and insert in db
    # add user id, task id by quering the user id and task id from the collection
    @staticmethod
    def add_user(data=None):
        try:
            print('add_user - Service')
            database = Database()
            data['user_id'] = database.get_user_count() + 1
            task_count = database.get_user_tasks_count(user_id=data['user_id'])
            task_count = task_count[0]['count'] if task_count else 0
            for item in data['todo']:
                item['task_id'] = task_count + 1
                item['created_date'] = datetime.today()
                item['last_modified'] = datetime.today()
                item['due_date'] = datetime.strptime(item['due_date'], '%Y-%m-%d')
                task_count += 1
            object_id = database.add_user(data)
            return {'Message': 'Successfully inserted, object id - ' + str(object_id)}, 201
        except Exception as error:
            print('Error in add_user service - ', error)
            return {'Message': 'Insertion failed - ' + str(error)}, 400

    @staticmethod
    def get_user(user_id=None):
        try:
            print('get_user - Service')
            database = Database()
            return json.dumps(database.get_user(user_id=user_id), default=Service.my_convertor), 200
        except Exception as error:
            print('Error in get_user Service - ', error)
            return {'Message': 'Error in getting user information - ' + str(error)}, 400

    # add tasks to the given user
    # add task id, created_date, last_modified and due date to the object
    @staticmethod
    def add_task(user_id=None, data=None):
        try:
            print('add_task - Serivce')
            database = Database()
            task_count = database.get_user_tasks_count(user_id=user_id)
            task_count = task_count[0]['count'] if task_count else 0
            for item in data['todo']:
                item['task_id'] = task_count + 1
                item['created_date'] = datetime.today()
                item['last_modified'] = datetime.today()
                item['due_date'] = datetime.strptime(item['due_date'], '%Y-%m-%d')
                task_count += 1
            updated_doc = database.add_task(user_id=user_id, data=data['todo'])
            del updated_doc['_id']
            return json.dumps(updated_doc, default=Service.my_convertor), 200
        except Exception as error:
            print('Error inside add_task service - ', error)
            return {'Message' : 'Failed to add new task - ' + str(error)}, 400

    # update task - given task_id and user_id
    # set last_modified
    @staticmethod
    def update_task(user_id=None, task_id=None, data=None):
        try:
            print('update_task - Service')
            database = Database()
            data['last_modified'] = datetime.today()
            database.update_task(user_id=user_id, task_id=task_id, data=data)
            return {'Message': 'Successfully Updated'}, 201
        except Exception as error:
            print('Error in update_task (Service) - ', error)
            return {'Messsage': 'Task updation failed - ' + str(error)}, 400

    # delete given task for given user
    @staticmethod
    def delete_task(user_id=None, task_id=None):
        try:
            print('delete_task - Service')
            database = Database()
            database.delete_task(user_id=user_id, task_id=task_id)
            return {'Message': 'Task deleted successfully'}, 200
        except Exception as error:
            print('Error in delete_task (Service) - ', error)
            return {'Message': 'Error while deleting task - ' + str(error)}, 400

    # delete all tasks for given user
    @staticmethod
    def delete_all_tasks(user_id=None):
        try:
            print('delete_all_tasks - Service')
            database = Database()
            database.delete_all_tasks(user_id=user_id)
            return {'Message': 'All tasks deleted successfully'}, 200
        except Exception as error:
            print('Error in delete_task (Service) - ', error)
            return {'Message': 'Error while deleting all tasks - ' + str(error)}, 400

    # update user
    @staticmethod
    def update_user(user_id=None, data=None):
        try:
            print('update_user Service')
            database = Database()
            database.update_user(user_id=user_id, data=data)
            return {'Message': 'Successfully Updated'}, 201
        except Exception as error:
            print('Error in update_user(Service) - ', error)
            return {'Messsage': 'User updation failed - ' + str(error)}, 400

    # delete user
    @staticmethod
    def delete_user(user_id=None):
        try:
            print('delete_user - Service')
            database = Database()
            database.delete_user(user_id=user_id)
            return {'Message': 'User deleted successfully'}, 200
        except Exception as error:
            print('Error in delete_user (Service) - ', error)
            return {'Message': 'Error while deleting user - ' + str(error)}, 400

    # get all tasks of a user
    @staticmethod
    def get_users_alltasks(user_id=None):
        try:
            print('get_users_alltasks - Service')
            database = Database()
            return json.dumps(database.get_users_alltasks(user_id=user_id), default=Service.my_convertor), 200
        except Exception as error:
            print('Error in get_users_alltasks (Service) - ', error)
            return {'Message': 'Error while getting tasks of a user- ' + str(error)}, 400

    # get all tasks of a user
    @staticmethod
    def get_user_task(user_id=None, task_id=None):
        try:
            print('get_user_task - Service')
            database = Database()
            return json.dumps(database.get_user_task(user_id=user_id, task_id=task_id), default=Service.my_convertor), 200
        except Exception as error:
            print('Error in get_user_task (Service) - ', error)
            return {'Message': 'Error while getting task for a user - ' + str(error)}, 400