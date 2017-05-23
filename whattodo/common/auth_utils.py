from flask_bcrypt import Bcrypt
from whattodo.models.user import User


bcrypt = Bcrypt()


def authenticate(username, password):
    user = User.query.filter(User.email == username).scalar()
    if bcrypt.check_password_hash(user.password, password):
        return user


def identity(payload):
    return User.query.filter(User.id == payload['identity']).scalar()
