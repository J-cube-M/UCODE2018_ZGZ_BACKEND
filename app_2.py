from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

from database import db
from models import Map
from routes import route

def create_app():
	app = Flask(__name__)
	app.config.from_object('config')
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gyoeqjtvlaanwq:3d3a9ae250ad8c4456aeefd5d6f84c25b91fea2316a92d554b47cffe1bdc2838@ec2-54-221-234-62.compute-1.amazonaws.com:5432/d3g9oa6mck8psa'
	
	app.app_context().push()
	db.init_app(app)

	app.register_blueprint(route, url_prefix='')

	return app

app = create_app()

if __name__ == '__main__':
	app.run(debug=False, use_reloader=True)