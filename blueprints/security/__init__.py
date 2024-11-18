import os
from flask import Blueprint
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

bp = Blueprint('security', __name__)

login_serializer = URLSafeTimedSerializer(os.environ['SECRET_KEY'])


def generate_login_token(user_id):
    return login_serializer.dumps(user_id, salt=os.environ['SECRET_KEY'])


def verify_login_token(token, max_age=2592000):  # 30 days in seconds
    try:
        user_id = login_serializer.loads(token, max_age=max_age, salt=os.environ['SECRET_KEY'])
    except (BadSignature, SignatureExpired):
        return None
    return user_id


from blueprints.security import routes
