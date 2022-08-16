""" This is the logger of the app"""

from flask import Flask

app = Flask(__name__)

logger = app.logger
