from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS

# service class
from service import Service

# Flask initialisation
app = Flask(__name__)
app.debug = True
app.config['SWAGGER'] = {"title": "ToDo Manager : Swagger-UI", "uiversion": 2}
CORS(app)
api = Api(app)


class User(Resource):

    @staticmethod
    def post():
        print('Post User - Controller')
        service = Service()
        request_body = request.get_json()
        return service.add_user(data=request_body)

    @staticmethod
    def get():
        print('Get User - Controller')
        try:
            user_id = request.args['userId']
            service = Service()
            response = service.get_user(user_id=int(user_id))
        except:
            service = Service()
            response = service.get_all_users()
        # print('type of response - ', type(response))
        return response

    @staticmethod
    def put():
        print('Put User - Controller')
        user_id = request.args['userId']
        request_body = request.get_json()
        service = Service()
        return service.update_user(user_id=int(user_id), data=request_body)

    @staticmethod
    def delete():
        print('Delete User - Controller')
        user_id = request.args['userId']
        service = Service()
        return service.delete_user(user_id=int(user_id))


class Task(Resource):

    @staticmethod
    def post(user_id):
        print('Post Task - Controller')
        service = Service()
        request_body = request.get_json()
        return service.add_task(user_id=int(user_id), data=request_body)

    @staticmethod
    def put(user_id):
        print('Put Task - Controller')
        task_id = request.args['taskId']
        service = Service()
        request_body = request.get_json()
        return service.update_task(user_id=int(user_id), task_id=int(task_id), data=request_body)

    @staticmethod
    def delete(user_id):
        print('Delete Task - Controller')
        service = Service()
        try:
            task_id = request.args['taskId']
            return service.delete_task(user_id=int(user_id), task_id=int(task_id))
        except:
            return service.delete_all_tasks(user_id=int(user_id))

    @staticmethod
    def get(user_id):
        print('Get Task - Controller')
        service = Service()
        try:
            task_id = request.args['taskId']
            return service.get_user_task(user_id=int(user_id), task_id=int(task_id))
        except:
            return service.get_users_alltasks(user_id=int(user_id))


class Start(Resource):
    @staticmethod
    def get():
        return "Welcome to ToDo-Manager"


class LoginVerification(Resource):
    @staticmethod
    def get():
        service = Service()
        email = request.args['email']
        password = request.args['password']
        return service.login_verification(email=email, password=password)


api.add_resource(Start, '/')
api.add_resource(User, '/user')
api.add_resource(Task, '/user/<int:user_id>/tasks')
api.add_resource(LoginVerification, '/verify-user')

if __name__ == '__main__':
    app.run()