from fastapi import FastAPI, Request, HTTPException
from helpers import verify_password, hash_data_salt
from database import DB
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse

app = FastAPI(title='PasswordManager', debug=False)

db_instance = DB("passMan")

USER_EXISTS = "User with this name exists"
OK = "Success"

@app.post("/retrieve_data")
async def post_data(request: Request):
    """ if authenticated successfully, return the encrypted data"""
    db_instance.check_content()
    json_data = await request.json()
    row = db_instance.select_all_from_user_data(json_data["username"])
    if verify_password(row[2], row[1], json_data["password"]):
        return {'data': row[3], 'nonce': row[4]}
    else:
        raise HTTPException(status_code=403, detail="Invalid credentials")

@app.post("/register")
async def post_register(request: Request):
    """ performs a registration"""
    json_data = await request.json()
    if not db_instance.check_if_user_exists(json_data["username"]):
        salt, hash = hash_data_salt(json_data["password"])
        db_instance.insert_new_user(json_data["username"], hash, salt)
        db_instance.check_content()
        return JSONResponse(content=OK, status_code=200)
    else:
        return JSONResponse(content=USER_EXISTS, status_code=409)

@app.put("/update")
async def update_data(request: Request):
    """ update user data"""
    json_data = await request.json()
    row = db_instance.select_all_from_user_data(json_data["username"])
    if verify_password(salt=row[2], password_hash=row[1], password=json_data["password"]):
        db_instance.update_user_data(username=json_data["username"], encrypted_data=json_data["data"], nonce=json_data["nonce"])
    else:
        raise HTTPException(status_code=403, detail="Invalid credentials")
