import bcrypt


__author__ = 'Ricardo'
__version__ = '0.1'
__all__ = ['verify_password', 'get_password_hash']


def verify_password(plain_password:str, hashed_password:str):

    plain_password = plain_password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')

    return bcrypt.checkpw(plain_password, hashed_password)

def get_password_hash(password:str):
    
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password, salt).decode('utf-8')
