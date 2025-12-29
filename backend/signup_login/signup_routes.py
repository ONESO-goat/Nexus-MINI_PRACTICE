from backend.config import app, db
from flask import request,session, jsonify 
from backend.database import Users
from datetime import datetime 
import uuid
from sqlalchemy.orm import joinedload, selectinload
from werkzeug.security import check_password_hash
from backend.signup_login.signup_service import validate_user, validate_password, hash_password

@app.route("/", methods=["GET"])
def get_users():
  users = (
    Users.query
    .options(joinedload(Users.created_projects), 
             selectinload(Users.made_tasks))
    .all()
    )
  user_in_application = []
  for user in users:
    user_in_application.append({
      "id": user.id,
      "username": user.username,
      "password": user.password,
      "join_date": user.join_date
    })

  return jsonify({"user": user_in_application})


@app.route("/signup", methods=["POST"])
def signup():
  data = request.get_json()
  if not data:
    return jsonify({"error": "error when grabiing the data"}), 400
  
  username = data.get("username")
  password = data.get("password")
  if not username or not password:
    return jsonify({"error":'error when grabbing the username and user'}), 400
  
  valid, error = validate_user(username)
  if not valid:
    return jsonify({"error": error}), 400
  
  valid, error = validate_password(password)
  if not valid:
    return jsonify({"error": error}), 400
  
  try:
    encryted_p = hash_password(password)
  except ValueError:
    return jsonify({"error": "unexpected error when creating the user"}), 500
  
  new_user = Users(
    id=str(uuid.uuid4()),
    username=username,
    password=encryted_p,
    join_date=datetime.utcnow()
  )

  try:
      db.session.add(new_user)
      db.session.commit()
      return jsonify({"message": "user successfuly created"}), 201
  except Exception as e:
      db.session.rollback()
      print(f"Database error: {str(e)}")  # Add this to see the actual error
      
      # Check if it's a duplicate username error
      if "UNIQUE constraint failed" in str(e) or "Duplicate entry" in str(e):
          return jsonify({"error": "Username already exists"}), 400
      
      return jsonify({"error": "Error creating user"}), 500


@app.route("/login", methods=["POST"])
def login():
  data = request.get_json()
  if not data:
    return jsonify({"error": "error grabbing json data"}), 404
  
  username = data.get("username")
  password  =data.get("password")
  if not username or not password:
    return jsonify({"error":"there was an error when accesing the user's input"}), 400

  user = Users.query.fliter_by(username=username).first()
  if not user:
    return jsonify({"error": "the user doesn't exist"}), 404
  
  if not check_password_hash(user.password, password):
    return jsonify({"error": "invalid password or username"}), 401


  session["user_id"] = str(user.id)
  session["username"] = user.username
  return jsonify({"message": "user sucessfully logs in",
                  "username": user.id})


@app.route("/logout", methods=["POST"])
def logout():
  try:
    session.clear()
    return jsonify({'message': "user successfully logged out"}), 200
  
  except Exception as e:
    
    return jsonify({"error":"error when trying to log user out", "details": e}), 500



  

  

  

