import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL",
                                       f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'test.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DISABLE_ROLE_CHECK = True
