from flask.blueprints import Blueprint
from flask import request
import json
import re

from models import Map, Cell, Product, User

from colaborativeFiltering import colaborativeSystem

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
	idZone = int(request.args.get('zone', default=-1))
	if idZone == -1:
		products = Product.query.all()
		products_ = list(map(lambda x : x.asDict(), products))
		return json.dumps(products_)
	else:
		products = Product.query.filter_by(zone=idZone).all()
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

	scores = colaborativeSystem.rateProductsForUser(user.id-1)

	res = []
	for id in scores:
		p = Product.query.filter_by(id=id+1).first()
		if p != None:
			res.append(p.asDict())

	return json.dumps(res)

@route.route('/updateSystem')
def updateSystem():
	nameUser = request.args.get('name', default="")
	if nameUser == "":
		return json.dumps({'error': 'Nombre incorrecto o no suministrado'})
	user = User.query.filter_by(name=nameUser).first()
	if user == None:
		return json.dumps({'error': 'El usuario no existe'})

	idProduct = int(request.args.get('id', default=-1))
	if idProduct == -1:
		return json.dumps({'error': 'Id incorrecta o no suministrada'})

	score = int(request.args.get('score', default=0))

	colaborativeSystem.updateSystem(productId=idProduct-1,userId=user.id-1,score=score)

	return json.dumps(True)

@route.route('/search')
def search():
	query = request.args.get('query', default="----")
	if query == "":
		return json.dumps({'error': 'No hay query'})

	results = Product.query.all()

	res = []

	regex = re.compile(query)
	for result in results:
		if result.name.lower().find(query.lower()) != -1:
			res.append(result.asDict())

	return json.dumps(res)
		