"""
This module instantiates an instance of flask and SQLalchemy
database, integrates the applications configuration, and
implements AWS X-Ray middleware.
"""

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config["DEBUG"] = True

xray_recorder.configure(service="app")
XRayMiddleware(app, xray_recorder)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = "login"

from app import models, routes  # noqa: E402, F401
