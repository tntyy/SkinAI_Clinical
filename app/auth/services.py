from werkzeug.security import check_password_hash

from app.auth.repositories import get_user_by_username


def authenticate(username, password):

    user = get_user_by_username(username)

    if not user:
        return None

    if not check_password_hash(user.password_hash, password):
        return None

    return user