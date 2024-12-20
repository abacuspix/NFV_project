# coding:utf-8
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# default flask logging handler pushes messages into the console
# works DEBUG mode only
app.config['LOG_FILENAME'] = 'project_name.log'
# log warning messages or higher
app.config['LOG_LEVEL'] = logging.WARNING
app.config['ADMINS'] = ['you@domain.com']
app.config['ENV'] = 'production'


def configure_file_logger(app, filename, level=logging.DEBUG):
    # special file handler that overwrites logging file after
    file_handler = RotatingFileHandler(
        filename=filename,
        encoding='utf-8',  # cool kids use utf-8
        maxBytes=1024 * 1024 * 32,  # we don't want super huge log files ...
        backupCount=3  # keep up to 3 old log files before rolling over
    )

    # define how our log messages should look like
    formatter = logging.Formatter(u"%(asctime)s %(levelname)s\t: %(message)s")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    app.logger.addHandler(file_handler)


def configure_mail_logger(app, level=logging.ERROR):
    """
    Notify admins by e-mail in case of error for immediate action
    based on from http://flask.pocoo.org/docs/0.10/errorhandling/#error-mails
    """

    if app.config['ENV'] == 'production':
        from logging.handlers import SMTPHandler

        mail_handler = SMTPHandler(
            '127.0.0.1',
            'server-error@domain.com',
            app.config['ADMINS'], 'YourApplication Failed')

        mail_handler.setLevel(level)
        app.logger.addHandler(mail_handler)


if __name__ == '__main__':
    app.debug = True
    configure_file_logger(app, 'project_name.dev.log')
    configure_mail_logger(app)
    app.run()
