from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
from mars_planet_library import settings

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.SECURITY_SETTINGS.get("APP_SECRET_KEY")
bcrypt = Bcrypt(app)
engine = create_engine(settings.SECURITY_SETTINGS.get("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
login_manager = LoginManager(app)

from mars_planet_library import routes
