try:
  goods = []
  print("importing users...")
  from database import Users
  print("users good")

  print("importing config")
  from config import app, db
  print("config good")

  print("importing signup routes")
  import signup_login.signup_routes
  print("routes good")

  print("checcking service")
  import signup_login.signup_service 
  print("services good")

except Exception as e:
  print(f"THERE A ERROR GRABBING DATA: {e}")
  import traceback
  traceback.print_exc()

  
