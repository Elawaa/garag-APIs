from app import app
from db import db
import data

db.init_app(data,app)

@app.before_first_request
def create_tables():
    db.create_all()