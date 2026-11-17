from sqlalchemy import text
from app import create_app
from app.extensions import db

app = create_app()
with app.app_context():
    print(db.session.execute(text("SELECT VERSION()")).scalar())