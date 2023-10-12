import os

from dotenv import load_dotenv
load_dotenv()

class Config(object):
    DEBUG = False,
    SECRET_KEY = 'secret_xxx',
    PONY = {'provider' : os.getenv('provider'), 
                'user' : os.getenv('user'), 
                'password' : os.getenv('password'), 
                'host' : os.getenv('host'), 
                'database' : os.getenv('database')
            }

