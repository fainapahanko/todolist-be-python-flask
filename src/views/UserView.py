from flask import request, json, Response, Blueprint, g

from ..models.UserModel import UserModel, UserSchema
from ..shared.Auth import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()


@user_api.route('/', methods=['POST'])
def create_user():
    """
    Create Use Func
    :return:
    """
    req_data = request.get_json()
    data = user_schema.load(req_data)
    print(data)

    if not data:
        message = {'error': 'Please check all the fields'}
        return custom_response(message, 400)

    user_in_db = UserModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = {'error': 'User already exist, please supply another email address'}
        return custom_response(message, 400)

    user = UserModel(data)
    user.save()

    ser_data = user_schema.dump(user)
    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 201)


@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    data = user_schema.load(req_data, partial=True)

    if not data:
        message = {'error': 'Please check all the fields'}
        return custom_response(message, 400)

    if not data.get('email') or not data.get('password'):
        response = {'error': 'you need email and password to sign in'}
        return custom_response(response, 400)

    user = UserModel.get_user_by_email(data.get('email'))

    if not user:
        response = {'error': 'invalid credentials'}
        return custom_response(response, 400)

    if not user.check_hash(data.get('password')):
        response = {'error': 'invalid credentials'}
        return custom_response(response, 400)

    ser_data = user_schema.dump(user)

    token = Auth.generate_token(ser_data.get('id'))

    response = {'jwt_token': token}
    return custom_response(response, 200)


@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    users = UserModel.get_all_users()
    ser_users = user_schema.dump(users, many=True)
    response = {'total': len(ser_users), 'users': ser_users}
    return custom_response(response, 200)


@user_api.route('/me', methods=['GET', 'PUT', 'DELETE'])
@Auth.auth_required
def authenticated_manipulations():
    user = UserModel.get_one_user(g.user.get('id'))
    if user:
        if request.method == 'GET':
            ser_user = user_schema.dump(user)
            return ser_user
        elif request.method == 'DELETE':
            user.delete()
            return custom_response({'response': 'Was deleted successfully'}, 200)
        elif request.method == 'PUT':
            data = request.get_json()
            user.update(data)
            ser_user = user_schema.dump(user)
            return ser_user
    else:
        response = {'error': 'Something went wrong. Please check if token if valid'}
        return custom_response(response, 400)


def custom_response(res, status_code):
    """
    Custom response
    :param res:
    :param status_code:
    :return:
    """
    return Response(
        mimetype='applications/json',
        response=json.dumps(res),
        status=status_code
    )