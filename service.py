import pprint
import json
from bson import json_util

from database import Database
from datetime import datetime, timedelta


class Service:

    # verify user
    @staticmethod
    def login_verification(email=None, password=None):
        try:
            print('login verification service')
            database = Database()
            user_data = database.get_user_by_mail(email=email)
            if user_data:
                if user_data[0]['password'] == password:
                    return {'message': 'Authorized', 'user_id': user_data[0]['user_id']}, 200
                else:
                    return {'message': "The Email id or Password you entered is incorrect."}, 401
            else:
                return {'message': "User doesn't exist, please Sign Up to continue"}, 401
        except Exception as error:
            return {'message': 'Error while verfying user - ' + str(error)}, 400


    # add created_date, last_modified in request body and insert in db
    # add user id, task id by quering the user id and task id from the collection
    @staticmethod
    def add_user(data=None):
        try:
            print('add_user - Service')
            database = Database()
            user_count = database.get_user_count()
            user_count = (user_count[0]['count'] if user_count else 0) + 1
            database.add_user_data(data={'user_id':user_count})
            data['user_id'] = user_count
            database.add_user(data)
            return {'message': 'Successfully inserted', 'user id': str(user_count)}, 201
        except Exception as error:
            print('Error in add_user service - ', error)
            return {'message': 'Insertion failed - ' + str(error)}, 400

    @staticmethod
    def get_all_users():
        try:
            print('get_all_users - Service')
            database = Database()
            return eval(json.dumps(database.get_all_users(), default=str)), 200
        except Exception as error:
            print('Error in get_all_users Service - ', error)
            return {'message': 'Error in getting all user information - ' + str(error)}, 400

    @staticmethod
    def get_user(user_id=None):
        try:
            print('get_user - Service')
            database = Database()
            return eval(json.dumps(database.get_user(user_id=user_id), default=str)), 200
        except Exception as error:
            print('Error in get_user Service - ', error)
            return {'message': 'Error in getting user information - ' + str(error)}, 400

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
                item['due_date'] = datetime.strptime(item['due_date'], "%a %b %d %Y %H:%M:%S %Z%z (IST)")
                task_count += 1
            updated_doc = database.add_task(user_id=user_id, data=data['todo'])
            del updated_doc['_id']
            return eval(json.dumps(updated_doc, default=str)), 200
        except Exception as error:
            print('Error inside add_task service - ', error)
            return {'message' : 'Failed to add new task - ' + str(error)}, 400

    # update task - given task_id and user_id
    # set last_modified
    @staticmethod
    def update_task(user_id=None, task_id=None, data=None):
        try:
            print('update_task - Service')
            database = Database()
            data['due_date'] = datetime.strptime(data['due_date'], "%a %b %d %Y %H:%M:%S %Z%z (IST)")
            data['last_modified'] = datetime.today()
            database.update_task(user_id=user_id, task_id=task_id, data=data)
            return {'message': 'Successfully Updated'}, 201
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
            return {'message': 'Task deleted successfully'}, 200
        except Exception as error:
            print('Error in delete_task (Service) - ', error)
            return {'message': 'Error while deleting task - ' + str(error)}, 400

    # delete all tasks for given user
    @staticmethod
    def delete_all_tasks(user_id=None):
        try:
            print('delete_all_tasks - Service')
            database = Database()
            database.delete_all_tasks(user_id=user_id)
            return {'message': 'All tasks deleted successfully'}, 200
        except Exception as error:
            print('Error in delete_task (Service) - ', error)
            return {'message': 'Error while deleting all tasks - ' + str(error)}, 400

    # update user
    @staticmethod
    def update_user(user_id=None, data=None):
        try:
            print('update_user Service')
            database = Database()
            database.update_user(user_id=user_id, data=data)
            return {'message': 'Successfully Updated'}, 201
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
            return {'message': 'User deleted successfully'}, 200
        except Exception as error:
            print('Error in delete_user (Service) - ', error)
            return {'message': 'Error while deleting user - ' + str(error)}, 400

    # get all tasks of a user
    @staticmethod
    def get_users_alltasks(user_id=None):
        try:
            print('get_users_alltasks - Service')
            database = Database()
            return eval(json.dumps(database.get_users_alltasks(user_id=user_id), default=str)), 200
        except Exception as error:
            print('Error in get_users_alltasks (Service) - ', error)
            return {'message': 'Error while getting tasks of a user- ' + str(error)}, 400

    # get all tasks of a user
    @staticmethod
    def get_user_task(user_id=None, task_id=None):
        try:
            print('get_user_task - Service')
            database = Database()
            return eval(json.dumps(database.get_user_task(user_id=user_id, task_id=task_id), default=str)), 200
        except Exception as error:
            print('Error in get_user_task (Service) - ', error)
            return {'message': 'Error while getting task for a user - ' + str(error)}, 400