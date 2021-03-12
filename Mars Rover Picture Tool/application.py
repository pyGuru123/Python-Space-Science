import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
from functools import partial


class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.rovers = ['Perseverance', 'Curiosity', 'Oppurtunity', 'Spirit']
		self.current_rover = None
		self.btn_list = []

		self.persevarnce_cam = ['Any Camera', 'EDL_RUCAM', 'EDL_RDCAM', 'EDL_DDCAM', 'EDL_PUCAM1', 'EDL_PUCAM2',
								'NAVCAM_LEFT', 'NAVCAM_RIGHT', 'MCZ_RIGHT', 'MCZ_LEFT', 'FRONT_HAZCAM_LEFT_A',
								'FRONT_HAZCAM_RIGHT_A', 'REAR_HAZCAM_LEFT', 'REAR_HAZCAM_RIGHT',
								'SKYCAM', 'SHERLOC_WATSON']
		self.curiosity_cam = ['Any Camera', 'FHAZ', 'RHAZ', 'MAST', 'CHEMCAM', 'MAHLI', 'MARDI', 'NAVCAM']
		self.oppurtunity_cam = ['Any Camera', 'FHAZ', 'RHAZ', 'NAVCAM', 'PANCAM', 'MINITES']
		self.cam_dict = {'Perseverance':self.persevarnce_cam, 'Curiosity':self.curiosity_cam,
						 'Oppurtunity':self.oppurtunity_cam, 'Spirit':self.oppurtunity_cam}
		self.current_camera = tk.IntVar()

		self.draw_frames()
		self.draw_buttons()

	def draw_frames(self):
		self.topbar = tk.Frame(self, width=1050, height=50, bg='#252525')
		self.imgFrame = tk.Frame(self, width=650, height=450, bg='#252525')
		self.infoFrame =  tk.Frame(self, width=650, height=50, bg='#252525')
		self.rightlabel = tk.Frame(self, width=400, height=40, bg='#252525')
		self.rightbar = tk.Frame(self, width=400, height=410, bg='white')
		self.bottomBox = tk.Frame(self, width=400, height=50, bg='dodgerblue3') 

		self.topbar.grid(row=0, column=0, columnspan=2)
		self.imgFrame.grid(row=1, column=0, rowspan=2)
		self.infoFrame.grid(row=3, column=0)
		self.rightlabel.grid(row=1, column=1)
		self.rightbar.grid(row=2, column=1)
		self.bottomBox.grid(row=3, column=1)

		self.topbar.grid_propagate(False)
		self.imgFrame.grid_propagate(False)
		self.infoFrame.grid_propagate(False)
		self.rightlabel.grid_propagate(False)
		self.rightbar.grid_propagate(False)
		self.bottomBox.grid_propagate(False)

		self.canvas = tk.Canvas(self.imgFrame, width=650, height = 450, bg='#252525')
		self.canvas.grid(row=0, column=0, padx=0)

	def draw_buttons(self):
		cindex = 0
		for text in self.rovers:
			btn = tk.Button(self.topbar, text=text, width=25,
					relief=tk.RAISED, bg='#e84545', fg='white')
			btn.config(command=partial(self.set_selection, btn, text))
			btn.grid(row=0, column=cindex, padx=(20,0), pady=10)
			self.btn_list.append(btn)
			cindex += 1

		self.set_selection(self.btn_list[0], self.rovers[0])

		self.settings_btn = tk.Button(self.topbar, image=settings_icon, bg='#252525',
						relief=tk.FLAT)
		self.settings_btn.grid(row=0, column=5, padx=(70,0))

	def set_selection(self, widget, text):
		# if self.render_id:
		# 	self.imgFrame.after_cancel(self.render_id)
		# 	self.render_id = None

		for w in self.imgFrame.winfo_children():
			w.destroy()

		self.canvas = tk.Canvas(self.imgFrame, width=650, height= 450, bg='#252525')
		self.canvas.grid(row=0, column=0, sticky='nsew')

		for w in self.topbar.winfo_children()[:4]:
			w.config(relief=tk.FLAT, bg='#e84545')

		for w in self.bottomBox.winfo_children():
			w.destroy()

		for w in self.rightbar.winfo_children():
			w.destroy()

		
		widget.config(relief=tk.RAISED, bg='dodgerblue3')
		self.current_rover = text

		rover = self.cam_dict[text]
		rover_cams = {camera : index+1 for index, camera in enumerate(rover)}
		r = 0
		for text, value in rover_cams.items():
			ttk.Radiobutton(self.rightbar, text=text, variable=self.current_camera,
					value=value, command=self.show_option, width=25).grid(row=r, column=0, padx=10, pady=2)
			r += 1
		self.current_camera.set(1)
		self.show_option()

	def show_option(self):
		rover = self.current_rover
		index = self.current_camera.get()
		rover_cams = self.cam_dict[rover]
		print(rover, rover_cams[index-1])


if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('1050x550+80+80')
	root.title('MaRover Picture')

	settings_icon = PhotoImage(file='assets/settings.png')

	app = Application(master=root)
	app.mainloop()