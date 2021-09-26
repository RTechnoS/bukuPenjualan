import datetime
import sqlite3 as sqlite
from datetime import datetime
import logging
import sys

logging.basicConfig(format='[%(asctime)s] %(levelname)-8s: %(message)s',datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO, handlers=[logging.FileHandler('./log.log'), logging.StreamHandler(sys.stdout)])

def to_dict_index(data):
	h = {}
	for i in data:
		h[i[0]] = i
	return h

def f_time(f_jam = "%H:%M:%S", f_hari = '%Y-%m-%d'):
	waktu = datetime.now()
	return (waktu.strftime(f_jam), waktu.strftime(f_hari)) #jam - hari

class DB:
	def __init__(self, dbLok='testing.db'):
		try:
			self.__connect = sqlite.connect(dbLok, check_same_thread=False)
			self.__cur = self.__connect.cursor()
			self.__status = True
		except:
			logging.exception('Database Disconnect !!')
			self.status = False

	@property
	def getConnect(self):
		return self.__connect

	@property
	def getCur(self):
		return self.__cur

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

		list_product = self.__cur.fetchall()
		return list_product


	def testJoinProduct(self, id_store=2):
		self.__cur.execute('SELECT product_type.id_store, product_type.name, product.name, product.price, product.note FROM product_type INNER JOIN product ON product_type.id_product_type = product.id_product_type')
		return self.__cur.fetchall()

	def submitHistory(self, id_store, id_product_type, id_product, id_via, price, time, amount, seller):
		self.__cur.execute(f'SELECT price from product where id_product={id_product} LIMIT 1')
		get_price = self.__cur.fetchone()
		if get_price != None:
			if price == get_price[0]*amount:
				price = get_price[0]*amount
				try:
					q = f'INSERT INTO history(id_store, id_product_type, id_product, amount, id_via, price, seller, time) VALUES ({id_store}, {id_product_type}, {id_product}, {amount}, {id_via}, {price}, "{seller}", "{time} {f_time()[0]}")'
					self.__cur.execute(q)
					self.__connect.commit()
					hasil = {'status':True, 'pesan':'Succes Ditambahkan', 'time':f"{time} {f_time()[0]}", 'price':price}
				except:
					logging.exception('Database Error')
					hasil = {'status':False, 'pesan':'Database error. Please wait', 'code':3}
			else:
				logging.warning(f'Input tidak sesuai dengan harga database | {price} != { get_price[0]*amount}')
				hasil = {'status':False, 'pesan':'Harga tidak sesuai, silahkan pilih ulang produk', 'code':1}
		else:
			logging.warning('Produk tidak ditemukan')
			hasil = {'status':False, 'pesan':'Produk tidak ada atau telah habis', 'code':2}

		return hasil


class Main(DB):
	def __init__(self, dbLok='testing.db'):
		super().__init__(dbLok)







