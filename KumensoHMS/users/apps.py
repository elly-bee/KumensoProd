from django.apps import AppConfig
#from .signals import *


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


    def ready(self):
         from . import signals