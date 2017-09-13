from flask import Flask
import logging

class Config(object):
    LOG_LEVEL = logging.WARNING

app = Flask(__name__)
app.config.from_object(Config)
app.run()