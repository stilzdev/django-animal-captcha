import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'django-animal-captcha.db'), }}
LANGUAGE_CODE = 'en'
SECRET_KEY = 'empty'
ROOT_URLCONF = 'testproject.urls'
TEMPLATE_DIRS = ('animaltest/templates', )
INSTALLED_APPS = ('django.contrib.contenttypes', 'animalcaptcha', 'testproject', )
