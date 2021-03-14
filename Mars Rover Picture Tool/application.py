import os
import threading
import webbrowser
from functools import partial

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
from tkinter import messagebox

from services import RoverImageDownloader, CredentialWindow, read_credentials


class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.rovers = ['Perseverance', 'Curiosity', 'Opportunity', 'Spirit']
		self.current_rover = None
		self.btn_list = []

		self.persevarnce_cam = ['Any Camera', 'EDL_RUCAM', 'EDL_RDCAM', 'EDL_DDCAM', 'EDL_PUCAM1', 'EDL_PUCAM2',
								'NAVCAM_LEFT', 'NAVCAM_RIGHT', 'MCZ_RIGHT', 'MCZ_LEFT', 'FRONT_HAZCAM_LEFT_A',
								'FRONT_HAZCAM_RIGHT_A', 'REAR_HAZCAM_LEFT', 'REAR_HAZCAM_RIGHT',
								'SKYCAM', 'SHERLOC_WATSON']
		self.curiosity_cam = ['Any Camera', 'FHAZ', 'RHAZ', 'MAST', 'CHEMCAM', 'MAHLI', 'MARDI', 'NAVCAM']
		self.oppurtunity_cam = ['Any Camera', 'FHAZ', 'RHAZ', 'NAVCAM', 'PANCAM', 'MINITES']
		self.cam_dict = {'Perseverance':self.persevarnce_cam, 'Curiosity':self.curiosity_cam,
						 'Opportunity':self.oppurtunity_cam, 'Spirit':self.oppurtunity_cam}
		self.current_camera = tk.IntVar()

		self.image_dict = {'Perseverance':Perseverance_pic, 'Curiosity':Curiosity_pic,
							'Opportunity':Opportunity_pic, 'Spirit':Spirit_pic}

		self.sol_var = tk.StringVar()
		self.date_var = tk.StringVar()
		self.sol_var.trace('w', self.reset_date)
		self.date_var.trace('w', self.reset_sols)

		self.num_imgs = tk.IntVar()
		self.num_imgs.set(1)

		self.RIDownloader = RoverImageDownloader()

		self.draw_frames()
		self.draw_buttons()
		self.draw_date_frame()

	def draw_frames(self):
		self.topbar = tk.Frame(self, width=1050, height=50, bg='#252525', highlightthickness=1)
		self.imgFrame = tk.Frame(self, width=650, height=450, bg='#252525', highlightthickness=1)
		self.infoFrame =  tk.Frame(self, width=650, height=50, bg='dodgerblue3')
		self.rightlabel = tk.Frame(self, width=400, height=40, bg='#252525', highlightthickness=1)
		self.rightbar1 = tk.Frame(self, width=200, height=410, bg='white')
		self.rightbar2 = tk.Frame(self, width=200, height=410, bg='white')
		self.bottomBox = tk.Frame(self, width=400, height=50, bg='white') 

		self.topbar.grid(row=0, column=0, columnspan=3)
		self.imgFrame.grid(row=1, column=0, rowspan=2)
		self.infoFrame.grid(row=3, column=0)
		self.rightlabel.grid(row=1, column=1, columnspan=2)
		self.rightbar1.grid(row=2, column=1)
		self.rightbar2.grid(row=2, column=2)
		self.bottomBox.grid(row=3, column=1, columnspan=2)

		self.topbar.grid_propagate(False)
		self.imgFrame.grid_propagate(False)
		self.infoFrame.grid_propagate(False)
		self.rightlabel.grid_propagate(False)
		self.rightbar1.grid_propagate(False)
		self.rightbar2.grid_propagate(False)
		self.bottomBox.grid_propagate(False)

		self.canvas = tk.Canvas(self.imgFrame, width=650, height = 450, bg='#252525', bd=0, relief=tk.FLAT,
					highlightthickness=0)
		self.canvas.grid(row=0, column=0, padx=0, pady=0)

		tk.Label(self.rightlabel, text='Select Camera', bg='#252525', fg='white', font=('verdana', 10, 'bold')
					).grid(row=0, column=0, pady=5, padx=30)
		tk.Label(self.rightlabel, text='Select Day', bg='#252525', fg='white', font=('verdana', 10, 'bold')
					).grid(row=0, column=1, pady=5, padx=90)

		self.fetch = ttk.Button(self.bottomBox, text='Fetch Resources', width=16,
						command=self.fetch_resources)
		self.fetch.grid(row=0, column=0, padx=(30,0), pady=10)

		self.download = ttk.Button(self.bottomBox, text='Download Images', width=16, state=tk.DISABLED)
		self.download.grid(row=0, column=1, padx=(30,0), pady=10)

		self.open = ttk.Button(self.bottomBox, text='Open', width=12, state=tk.DISABLED,
						command=lambda : self.open_folder(self.current_rover))
		self.open.grid(row=0, column=2, padx=(30,0), pady=10)

	def draw_date_frame(self):
		ttk.Label(self.rightbar2, text='Enter Sol ( Martian Day )',
							).grid(row=0, column=0, padx=30, pady=(5,0))
		self.solEntry = ttk.Entry(self.rightbar2, width=20, textvariable=self.sol_var)
		self.solEntry.grid(row=1, column=0, padx=30, pady=(5,0))

		ttk.Label(self.rightbar2, text='Enter Earth Date\n( YYYY-MM-DD )',
						width=20, anchor=tk.CENTER).grid(row=2, column=0, padx=30, pady=(30,0))
		self.dateEntry = ttk.Entry(self.rightbar2, width=20, textvariable=self.date_var)
		self.dateEntry.grid(row=3, column=0, padx=30, pady=(5,0))

		ttk.Label(self.rightbar2, text='Number of Images\n(1<= images <=100)',
						width=20, anchor=tk.CENTER).grid(row=5, column=0, padx=30, pady=(40,0))
		self.num_img_en = ttk.Entry(self.rightbar2, width=10, textvariable=self.num_imgs)
		self.num_img_en.grid(row=6, column=0, padx=30, pady=5)

	def draw_buttons(self):
		cindex = 0
		for text in self.rovers:
			btn = tk.Button(self.topbar, text=text, width=25, font=('veradan', 10, 'bold'),
					relief=tk.RAISED, bg='#e84545', fg='white')
			btn.config(command=partial(self.set_selection, btn, text))
			btn.grid(row=0, column=cindex, padx=(20,0), pady=10)
			self.btn_list.append(btn)
			cindex += 1

		self.set_selection(self.btn_list[0], self.rovers[0])

		self.settings_btn = tk.Button(self.topbar, image=settings_icon, bg='#252525',
						relief=tk.FLAT, command=self.creds_win)
		self.settings_btn.grid(row=0, column=5, padx=(70,0))

	def set_selection(self, widget, text):
		for w in self.topbar.winfo_children()[:4]:
			w.config(relief=tk.FLAT, bg='#e84545')

		for w in self.rightbar1.winfo_children():
			w.destroy()

		widget.config(relief=tk.RAISED, bg='dodgerblue3')
		self.current_rover = text

		image = self.image_dict[text]
		self.canvas.create_image(0, 0, anchor='nw', image=image)

		rover = self.cam_dict[text]
		rover_cams = {camera : index+1 for index, camera in enumerate(rover)}
		r = 0
		for text, value in rover_cams.items():
			if r == 0:
				pady=(5,0)
			else:
				pady=2
			ttk.Radiobutton(self.rightbar1, text=text, variable=self.current_camera,
					value=value, width=25).grid(row=r, column=0, padx=15, pady=pady)
			r += 1
		self.current_camera.set(1)

	def reset_date(self, *args):
		if self.sol_var.get():
			self.date_var.set('')

	def reset_sols(self, *args):
		if self.date_var.get():
			self.sol_var.set('')

	def open_folder(self, rover):
		for r in self.rovers:
			if rover == r:
				if os.path.exists(rover + '/'):
					webbrowser.open('file:///' + os.path.realpath(rover + '/'))

	def creds_win(self):
		CredentialWindow()

	def fetch_resources(self):
		api_key = read_credentials()
		if not api_key:
			messagebox.showinfo('api key error', 'An Api key is required')
			CredentialWindow()
		else:
			rover = self.current_rover
			index = self.current_camera.get()
			rover_cams = self.cam_dict[rover]
			camera = rover_cams[index-1]
			if camera == 'Any Camera':
				camera = None

			sol = self.sol_var.get()
			date = self.date_var.get()

			num_img = self.num_imgs.get()
			if num_img <= 0:
				num_img = 1
			if num_img > 100:
				num_img = 100
			
			thread = threading.Thread(target=self.fetch_urls)
			thread.start()
			self.poll_thread(thread)

	def poll_thread(thread):
		if thread.is_alive()
		self.after()

	def fetch_urls(self)
			self.RIDownloader.fetch_urls(api_key, rover, camera=camera, sol=sol, date=date, num_img=num_img)

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('1050x550+130+80')
	root.title('MaRover Picture')

	settings_icon = PhotoImage(file='assets/settings.png')
	Perseverance_pic = PhotoImage(file='assets/Perseverance_rover.png')
	Curiosity_pic = PhotoImage(file='assets/Curiosity_rover.png')
	Opportunity_pic = PhotoImage(file='assets/Opportunity_rover.png')
	Spirit_pic = PhotoImage(file='assets/Spirit_rover.png')

	app = Application(master=root)
	app.mainloop()