from google_reminder_api_wrapper import ReminderApi
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"test": "t"}


@app.post("/set-remainder")
async def set_remainder(text: str, dt: str):
    try:
        api = ReminderApi()
        new_reminder = api.create(text, dt)
        print(dt)
    except:
        return {"result": "Google reminder setting error"}
    return {"text": "ok"}
