import jwt
from settings import JWT_SECRET_KEY
from datetime import datetime, timedelta
from flask import json, Response, request, g
from functools import wraps
from ..models.UserModel import UserModel


class Auth:
    """
    Authentication Class
    """
    @staticmethod
    def generate_token(user_id):
        """
        Generate Token Method
        :param user_id:
        :return:
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                JWT_SECRET_KEY,
                'HS256'
            ).decode('utf-8')
        except Exception as e:
            response = {'error': 'error in generating user token'}
            return custom_response(response, 400)

    @staticmethod
    def decode_token(token):
        """
        Decode token method
        :param token:
        :return:
        """

        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY)
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignature as e1:
            re['error'] = {'message': 'token expired, please login again'}
            return re
        except jwt.InvalidTokenError as e2:
            re['error'] = {'message': 'invalid token, please try again with a new token'}
            return re

    @staticmethod
    def auth_required(func):
        """
        Auth decorator
        """
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                response = {'error': 'Authentication token is not available, please login to get one'}
                return custom_response(response, 400)
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)
            if data['error']:
                response = data['error']
                return custom_response(response, 400)

            user_id = data['data']['user_id']
            check_user = UserModel.get_one_user(user_id)
            if not check_user:
                response = {'error': 'user does not exist, invalid token'}
                return custom_response(response, 400)
            g.user = {'id': user_id}
            return func(*args, **kwargs)
        return decorated_auth


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
