from fastapi import FastAPI
from routes import router
from models import create_user_table

app = FastAPI()

create_user_table() #auto create the table

app.include_router(router)
