import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_NAME = os.environ['APP_NAME']
    SECRET_KEY = os.environ['SECRET_KEY']
    ALCHEMICAL_DATABASE_URL = os.environ['ALCHEMICAL_DATABASE_URL']
