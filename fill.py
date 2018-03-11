
from models import Map, Cell, Product, Zone, User

def addMapWithCells(db, mapData, zonesRadius, cellList):
	map_ = Map(id=mapData[0], name=mapData[1], maxX=mapData[2], maxY=mapData[3])
	db.session.add(map_)
	db.session.flush()

	for i in range(0, len(cellList)):
		for j in range(0, len(cellList[0])):
			if cellList[i][j] == 0:
				continue

			r = 0 if (cellList[i][j] == -1 or cellList[i][j] == 0) else zonesRadius[cellList[i][j]]
			cell = Cell(map=mapData[0], value=cellList[i][j], radius=r, posX=j, posY=i)
			db.session.add(cell)
			db.session.flush()

	db.session.commit()

	print ('Added map {0}'.format(mapData[1]))

def addZones(db, zonesList):
	res = []
	for zone in zonesList:
		z = Zone(name=zone[0])

		map_ = Map.query.filter_by(id=zone[1]).first()
		if map_ != None:
			print ('Added to {0} zone {1}'.format(map_.name, z.name))
			map_.zones.append(z)
			db.session.add(map_)

		db.session.add(z)
		db.session.flush()
		res.append(z.id)

		print ('Added zone {0}'.format(zone[0]))

	db.session.commit()
	return res

def addProducts(db, zones_id, productsList):
	for product in productsList:
		p = Product(name=product[0], description=product[1], zone=zones_id[product[3]], image=product[2])
		db.session.add(p)
		db.session.flush()

		print ('Added product {0}'.format(product[0]))

	db.session.commit()

def addUsers(db, users):
	for user in users:
		u = User(name=user)
		db.session.add(u)
		db.session.flush()
		print('Added user {0}'.format(user))

	db.session.commit()


def fillDB(db):
	print (' -- Filling maps --')
	addMapWithCells(db, (0, 'Shop test 1', 6, 5), \
					{2 : 2, 3 : 2}, \
					[[-1, -1, -1, -1, -1, -1], \
					 [-1,  2,  0,  0,  0, -1], \
					 [-1,  0,  0,  0,  0, -1], \
					 [-1,  0,  0,  0,  3, -1], \
					 [-1, -1, -1, -1, -1, -1]])

	addMapWithCells(db, (1, 'Shop test 2', 8, 8), \
					{2 : 3, 3 : 2, 4 : 2}, \
					[[-1, -1, -1, -1, -1, -1, -1, -1], \
					 [-1,  4,  0,  0, -1,  0,  0, -1], \
					 [-1,  0,  0,  0, -1,  2,  0, -1], \
					 [-1,  0,  0,  0, -1,  0,  0, -1], \
					 [-1,  0,  0,  3, -1,  0,  0, -1], \
					 [-1,  0,  0,  0, -1,  0,  0, -1], \
					 [-1,  0,  0,  0,  0,  0,  0, -1], \
					 [-1,  0,  0, -1, -1, -1, -1, -1]])

	print (' -- Filling zones --')
	ids = addZones(db, [('Calzado', 1), ('Camisetas', 1), ('Pantalones', 1), ('Kimonos', 2), ('Equipamiento', 3)])

	print (' -- Filling products --')
	#addProducts(db, ids, [('Zapatilla Predator', 'Muy top', 'http://google.com'), \
	#				      ('Camiseta manga corta', 'Muy corta', 'http://google.es')])

	addProducts(db, ids, [('Zapatillas futbol', 'Predator style', 'url', 0), \
						  ('Camiste basket', 'Lebron james approved', 'url', 1), \
						  ('Bañador masculino', 'Feel like a dolphin', 'url', 2), \
						  ('Dobok', 'Hit harder', 'url', 3), \
						  ('Balon de futbol', 'Balls', 'url', 4)])

	print (' -- Filling users --')
	addUsers(db, ['Mike', 'Turtle', 'Juanjo'])

	db.session.commit()
