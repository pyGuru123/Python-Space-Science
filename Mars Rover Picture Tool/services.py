import os
import json
import webbrowser
import tkinter as tk
from math import ceil
import concurrent.futures

import requests

class RoverImageDownloader:
	def __init__(self):
		self.url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/'

	def fetch_urls(self, api_key, rover, camera=None, sol=None, date=None, num_img=1):
		self.image_urls = []
		url = self.url
		pages = ceil(num_img / 25)
		print(pages)

		url += f'{rover}/photos?'
		if camera:
			url += f'camera={camera}&'
		if sol:
			url += f'sol={sol}&'
		if date:
			url += f'earth_date={date}&'
	
		url += f'pages={pages}&'
		url += f'api_key={api_key}'
		print(url)
		
		try:
			r = requests.get(url)
			im_list = r.json()['photos']
			for dct in im_list:
				img = dct['img_src']
				self.image_urls.append(img)

			self.image_urls = self.image_urls[:num_img]
			return 'done'
		except:
			return 'error'

	def download_images(self, rover, sol, date):
		if not os.path.exists(f'{rover}/'):
			os.mkdir(f'{rover}')

		rovers = [rover for i in range(len(self.image_urls))]
		sols = [None for i in range(len(self.image_urls))]
		dates = [None for i in range(len(self.image_urls))]
		if sol:
			sols = [sol for i in range(len(self.image_urls))]
		if date:
			dates = [date for i in range(len(self.image_urls))]
		with concurrent.futures.ThreadPoolExecutor() as executor:
			executor.map(self.download_img, self.image_urls, rovers, sols ,dates)

	def download_img(self, url, rover, sol=None, date=None):
		name = url.split('/')[-1]
		if sol:
			fname = f'{rover}/sol-{sol}-{name}'
		elif date:
			fname = f'{rover}/date-{date}-{name}'
		r = requests.get(url)
		with open(fname, 'wb') as f:
			f.write(r.content)

def rover_info(rover):
	json_file = 'data/info.json'

	if os.path.exists(json_file):
		with open(json_file, 'r') as file:
			dct = json.load(file)
			return dct[rover]


class CredentialWindow(tk.Toplevel):
	def __init__(self):
		super(CredentialWindow, self).__init__()
		self.title('Credentials')
		self.geometry('300x150+550+345')
		self.resizable(0,0)

		self.draw_widgets()
		self.protocol("WM_DELETE_WINDOW", self.destroy)

	def draw_widgets(self):
		tk.Label(self, text='Enter API key here', fg='black',
				font=('verdana', 10, 'bold')).grid(row=0, column=0, padx=80, pady=5,
						columnspan=4)

		pady = 10

		self.key = tk.StringVar()

		api_key = read_credentials()
		if api_key:
			self.key.set(api_key)

		tk.Entry(self, width=45, textvariable=self.key).grid(row=1, column=1,
							 columnspan=2, pady=pady)

		tk.Button(self, text='Save',bg='green', relief=tk.FLAT,
					fg='white', width=8, command=self.save_credentials
					).grid(row=3, column=1, columnspan=2, pady=5)

		self.linklbl = tk.Label(self, text='Register for an API key here', fg='blue', cursor='hand2',
				font=('verdana', 7, 'underline'))
		self.linklbl.grid(row=4, column=0, padx=80, pady=20,
						columnspan=4)
		self.linklbl.bind("<Button-1>", self.nasa_api_home)

	def save_credentials(self):
		key = self.key.get()

		data = {
				'api_key' : key,
		}

		write_credentials(data)

		self.destroy()

	def nasa_api_home(self, event):
		webbrowser.open('https://api.nasa.gov/')

def read_credentials():
	json_file = 'data/credentials.json'

	if os.path.exists(json_file):
		with open(json_file, 'r') as file:
			dct = json.load(file)

		return dct['api_key']
	else:
		return None

def write_credentials(data):
	json_file = 'data/credentials.json'
	with open(json_file, 'w') as file:
		json.dump(data, file)