import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox

import fungsi, sys
from datetime import datetime

def f_time(f_jam = "%H:%M:%S", f_hari = '%Y-%m-%d'): #mengembalikan jam dan hari 
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

class Main:
	def __init__(self):
		self.waktu, self.hari = f_time()
		self.raw_store = FUNGSI.getStore(q='singkat')
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


	def update_data(self):
		self.update_list_product_type(self.raw_store[self.combo_store.current()][0])

	def update_list_product_type(self, id_store=1):
		self.raw_product_type = FUNGSI.getProduct_type(id_store=id_store)
		self.list_product_type = [f"{i[2]}"for i in self.raw_product_type]
		self.combo_product_type['values'] = self.list_product_type
		if len(self.list_product_type) != 0:
			self.var_product_type.set(self.list_product_type[0])
			self.update_list_product(self.raw_product_type[0][0]) 
		else:
			self.var_product_type.set('')
			self.update_list_product(status=False)

	def update_list_product(self, id_product_type=1, status=True):
		if status:
			self.raw_product = FUNGSI.getProduct(id_product_type)
			self.list_product = [f"{i[3]} "for i in self.raw_product]
			self.combo_product['values'] = self.list_product
			if len(self.list_product) != 0:
				self.var_product.set(self.list_product[0])
				self.update_price(self.raw_product[0])
			else:
				self.var_product.set('')
				self.update_price(status=False)
		else:
			self.combo_product['values'] = []
			self.var_product.set('')
			self.update_price(status=False)

	def update_list_via(self, id_store=1):
		self.raw_via = FUNGSI.getVia(id_store=id_store)
		self.list_via = [f"{i[2]}-{i[3]}" for i in self.raw_via]
		self.combo_via['values'] = self.list_via
		if len(self.list_via) != 0:
			self.var_via.set(self.list_via[0])
		else:
			self.var_via.set('')

	def update_price(self, data_product={}, status=True):
		self.var_amount.set(1)
		if status:
			self.harga = data_product[4]
		else:
			self.harga = 0
		self.var_price.set(f_price(self.harga))

	def changeStore(self, *args):
		id_store = self.raw_store[self.combo_store.current()][0]

		self.update_list_product_type(id_store)
		self.update_list_via(id_store)

	def changeProduct_type(self, *args):
		id_product_type = self.raw_product_type[self.combo_product_type.current()][0]
		self.update_list_product(id_product_type)

	def changeProduct(self, *args):
		self.update_price(self.raw_product[self.combo_product.current()])

	def changeAmount(self,event):
		try:
			j = int(self.var_amount.get())
		except:
			j = 1
			self.var_amount.set(1)

		self.var_price.set(f_price(int(self.harga)*j))


################### Bagian window utama ###########################


class Dashboard(Main):
	def __init__(self, master):
		super().__init__()
		self.win = master
		self.win.geometry('700x450')
		self.win.title('Penjualan Game')
		self.win.resizable(False, False)

		self.frm_utama = tk.Frame(self.win)
		self.frm_utama.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

		self.sty_top()
		self.sty_bottom()

		self.win.mainloop()
	
	def update_price(self, data_product={}, status=True):
		self.var_amount.set(1)
		if status:
			self.harga = data_product[4]
		else:
			self.harga = 0
		self.var_price.set(f_price(self.harga))

	def sty_top(self):
		self.frm_top = tk.Frame(self.frm_utama)
		self.frm_top.pack(fill=tk.BOTH, expand=True)
		self.def_frm_option()
		self.def_frm_product()

		self.txt_price = tk.Label(self.frm_top, textvariable=self.var_price, font=("Arial", 45))
		self.txt_price.grid(row=3, column=0)

	def sty_bottom(self):
		self.frm_bottom = tk.Frame(self.frm_utama)
		self.frm_bottom.pack(fill=tk.BOTH)
		self.def_frm_menu()
		

	def def_frm_option(self):
		frm_detail = tk.Frame(self.frm_top)
		frm_detail.grid(row=0, column=0, sticky="W")

		tk.Label(frm_detail, text = 'store          ').grid(row=0, column=0, sticky="W")
		
		self.combo_store = ttk.Combobox(frm_detail, state='readonly', textvariable=self.var_store, values=self.list_store, width=25)
		self.combo_store.grid(row=0, column=1)
		self.combo_store.bind('<<ComboboxSelected>>', self.changeStore)

		tk.Label(frm_detail, text = '          ').grid(row=0, column=2, sticky="W")

		tk.Label(frm_detail, text = 'Tanggal    : ').grid(row=0, column=3, sticky="W")
		self.txt_tanggal = tk.Entry(frm_detail, textvariable=self.var_tanggal)
		self.txt_tanggal.grid(row=0, column=4)

	def def_frm_product(self):
		frm_option = tk.Frame(self.frm_top)
		frm_option.grid(row=1, column=0, pady=20)

		tk.Label(frm_option, text = 'Jenis').grid(row=0, column=0, sticky="W", pady=3)
		self.combo_product_type = ttk.Combobox(frm_option, state='readonly',textvariable=self.var_product_type, values=self.list_product, width=25)
		self.combo_product_type.grid(row=0, column=1)
		self.combo_product_type.bind('<<ComboboxSelected>>', self.changeProduct_type)
		
		tk.Label(frm_option, text = 'Product').grid(row=1, column=0, sticky="W", pady=3)
		self.combo_product = ttk.Combobox(frm_option, state='readonly',textvariable=self.var_product, values=self.list_product,width=25)
		self.combo_product.grid(row=1, column=1)
		self.combo_product.bind('<<ComboboxSelected>>', self.changeProduct)

		tk.Label(frm_option, text = 'Pembayaran').grid(row=2, column=0, sticky="W", pady=3)
		self.combo_via = ttk.Combobox(frm_option, state='readonly',textvariable=self.var_via, values=self.list_via,width=25)
		self.combo_via.grid(row=2, column=1)

		tk.Label(frm_option, text = '          ').grid(row=0, column=2, sticky="W")

		tk.Label(frm_option, text = 'Pembeli').grid(row=0, column=3, sticky="W")
		self.txt_seller = tk.Entry(frm_option, textvariable=self.var_seller,width=27)
		self.txt_seller.grid(row=0, column=4)

		tk.Label(frm_option, text = 'Jumlah').grid(row=1, column=3, sticky="W")
		self.txt_amount = tk.Entry(frm_option, textvariable=self.var_amount,width=27)
		self.txt_amount.grid(row=1, column=4)
		self.txt_amount.bind("<KeyRelease>", self.changeAmount)

		tk.Button(frm_option, text='Submit', bg='#0086E6', command=self.processSubmit).grid(row=4, column=0, sticky="W", pady=15)

	def def_frm_menu(self):
		frm_menu = tk.Frame(self.frm_bottom)
		frm_menu.grid(row=0, column=0)
		tk.Button(frm_menu,text='Admin', state=tk.NORMAL).grid(row=0, column=0, padx=15)
		tk.Button(frm_menu,text='Grafik', state=tk.NORMAL, command=self.to_winGrafik).grid(row=0, column=1, padx=15)
		tk.Button(frm_menu,text='Test', state=tk.NORMAL).grid(row=0, column=2, padx=15)
		

	def processSubmit(self):
		data = {}
		if self.combo_store.current() >= 0:
			data['id_store'] = self.raw_store[self.combo_store.current()][0]
			if self.combo_product_type.current() >= 0:
				data['id_product_type'] = self.raw_product_type[self.combo_product_type.current()][0]
				if self.combo_product.current() >= 0:
					data['id_product'] = self.raw_product[self.combo_product.current()][0]
					if self.combo_via.current() >= 0:
						data['id_via'] = self.raw_via[self.combo_via.current()][0]
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
				pass

			elif hasil['code'] == 2:
				pass

			elif hasil['code'] == 3:
				print('error code 3')

		self.update_data()


	def to_winGrafik(self):
		FilterGrafik(self.win)


class Admin:
	def __init__(self, Master):
		pass


class FilterGrafik(Main):
	def __init__(self, Master):
		super().__init__()
		self.master = Master
		self.winFilterGrafik = tk.Toplevel(Master)
		self.winFilterGrafik.geometry('450x165')

		self.var_cekbox_store = tk.IntVar()
		self.var_cekbox_product_type = tk.IntVar()
		self.var_cekbox_product = tk.IntVar()
		self.var_cekbox_via = tk.IntVar()

		self.winFilterGrafik.title('Filter Grafik')
		self.sty_top()
		self.winFilterGrafik.mainloop()

	def sty_top(self):
		self.frm_top = tk.Frame(self.winFilterGrafik)
		self.frm_top.pack(fill=tk.BOTH, expand=True, pady=12, padx=12)
		self.def_frm_grafik()
		tk.Button(self.winFilterGrafik, text='Search', command=self.getHistoryFilter).pack(pady=3, fill=tk.BOTH, padx=12)


	def def_frm_grafik(self):
		frm_grafik_atas = tk.Frame(self.frm_top)
		frm_grafik_atas.grid(row=0, column=0)

		tk.Label(frm_grafik_atas, text = 'store          ').grid(row=0, column=0, sticky="W")
		
		self.combo_store = ttk.Combobox(frm_grafik_atas, state='readonly', textvariable=self.var_store, values=self.list_store, width=25)
		self.combo_store.grid(row=0, column=1); self.combo_store.bind('<<ComboboxSelected>>', self.changeStore)
		cekbox_store = tk.Checkbutton(frm_grafik_atas, text='Store', variable=self.var_cekbox_store)
		cekbox_store.select()
		cekbox_store.config(state='disabled')
		cekbox_store.grid(row=0, column=2, sticky="W")

		tk.Label(frm_grafik_atas, text = 'Jenis').grid(row=1, column=0, sticky="W", pady=3)
		self.combo_product_type = ttk.Combobox(frm_grafik_atas, state='readonly',textvariable=self.var_product_type, values=self.list_product, width=25)
		self.combo_product_type.grid(row=1, column=1)
		self.combo_product_type.bind('<<ComboboxSelected>>', self.changeProduct_type)
		cekbox_product_type = tk.Checkbutton(frm_grafik_atas, text='Product Type', variable=self.var_cekbox_product_type)
		cekbox_product_type.grid(row=1, column=2, sticky="W")

		tk.Label(frm_grafik_atas, text = 'Product').grid(row=2, column=0, sticky="W", pady=3)
		self.combo_product = ttk.Combobox(frm_grafik_atas, state='readonly',textvariable=self.var_product, values=self.list_product,width=25)
		self.combo_product.grid(row=2, column=1)
		self.combo_product.bind('<<ComboboxSelected>>', self.changeProduct)
		cekbox_product = tk.Checkbutton(frm_grafik_atas, text='Product', variable=self.var_cekbox_product)
		cekbox_product.grid(row=2, column=2, sticky="W")
		
		tk.Label(frm_grafik_atas, text = 'Pembayaran').grid(row=3, column=0, sticky="W", pady=3)
		self.combo_via = ttk.Combobox(frm_grafik_atas, state='readonly',textvariable=self.var_via, values=self.list_via,width=25)
		self.combo_via.grid(row=3, column=1)
		cekbox_via = tk.Checkbutton(frm_grafik_atas, text='Via', variable=self.var_cekbox_via)
		cekbox_via.grid(row=3, column=2, sticky="W")

		
	def update_price(self, data_product={}, status=True):
		pass ## jangan di hapus

	def getHistoryFilter(self):
		data_id = {}
		data_text = {}
		if self.combo_store.current() >= 0:
			data_id['id_store'] = self.raw_store[self.combo_store.current()][0]
			data_text['store'] = self.combo_store.get()

			if self.var_cekbox_product_type.get():
				if self.combo_product_type.current() >= 0:
					data_id['id_product_type'] = self.raw_product_type[self.combo_product_type.current()][0]
					data_text['product_type'] = self.combo_product_type.get()
			if self.var_cekbox_product.get():
				if self.combo_product.current() >= 0:
					data_id['id_product'] = self.raw_product[self.combo_product.current()][0]
					data_text['product'] = self.combo_product.get()
			if self.var_cekbox_via.get():
				if self.combo_via.current() >= 0:
					data_id['id_via'] = self.raw_via[self.combo_via.current()][0]
					data_text['via'] = self.combo_via.get()

		history = FUNGSI.getHistory(data_id)
		self.winFilterGrafik.destroy()
		Grafik(self.master, history, data_id, data_text)


class Grafik:
	def __init__(self, Master, history, data_id, data_text):
		
		self.raw_data = history
		self.winGrafik = tk.Toplevel(Master)
		#self.winGrafik.geometry('700x500')

		self.var_store = tk.StringVar(); self.var_store.set('')
		self.var_product_type = tk.StringVar(); self.var_product_type.set('')
		self.var_product = tk.StringVar(); self.var_product.set('')
		self.var_via = tk.StringVar(); self.var_via.set('')

		for i in data_text:
			if i == 'store':
				self.var_store.set(data_text[i])

			elif i == 'product_type':
				self.var_product_type.set(data_text[i])

			elif i == 'product':
				self.var_product.set(data_text[i])

			elif i == 'via':
				self.var_via.set(data_text[i])


		self.winGrafik.title('Show Data')
		self.sum_data = self.sum_raw_data()
		self.sty_top()
		self.sty_center()
		self.sty_bottom()
		self.winGrafik.mainloop()

	def sum_raw_data(self):
		pendapatan = 0
		sum_product_type = {}
		sum_product = {}
		sum_via = {}
		hasil = {'total':{}}
		for i in self.raw_data:
			pendapatan+=i[6]
			if i[1] not in sum_product_type:
				sum_product_type[i[1]] = {'sold':1, 'income':i[6]}
			else:
				sum_product_type[i[1]]['sold'] += 1
				sum_product_type[i[1]]['income'] += i[6]

			if i[2] not in sum_product:
				sum_product[i[2]] = {'sold':1, 'income':i[6]}
			else:
				sum_product[i[2]]['sold'] += 1
				sum_product[i[2]]['income'] += i[6]

			if i[3] not in sum_via:
				sum_via[i[3]] = {i[4]:{'sold':1, 'income':i[6]}}
			else:
				if i[4] not in sum_via[i[3]]:
					sum_via[i[3]][i[4]] = {'sold':1, 'income':i[6]}
				else:
					sum_via[i[3]][i[4]]['sold'] += 1
					sum_via[i[3]][i[4]]['income'] += i[6]

		
		hasil['total']['income'] = pendapatan
		hasil['total']['sold'] = len(self.raw_data)
		hasil['total']['product_type'] = len(sum_product_type)
		hasil['total']['product'] = len(sum_product)
		hasil['total']['via'] = len(sum_via)
		hasil['product_type'] = sum_product_type
		hasil['product'] = sum_product
		hasil['via'] = sum_via

		#print(self.raw_data[0])
		# print(sys.getsizeof(self.raw_data))
		# print(sys.getsizeof(hasil))

		return hasil

	def generate_treeView(self, window, data, scroll=(0,3), size=[20,20]):
		raw_data, column_name, column_title, column_size = data
		sRow, sCol = scroll
		style = ttk.Style(window)
		style.configure('Treeview', rowheight=size[0], height=size[1])

		treeView = ttk.Treeview(window)
		treeView.config(columns=column_name, show = "headings")
		
		for c_data, c_title, c_size in zip(column_name, column_title, column_size):
			treeView.heading(c_data, text=c_title)
			treeView.column(c_data, width=c_size)

		for num, val in enumerate(raw_data):
			treeView.insert('','end', values=val)

		scroll_treeView = ttk.Scrollbar(window, orient="vertical", command=treeView.yview)
		scroll_treeView.grid(row=sRow, column=sCol,sticky=tk.N+tk.S)
		treeView.configure(yscrollcommand=scroll_treeView.set)

		return treeView

	def sty_top(self):
		self.frm_top = tk.Frame(self.winGrafik)
		self.frm_top.pack(fill=tk.BOTH, expand=True, pady=12, padx=12)
		self.def_frm_0_top()
		self.def_frm_1_top()

	def sty_center(self):
		self.frm_center = tk.Frame(self.winGrafik)
		self.frm_center.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
		self.def_frm_0_center()

	def sty_bottom(self):
		self.frm_bottom = tk.Frame(self.winGrafik)
		self.frm_bottom.pack(fill=tk.BOTH)
		self.def_frm_0_bottom()
		#self.def_frm

	def def_frm_0_top(self):
		frm_0 = tk.Frame(self.frm_top)
		frm_0.grid(row=0, column=0)

		frm_0_0 = tk.Frame(frm_0)
		frm_0_0.grid(row=0, column=0, pady=17, sticky="W")

		frm_0_1 = tk.Frame(frm_0)
		frm_0_1.grid(row=1, column=0, pady=25, sticky="W")
		
		tk.Label(frm_0_0, text='Pemasukan ').grid(row=0, column=0, sticky="W")
		tk.Label(frm_0_0, text=' : ').grid(row=0, column=1, sticky="W")
		tk.Label(frm_0_0, text=f_price(self.sum_data['total']['income'])).grid(row=0, column=2, sticky="W")

		tk.Label(frm_0_0, text='Terjual ').grid(row=1, column=0, sticky="W")
		tk.Label(frm_0_0, text=' : ').grid(row=1, column=1, sticky="W")
		tk.Label(frm_0_0, text=self.sum_data['total']['sold']).grid(row=1, column=2, sticky="W")

		tk.Label(frm_0_1, text='Toko ').grid(row=1, column=0, sticky="W")
		tk.Label(frm_0_1, text=' : ').grid(row=1, column=1, sticky="W")
		tk.Label(frm_0_1, textvariable=self.var_store).grid(row=1, column=2, sticky="W")

		tk.Label(frm_0_1, text='Type ').grid(row=2, column=0, sticky="W")
		tk.Label(frm_0_1, text=' : ').grid(row=2, column=1, sticky="W")
		tk.Label(frm_0_1, textvariable=self.var_product_type).grid(row=2, column=2, sticky="W")

		tk.Label(frm_0_1, text='Product ').grid(row=3, column=0, sticky="W")
		tk.Label(frm_0_1, text=' : ').grid(row=3, column=1, sticky="W")
		tk.Label(frm_0_1, textvariable=self.var_product).grid(row=3, column=2, sticky="W")

		tk.Label(frm_0_1, text='Pembayaran ').grid(row=4, column=0, sticky="W")
		tk.Label(frm_0_1, text=' : ').grid(row=4, column=1, sticky="W")
		tk.Label(frm_0_1, textvariable=self.var_via).grid(row=4, column=2, sticky="W")

		print(self.sum_data)


	def def_frm_1_top(self):
		frm_1 = tk.Frame(self.frm_top)
		frm_1.grid(row=0, column=2, padx=15)

		list_product_type = []
		for i in self.sum_data['product_type']:
			list_product_type.append([i, self.sum_data['product_type'][i]['sold'], f_price(self.sum_data['product_type'][i]['income'])])

		list_product = []
		for i in self.sum_data['product']:
			list_product.append([i, self.sum_data['product'][i]['sold'], f_price(self.sum_data['product'][i]['income'])])

		list_via =  []
		for i in self.sum_data['via']:
			for j in self.sum_data['via'][i]:
				list_via.append([f"{i} {j}", self.sum_data['via'][i][j]['sold'], f_price(self.sum_data['via'][i][j]['income'])])


		tree_product_type = self.generate_treeView(frm_1,(list_product_type, ['name','sold','income'], ['Nama', 'Terjual', 'Pemasukan'], [80,80,90]))
		tree_product_type.grid(row=0, column=0, sticky='nsew')

		tree_product = self.generate_treeView(frm_1,(list_product,['name','sold','income'], ['Nama', 'Terjual', 'Pemasukan'], [80,80,90]))
		tree_product.grid(row=0, column=1, sticky='nsew')

		tree_via = self.generate_treeView(frm_1,(list_via, ['name','sold','income'], ['Nama', 'Terjual', 'Pemasukan'], [80,80,90]))
		tree_via.grid(row=0, column=2, sticky='nsew')


	def def_frm_0_center(self):
		frm_1 = tk.Frame(self.frm_center)
		frm_1.grid(row=0, column=1)

		fig = Figure(figsize = (6,1.5), dpi = 150)
		list_product_type = [[],[]]
		list_via = [[],[]]
		
		for i in self.sum_data['product_type']:
		    list_product_type[0].append(self.sum_data['product_type'][i]['income'])
		    list_product_type[1].append(i)

		for i in self.sum_data['via']:
		    for j in self.sum_data['via'][i]:
		        list_via[0].append(self.sum_data['via'][i][j]['income'])
		        list_via[1].append(f'{i} {j}')

		plot_product_type = fig.add_subplot(131)
		plot_product_type.pie(list_product_type[0], labels = list_product_type[1], autopct='%.1f%%',wedgeprops={'linewidth': 2.0, 'edgecolor': 'white'}, textprops={'size': 'x-small'})
		plot_product_type.set_title('Tipe Produk', fontsize=7)

		plot_via = fig.add_subplot(133)
		plot_via.pie(list_via[0], labels = list_via[1], autopct='%.1f%%',wedgeprops={'linewidth': 2.0, 'edgecolor': 'white'}, textprops={'size': 'x-small'})
		plot_via.set_title('Pembayaran', fontsize=7)

		canvas_plot = FigureCanvasTkAgg(fig, frm_1)
		canvas_plot.get_tk_widget().grid(row=0, column=0, padx=20)

		#for i in

	def def_frm_0_bottom(self):
		frm_0 = tk.Frame(self.frm_bottom)
		frm_0.grid(row=0, column=0, pady=20, padx=20)
		title = ('Id', 'Type Product', 'Product', 'Via Service', 'Via Name', 'Jumlah', 'Total', 'Pembeli', 'Waktu')
		size = (40, 110, 110, 100, 125, 60,100, 100,160)
		tree_history = self.generate_treeView(frm_0, (self.raw_data, ('id', 'type', 'product', 'via_service', 'via_name', 'amount', 'price', 'seller','time'), title, size))
		tree_history.grid(row=0, column=0,columnspan=3)

Dashboard(tk.Tk())