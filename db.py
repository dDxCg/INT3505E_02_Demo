from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

db = SQLAlchemy()
REFRESH_STORE = {}
ACCESS_JTI_BLACKLIST = set()
mongo = PyMongo()

