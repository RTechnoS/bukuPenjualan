import tkinter as tk
from tkinter import ttk, messagebox
import fungsi
from datetime import datetime

def f_time(f_jam = "%H:%M:%S", f_hari = '%Y-%m-%d'):
	waktu = datetime.now()
	return (waktu.strftime(f_jam), waktu.strftime(f_hari)) #jam - hari

def f_price(jumlah): #mengubah angka contoh : 3200000 menjadi 3.200.000
	jumlah = str(jumlah)
	
	dt = []
	pjg = len(jumlah)
	p = jumlah
	if pjg > 3:
		sisa = pjg % 3
		jml = pjg //3
		if sisa != 0:
			dt.append(p[:sisa])
			p = p[sisa:]

		for i in range(jml):
			dt.append(p[:3])
			p = p[3:]
		jumlah = '.'.join(dt)
	return jumlah

FUNGSI = fungsi.Main()
connect = FUNGSI.getConnect
cur = FUNGSI.getCur

class Dashboard:
	def __init__(self, master):
		self.win = master
		self.win.geometry('700x450')
		self.win.title('Penjualan Game')
		self.win.resizable(False, False)

		self.waktu, self.hari = f_time()

		self.frm_utama = tk.Frame(self.win)
		self.frm_utama.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

		self.raw_store = FUNGSI.getStore(q='id_store,name')
		self.list_store = [f"{i[1]}"for i in self.raw_store]

		self.list_product_type = []
		self.list_product = []
		self.list_via = []

		self.var_store = tk.StringVar(); self.var_store.set('')
		self.var_tanggal = tk.StringVar(); self.var_tanggal.set(self.hari)
		self.var_product_type = tk.StringVar(); self.var_product_type.set('')
		self.var_product = tk.StringVar(); self.var_product.set('')
		self.var_via = tk.StringVar(); self.var_via.set('')
		self.var_price = tk.StringVar(); self.var_price.set(f_price(0))
		self.var_amount = tk.StringVar(); self.var_amount.set(1)
		self.var_seller = tk.StringVar(); self.var_seller.set('')
		self.harga = 0

		self.sty_atas()
		#self.sty_bawah()

		self.win.mainloop()


	def update_list_product_type(self, id_store=1):
		self.raw_product_type = FUNGSI.getProduct_type(id_store=id_store)
		self.list_product_type = [f"{i[2]}"for i in self.raw_product_type]
		self.__combo_product_type['values'] = self.list_product_type
		if len(self.list_product_type) != 0:
			self.var_product_type.set(self.list_product_type[0])
			self.update_list_product(self.raw_product_type[0][0]) 
		else:
			self.var_product_type.set('')
			self.update_list_product(status=False)
			#self.update_price(status=False)

	def update_list_product(self, id_product_type=1, status=True):
		if status:
			self.raw_product = FUNGSI.getProduct(id_product_type)
			self.list_product = [f"{i[3]} "for i in self.raw_product]
			self.__combo_product['values'] = self.list_product
			if len(self.list_product) != 0:
				self.var_product.set(self.list_product[0])
				self.update_price(self.raw_product[0])
			else:
				self.var_product.set('')
				self.update_price(status=False)
		else:
			self.__combo_product['values'] = []
			self.var_product.set('')
			self.update_price(status=False)

	def update_list_via(self, id_store=1):
		self.raw_via = FUNGSI.getVia(id_store=id_store)
		self.list_via = [f"{i[2]}-{i[3]}" for i in self.raw_via]
		self.__combo_via['values'] = self.list_via
		if len(self.list_via) != 0:
			self.var_via.set(self.list_via[0])
		else:
			self.var_via.set('')

	def update_price(self, data_product=0, status=True):
		self.var_amount.set(1)
		if status:
			self.harga = data_product[4]
		else:
			self.harga = 0
		self.var_price.set(f_price(self.harga))

	def changeStore(self, *args):
		id_store = self.raw_store[self.__combo_store.current()][0]

		self.update_list_product_type(id_store)
		self.update_list_via(id_store)

	def changeProduct_type(self, *args):
		id_product_type = self.raw_product_type[self.__combo_product_type.current()][0]
		#print('\nproduct_type = ', self.raw_product_type[self.__combo_product_type.current()])

		self.update_list_product(id_product_type)

	def changeProduct(self, *args):
		# id_product = self.raw_product[self.__combo_product.current()][0]
		# print('\nid_product = ', id_product)
		self.update_price(self.raw_product[self.__combo_product.current()])
		#print(self.raw_product[id_product][4])
		#price = self.list_product

	def changeAmount(self,event):
		#print(event.__dict__)
		#print(int(self.harga)*int(self.var_amount.get()))
		try:
			j = int(self.var_amount.get())
		except:
			j = 1
			self.var_amount.set(1)

		self.var_price.set(f_price(int(self.harga)*j))


################### Bagian window utama ###########################

	def sty_atas(self):
		self.frm_atas = tk.Frame(self.frm_utama)
		self.frm_atas.pack(fill=tk.BOTH)
		self.def_frm_option()
		self.def_frm_product()

		self.__txt_price = tk.Label(self.frm_atas, textvariable=self.var_price, font=("Arial", 45))
		self.__txt_price.grid(row=3, column=0)

	def def_frm_option(self):
		frm_detail = tk.Frame(self.frm_atas)
		frm_detail.grid(row=0, column=0, sticky="W")


		
		tk.Label(frm_detail, text = 'store          ').grid(row=0, column=0, sticky="W")
		
		self.__combo_store = ttk.Combobox(frm_detail, state='readonly', textvariable=self.var_store, values=self.list_store, width=25)
		self.__combo_store.grid(row=0, column=1)
		self.__combo_store.bind('<<ComboboxSelected>>', self.changeStore)

		tk.Label(frm_detail, text = '          ').grid(row=0, column=2, sticky="W")

		tk.Label(frm_detail, text = 'Tanggal    : ').grid(row=0, column=3, sticky="W")
		self.__txt_tanggal = tk.Entry(frm_detail, textvariable=self.var_tanggal)
		self.__txt_tanggal.grid(row=0, column=4)

	def def_frm_product(self):
		frm_option = tk.Frame(self.frm_atas)
		frm_option.grid(row=1, column=0, pady=20)

		tk.Label(frm_option, text = 'Jenis').grid(row=0, column=0, sticky="W", pady=3)
		self.__combo_product_type = ttk.Combobox(frm_option, state='readonly',textvariable=self.var_product_type, values=self.list_product, width=25)
		self.__combo_product_type.grid(row=0, column=1)
		self.__combo_product_type.bind('<<ComboboxSelected>>', self.changeProduct_type)
		
		tk.Label(frm_option, text = 'Product').grid(row=1, column=0, sticky="W", pady=3)
		self.__combo_product = ttk.Combobox(frm_option, state='readonly',textvariable=self.var_product, values=self.list_product,width=25)
		self.__combo_product.grid(row=1, column=1)
		self.__combo_product.bind('<<ComboboxSelected>>', self.changeProduct)

		tk.Label(frm_option, text = 'Pembayaran').grid(row=2, column=0, sticky="W", pady=3)
		self.__combo_via = ttk.Combobox(frm_option, state='readonly',textvariable=self.var_via, values=self.list_via,width=25)
		self.__combo_via.grid(row=2, column=1)

		# tk.Label(frm_option, text = 'Harga').grid(row=3, column=0, sticky="W", pady=3)


		tk.Label(frm_option, text = '          ').grid(row=0, column=2, sticky="W")

		tk.Label(frm_option, text = 'Pembeli').grid(row=0, column=3, sticky="W")
		self.__txt_seller = tk.Entry(frm_option, textvariable=self.var_seller,width=27)
		self.__txt_seller.grid(row=0, column=4)

		tk.Label(frm_option, text = 'Jumlah').grid(row=1, column=3, sticky="W")
		self.__txt_amount = tk.Entry(frm_option, textvariable=self.var_amount,width=27)
		self.__txt_amount.grid(row=1, column=4)
		self.__txt_amount.bind("<KeyRelease>", self.changeAmount)

		tk.Button(frm_option, text='Submit', bg='#0086E6', command=self.processSubmit).grid(row=4, column=0, sticky="W", pady=15)


	def processSubmit(self):
		data = {}
		if self.__combo_store.current() >= 0:
			data['id_store'] = self.raw_store[self.__combo_store.current()][0]
			if self.__combo_product_type.current() >= 0:
				data['id_product_type'] = self.raw_product_type[self.__combo_product_type.current()][0]
				if self.__combo_product.current() >= 0:
					data['id_product'] = self.raw_product[self.__combo_product.current()][0]
					if self.__combo_via.current() >= 0:
						data['id_via'] = self.raw_via[self.__combo_via.current()][0]
						if int(self.var_amount.get()) > 0:
							data['amount'] = int(self.var_amount.get())
							if int(self.harga) > 0:
								data['price'] = self.harga * int(self.var_amount.get())
								if len(self.var_tanggal.get()) == 10:
									data['time'] = self.var_tanggal.get()
									data['seller'] = self.var_seller.get()
									self.sendSubmit(data)
									


	def sendSubmit(self, data):
		hasil = FUNGSI.submitHistory(data['id_store'], data['id_product_type'],data['id_product'], data['id_via'], data['price'], data['time'], data['amount'], data['seller'])
		if hasil['status']:
			print('\033[1;37;44m[DONE]\033[0m ', hasil['time'], ' Total ', f_price(hasil['price']))
			messagebox.showinfo('Succes', 'Submit Succes')
		else:
			print('\033[1;37;41m[FAIL]\033[0m ', hasil['pesan'])
			messagebox.showerror('Gagal', hasil['pesan'])
			if hasil['code'] == 1:
				self.update_list_product_type(self.raw_store[self.__combo_store.current()][0])

			elif hasil['code'] == 2:
				self.update_list_product_type(self.raw_store[self.__combo_store.current()][0])

			elif hasil['code'] == 3:
				print('error code 3')
Dashboard(tk.Tk())