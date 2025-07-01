from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from routes import router
from database import engine, Base


app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(router)
templates = Jinja2Templates(directory="templates")
