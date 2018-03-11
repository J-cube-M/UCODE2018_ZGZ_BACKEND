from flask.blueprints import Blueprint
from flask import request
import json

from models import Map, Cell, Product, User

route = Blueprint('route', __name__)

@route.route('/')
def default():
	return """
	<h1>Hello heroku</h1>

	<img src="http://loremflickr.com/600/400">
	"""
@route.route('/getMap')
def getMap():
	idMap = int(request.args.get('id', default=-1))

	if idMap < 0:
		return json.dumps({'error': 'Id incorrecta o no suministrada'})
	
	map_ = Map.query.filter_by(id=idMap).first()
	if map_ == None:
		return json.dumps({'error': 'No existe ningún mapa con dicha id'})

	# Return all cells
	cells = Cell.query.filter_by(map=idMap).all()
	cells_ = list(map(lambda x : x.asDict(), cells))

	zones_ = list(map(lambda x : x.asDict(), map_.zones))

	return json.dumps({'map': map_.asDict(), 'cells' : cells_, 'zones' : zones_})

@route.route('/getProductInfo')
def getProductInfo():
	idProduct = int(request.args.get('id', default=-1))

	if idProduct < 0:
		return json.dumps({'error': 'Id incorrecta o no suministrada'})

	product = Product.query.filter_by(id=idProduct).first()

	if product == None:
		return json.dumps({'error': 'No existe ningún producto con dicha id'})

	return json.dumps(product.asDict())

@route.route('/allProducts')
def allProducts():
	products = Product.query.all()
	products_ = list(map(lambda x : x.asDict(), products))
	return json.dumps(products_)

@route.route('/getRecomendations')
def getRecomendations():
	nameUser = request.args.get('name', default="")
	if nameUser == "":
		return json.dumps({'error': 'Nombre incorrecto o no suministrado'})

	user = User.query.filter_by(name=nameUser).first()
	if user == None:
		return json.dumps({'error': 'No existe ningún usuario con dicho nombre'})

	return json.dumps(user.asDict())
		