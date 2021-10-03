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

	def __runQuery(self, q='', fetch='all', method=1):
		# method 1 = select, 2 = insert
		hasil = False
		if q != '':
			try:
				self.__cur.execute(q)
				if method == 1:
					if fetch == 'all':
						hasil = self.__cur.fetchall()
					else:
						hasil = self.__cur.fetchone()
				
				elif method == 2:
					self.__connect.commit()
					hasil = True
			except:
				hasil = False

			return hasil


	def getStore(self, q=False):
		if q=='singkat':
			list_store = self.__runQuery(f'SELECT id_store,name from store')
		else:
			list_store = self.__runQuery(f'SELECT * from store')
		return list_store

	def getVia(self, id_store=False):
		try:
			if id_store:
				hasil = self.__runQuery(f'SELECT * from via where id_store={int(id_store)}')
			else:
				hasil = self.__runQuery(f'SELECT * from via')
		except:
			logging.exception('Terdeteksi melakukan percobaan SQLI')
			hasil = []
		return hasil

	def getProduct_type(self, id_store=False):
		try:
			if id_store:
				hasil = self.__runQuery(f'SELECT * from product_type where id_store={int(id_store)}')
			else:
				hasil = self.__runQuery(f'SELECT * from product_type')
		except:
			logging.exception('Terdeteksi melakukan percobaan SQLI')
			hasil = []

		return hasil

	def getProduct(self, id_product_type=False):
		try:
			if id_product_type:
				hasil = self.__runQuery(f'SELECT * from product where id_product_type={int(id_product_type)}')
			else:
				hasil = self.__runQuery(f'SELECT * from product')
		except:
			logging.exception('Terdeteksi melakukan percobaan SQLI')
			hasil = []

		return hasil

	def submitHistory(self, id_store, id_product_type, id_product, id_via, price, time, amount, seller):
		error = False
		try:
			int(id_store)
			int(id_product_type)
			int(id_product)
			int(id_via)
			int(price)
			int(amount)
			seller = seller[:15]
			
			if len(time) != 10:
				error = True

		except:
			error = True
			logging.exception('Terdeteksi melakukan percobaan SQLI')

		if error == False:
			get_price = self.__runQuery(f'SELECT price from product where id_product={id_product} LIMIT 1', fetch='one')
			if get_price != None:
				if price == get_price[0]*amount:
					price = get_price[0]*amount

					q = self.__runQuery(f'INSERT INTO history(id_store, id_product_type, id_product, amount, id_via, price, seller, time) VALUES ({id_store}, {id_product_type}, {id_product}, {amount}, {id_via}, {price}, "{seller}", "{time} {f_time()[0]}")', method=2)
					if q:
						hasil = {'status':True, 'pesan':'Succes Ditambahkan', 'time':f"{time} {f_time()[0]}", 'price':price}
					else:
						logging.exception('Database Error')
						hasil = {'status':False, 'pesan':'Database error. Please wait', 'code':3}
					
				else:
					logging.warning(f'Input tidak sesuai dengan harga database | {price} != { get_price[0]*amount}')
					hasil = {'status':False, 'pesan':'Harga tidak sesuai, silahkan pilih ulang produk', 'code':1}
			else:
				logging.warning('Produk tidak ditemukan')
				hasil = {'status':False, 'pesan':'Produk tidak ada atau telah habis', 'code':2}
		else:
			hasil = {'status':False, 'pesan':'Data yang di inputkan salah', 'error':4}

		return hasil

	def getHistory(self, data):
		hasil = ()
		error = False
		
		try:
			pass
		except:
			error = True


		if error:
			hasil = ()
		else:
			try:
				if len(data) != 0:
					q = f"SELECT history.id_history, product_type.name, product.name, via.service, via.name, history.amount, history.price, history.seller, history.time FROM history INNER JOIN product_type on history.id_product_type = product_type.id_product_type INNER JOIN product on history.id_product = product.id_product INNER JOIN via on history.id_via = via.id_via "
					
					if 'id_store' in data:
						q += " where history.id_store={}".format(int(data['id_store']))
						if 'id_product_type' in data:
							q += " and history.id_product_type={}".format(int(data['id_product_type']))
						if 'id_product' in data:
							q += " and history.id_product={}".format(int(data['id_product']))
						if 'id_via' in data:
							q += " and history.id_via={}".format(int(data['id_via']))

					hasil = self.__runQuery(q)
			except:
				logging.exception('Terdeteksi melakukan percobaan SQLI')
				hasil = ()

		return hasil

# SELECT history.id_history, product_type.name, product.name, via.service, via.name, history.amount, history.price, history.seller, history.time
# FROM history 
# INNER JOIN product_type on history.id_product_type = product_type.id_product_type
# INNER JOIN product on history.id_product = product.id_product
# INNER JOIN via on history.id_via = via.id_via 
# where history.id_store = 2


	# def testJoinProduct(self, id_store=2):
	# 	self.__runQuery('SELECT product_type.id_store, product_type.name, product.name, product.price, product.note FROM product_type INNER JOIN product ON product_type.id_product_type = product.id_product_type')
	# 	return self.__cur.fetchall()


class Main(DB):
	def __init__(self, dbLok='testing.db'):
		super().__init__(dbLok)
		








