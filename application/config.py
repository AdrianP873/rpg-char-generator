import os

""" __file__ refers to the module loaded by Python. In my case it will load application.py.
Therefore we are getting the absolute path of the directory where application.py is.
I could hardcore application.py instead of __file__ however this gives greater flexibility"""  # noqa: E501
basedir = os.path.abspath(os.path.dirname(__file__))


# Define configuration settings as class variables inside a config class
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "my secret key"

    # Set database location
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "rpg.db")

    # Signal application everytime change is about to be made to DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
