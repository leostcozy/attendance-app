from .settings import *
from pathlib import Path

SECRET_KEY='5(3u5_(f%=wda@^yk4xw%))mk+*89t^c_6h(c*%bu$qt7*9art'
DEBUG=True
DATABASE_URL='mysql://root:leo08178@localhost:3306/attendance-db'
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "attendance-db",
        "USER": "root",
        "PASSWORD": "leo08178",
        "HOST": "localhost",
        "PORT": "3306"
    }
}
BASE_DIR = Path(__file__).resolve().parent.parent