# config.py

import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "WCE2025")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///college_placement.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
