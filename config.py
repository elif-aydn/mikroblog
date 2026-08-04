import os


basedir = os.path.abspath(os.path.dirname(__file__))


def env_flag(name):
    value = os.environ.get(name, '')
    return value.strip().lower() in (
        '1',
        'true',
        'yes',
        'on'
    )


class Config:
    SECRET_KEY = (
        os.environ.get('SECRET_KEY')
        or 'microblog-local-development-secret-key-2026'
    )

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or 'sqlite:///'
        + os.path.join(basedir, 'app.db')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = (
        os.environ.get('MAIL_SERVER')
        or '127.0.0.1'
    )

    MAIL_PORT = int(
        os.environ.get('MAIL_PORT')
        or 8025
    )

    MAIL_USE_TLS = env_flag('MAIL_USE_TLS')
    MAIL_USE_SSL = env_flag('MAIL_USE_SSL')

    MAIL_USERNAME = os.environ.get(
        'MAIL_USERNAME'
    )

    MAIL_PASSWORD = os.environ.get(
        'MAIL_PASSWORD'
    )

    ADMINS = [
        'your-email@example.com'
    ]

    POSTS_PER_PAGE = 25

    LANGUAGES = ['en', 'es']

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')