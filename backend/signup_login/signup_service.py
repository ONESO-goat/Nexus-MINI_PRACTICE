from flask import session
from werkzeug.security import generate_password_hash
from backend.database import Users

SPECIAL_CHARACTERS = "!@#$%^&*()_+=-~`[]\{}|/.,<>?"
def hash_password(password):
  return generate_password_hash(password)


def username_length(username):
  if not username:
    return False
  username = username.lower()
  
  if len(username) < 3 or len(username) > 60:
    return False
  
  return True


def validate_user(username):
  username = username.lower()
  if not username:
    return False, "error when grabbing the user"

  user = Users.query.filter_by(username=username).first()
  if user:
    return False, "user already exist"
  
  if username.isdigit():
    return False, "username cannot be number only"
  
  if user in session:
    return False, "User is already logged into the system"
  
  if not username_length(username):
    return False, "username length is out of range."
  

  
  return True, "the username is available"



def validate_password(password):

  if not password:
    return False, "Error when grabbing the passsword"
  
  if len(password) < 8 or len(password) > 120:
    return False, f'password is out of range: {len(password)}'
  
  has_special = any(char in SPECIAL_CHARACTERS for char in password)
  if not has_special:
    return False, "Please include atleast 1 special character."
  

  return True, "Password is valid for production"

  
  
