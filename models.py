from database import db

from sqlalchemy.dialects.postgresql import JSON

maps_help = db.Table('maps_help', db.Model.metadata,
			db.Column('map_id', db.Integer, db.ForeignKey('maps.id'), primary_key=True),
			db.Column('zone_id', db.Integer, db.ForeignKey('zones.id'), primary_key=True))

class Map(db.Model):
	__tablename__ = 'maps'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True)
	maxX = db.Column(db.Integer)
	maxY = db.Column(db.Integer)
	zones = db.relationship('Zone', secondary=maps_help)

	'''def __init__(self, id, name, maxX, maxY):
		self.id = id
		self.name = name
		self.maxX = maxX
		self.maxY = maxY'''
	def asDict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __repr__(self):
		return '<id {0}'.format(self.id)

class Cell(db.Model):
	__tablename__ = 'cells'

	id = db.Column(db.Integer, primary_key=True)
	map = db.Column(db.Integer, db.ForeignKey('maps.id'))
	value = db.Column(db.Integer)
	radius = db.Column(db.Integer, nullable=True)
	posX = db.Column(db.Integer)
	posY = db.Column(db.Integer)

	'''def __init__(self, id, map, value, radius):
		self.id = id
		self.map = maps_help
		self.value = value
		self.radius = radius'''

	def asDict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Product(db.Model):
	__tablename__ = 'products'

	id = db.Column(db.Integer, 
                 db.Sequence('product_id_seq', start=1, increment=1),   
                 primary_key=True)
	name = db.Column(db.String(50))
	image = db.Column(db.String(100))
	description = db.Column(db.String(200))
	zone = db.Column(db.Integer, db.ForeignKey('zones.id'))

	'''def __init__(self, id, name, image, description, zone):
		self.id = id
		self.name = name
		self.image = image
		self.description = description
		self.zone = zone'''

	def asDict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Zone(db.Model):
	__tablename__ = 'zones'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	#maps = db.relationship('Maps', secondary=maps_help)

	'''def __init__(self, id, name, maps):
		self.id = id
		self.name = name
		self.maps = maps'''

	def asDict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, 
                 db.Sequence('user_id_seq', start=1, increment=1),   
                 primary_key=True)
	name = db.Column(db.String(50))

	def asDict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class CF(db.Model):
	__tablename__ = 'cfs'

	id = db.Column(db.Integer, primary_key=True)
	data = db.Column(db.PickleType)

	def asDict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	'''def __init__(self, id, data):
		self.id = id
		self.data = data'''
