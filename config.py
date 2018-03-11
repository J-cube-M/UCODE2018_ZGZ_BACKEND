import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgres://gyoeqjtvlaanwq:3d3a9ae250ad8c4456aeefd5d6f84c25b91fea2316a92d554b47cffe1bdc2838@ec2-54-221-234-62.compute-1.amazonaws.com:5432/d3g9oa6mck8psa'