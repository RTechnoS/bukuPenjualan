import sqlite3 as sqlite

class DB:
	def __init__(self, dbLok='../testing.db'):
		try:
		#if 1+1 ==2:
			self.__connect = sqlite.connect(dbLok, check_same_thread=False)
			self.__cur = self.__connect.cursor()

			#self.__cur.row_factory = self.dict_factory
			
			self.__status = True
		except:
			print('Database Disconnect !!')
			#logging.exception('Database Disconnect !!')
			self.status = False

	@property
	def getConnect(self):
		return self.__connect

	@property
	def getCur(self):
		return self.__cur

	def to_dict_index(self, data):
		h = {}
		for i in data:
			h[i[0]] = i
		return h

	# def dict_factory(self, cursor, row):
	# 	d = {}
	# 	for idx, col in enumerate(cursor.description):
	# 		d[col[0]] = row[idx]
	# 	return d

	def getStore(self, q=False):
		if q:
			self.__cur.execute(f'SELECT {q} from store')
		else:
			self.__cur.execute(f'SELECT * from store')
		list_store = self.__cur.fetchall()
		return list_store

	def getVia(self, id_store=False):
		if id_store:
			self.__cur.execute(f'SELECT * from via where id_store={id_store}')
		else:
			self.__cur.execute(f'SELECT * from via')

		list_via = self.__cur.fetchall()
		return list_via

	def getProduct_type(self, id_store=False):
		self.__cur.row_factory = self.dict_factory
		if id_store:
			self.__cur.execute(f'SELECT * from product_type where id_store={id_store}')
		else:
			self.__cur.execute(f'SELECT * from product_type')


		list_product_type = self.__cur.fetchall()
		return list_product_type

	def getProduct(self, id_product_type=False):
		if id_product_type:
			self.__cur.execute(f'SELECT * from product where id_product_type={id_product_type}')
		else:
			self.__cur.execute(f'SELECT * from product')

		list_product = self.to_dict_index(self.__cur.fetchall())
		return list_product


	def testJoinProduct(self, id_store=2):
		self.__cur.execute('SELECT product_type.id_store, product_type.name, product.name, product.price, product.note FROM product_type INNER JOIN product ON product_type.id_product_type = product.id_product_type')
		return self.__cur.fetchall()


DBCONNECT = DB()

p = DBCONNECT.getProduct(1)
print(p)
