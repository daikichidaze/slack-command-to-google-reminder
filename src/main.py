import os

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from google_reminder_api_wrapper import ReminderApi

import db

app = FastAPI()
manager = LoginManager(os.environ['SECRET'], token_url='/auth/token')


@app.get("/")
def index(user=Depends(manager)):
    return {"message": "API for google reminder"}


@app.post("/set-remainder")
async def set_remainder(text: str, dt: str):
    # set_env_val(auth)
    try:
        api = ReminderApi()
        new_reminder = api.create(text, dt)
    except:
        raise {"message": "Reminder setting error"}
    return {"message": "Reminder added"}

# For user auth


@manager.user_loader()
def load_user(email: str):
    user = db.db.get(email)
    return user


@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    # we are using the same function to retrieve the user
    user = load_user(email)
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
