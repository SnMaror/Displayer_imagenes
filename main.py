

"""
## Python 3.6 por SnMaror, primer upload a github.

# Fue hecho sin tener en cuenta mostrarselo a alguien asi que si alguien lo ve no me maten por la falta de comentarios
# como dije en la descripcon se podria mejorar de todo en este programita jaja desde hacerlo 
# mas optimo a hacerlo mas estetico o agregarle funciones

# Ni siquiera voy a explicar como funciona #Hdp :v


"""

#### imports

from tkinter import *
from PIL import Image ,ImageTk 
from tkinter import filedialog
from tkinter import messagebox
from random import randint
from threading import Thread
from win32api import GetSystemMetrics
import glob,time,os,re

#########
######### Classes
#########

class Img():
	"""docstring for Img"""
	def __init__(self,file,**kwargs):
		
		self.file = file
		self.img = None

		if "image" in kwargs and isinstance(kwargs["image"],Image.Image):
			self.img = kwargs["image"]
		elif os.path.isfile(file):
			self.img = Image.open(file)


		if "size" in kwargs:
			self.resize(kwargs["size"])

		self.frames = []
		self.actual_frame = 0
		self.last_center = None
		self.last_factor = None


		self.set_frames()

		print(len(self.frames))
	def adjust(self,size):
		if self.img == None:return

		if isinstance(size,(list,tuple)):
			x, y = self.img.size


			y = int(max(y * size[0] / x, 1))
			x = int(size[0])
        	
			x = int(max(x * size[1] / y, 1))
			y = int(size[1])

			if x !=self.img.width or y != self.img.height:
				self.img = self.img.resize((x,y),Image.ANTIALIAS)

	def resize(self,size):
		if self.img == None:return

		if isinstance(size,(list,tuple)):
			self.img = self.img.resize(size,Image.ANTIALIAS)


	def zoom(self,factor,mode = 0,**kwargs):
		if self.img == None:return

		if factor == 0:
			return self.img
		
		if factor <0:
			mode*= -1
			factor = abs(factor)

		if factor > 4:
			factor = 4

		factor+=1

		if mode == 0:
			nw_imagen = self.img.resize((int(self.img.width*factor),int(self.img.height*factor)),Image.ANTIALIAS)
			return nw_imagen


		if not "center" in kwargs:
			raise KeyError("No se encontro la llave 'center' en kwargs, para el modo 1 o -1 es necesaria.")
		else:
			if mode == 1:
				difx,dify = (self.img.width/factor)/2, (self.img.height/factor)/2
				if difx <50 or dify <50:
					return 
			else:
				difx,dify = (factor*self.img.width)/2, (factor*self.img.height)/2

			center = kwargs["center"]

			desde_x = int(center[0]-difx)
			desde_y = int(center[1]-dify)

			hasta_x = int(center[0]+difx)
			hasta_y = int(center[1]+dify)




			if desde_x<1:
				dif= 1-desde_x

				desde_x = 1
				hasta_x+=dif

			if hasta_x > self.img.width:
				dif = hasta_x-self.img.width
				hasta_x = self.img.width
				desde_x-= dif


			if desde_x <1 or hasta_x> self.img.width:
				desde_x = 1
				hasta_x = self.img.width


			if desde_y<1:
				dif= 1-desde_y

				desde_y = 1
				hasta_y+=dif

			if hasta_y > self.img.height:
				dif = hasta_y-self.img.height
				hasta_y = self.img.height
				desde_y-= dif


			if desde_y <1 or hasta_y> self.img.height:
				desde_y = 1
				hasta_y = self.img.height


			self.last_factor = (factor-1)
			self.last_center = [desde_x,desde_y]
			nw_imagen = self.img.crop((desde_x,desde_y,hasta_x,hasta_y))
			return Img(file = self.file,image = nw_imagen,size = (self.img.width,self.img.height))

		
	def zoom_to_tk(self,factor,mode = 0,**kwargs):
		new_img = self.zoom(factor,mode,**kwargs)
		if new_img != None:
			if mode != 0:
				imagen =  new_img.returnTk()
			else:
				imagen = ImageTk.PhotoImage(new_img)
			return imagen

	def concatenate_zoom(self,factor,mode,center):


		if self.last_center != None:
			print("vieja x",self.last_center[0],"nueva x",center[0])

			difx = self.last_center[0]+(center[0])
			dify = self.last_center[1]+(center[1])
			center = [difx,dify]

		if self.last_factor != None:
			factor = factor+self.last_factor 

		if factor<0: return self

		print("res x",center[0])
		return self.zoom(factor,mode = mode,center = center)
	def returnTk(self):
		if self.img == None:return
		return ImageTk.PhotoImage(self.img)

	def update(self,indice=None):
		if len(self.frames)>0:
			if isinstance(indice,int):
				self.actual_frame = indice

			self.img = self.frames[self.actual_frame]
			self.actual_frame+=1
			if not self.actual_frame<len(self.frames):
				self.actual_frame=0
			return self.img

	def set_frames(self):
		self.frames= []
		while 1:
			try:
				self.img.seek(self.img.tell()+1)
				self.frames.append(self.img.copy())
			except EOFError:
				self.img.seek(0)
				break # end of sequence



class MyTk(Tk):
	"""docstring for My_Tk"""
	def __init__(self,*args,**kwargs):
		super(MyTk, self).__init__(*args,**kwargs)


		self.minsize(width,height)

	def winfo_size(self):
		return [self.winfo_width(),self.winfo_height()]
#########
######### Functions
#########




###### Save in backup photos dispositions

def hold_disposition(grupo = "photos_names"):

	if len(photos) >0 and not lock:
		

		hndl = open(grupo+".pan","w")	
		for elemento in photos:
			url_s = elemento[0]
			if not isinstance(url_s,str) and url_s != None:
				try:
					url_s = url_s.file 
				except:
					print(url_s[1],"No se guardo")
					continue
			
			if len(re.split(r"\/|\\",url_s)) <= 1:
				url_s = os.getcwd()+"\\"+url_s
			
			hndl.write(url_s+"<>"+elemento[1]+"<>"+str(elemento[2])+"\n")
		
		hndl.close()

		messagebox.showinfo(message="Se guardo correctamente la disposicion")



###### Add url to photo database

def add_url_photo(url):
	if url != "":
		if not os.path.isfile(url):
			return False
		try:
			hndl = open(actual_grupo+".pan","r")
			lines = hndl.read().split("\n")
			hndl.close()

			urls= []

			for x in lines:
				ur = x.split(r"<>")[0]
				urls.append(ur)

			if len(re.split(r"\/|\\",url)) <= 1:
				url = os.getcwd()+"\\"+url
			
			if not url in urls:

				name_file = str(url.split(r"/")[-1])

				

				hndl = open(actual_grupo+".pan","a")
				hndl.write(url+"<>"+name_file+"<>1\n")
				hndl.close()
				return True
			
		except Exception as e:
			return False

		return url




###### load photo functions

def load_photos(group):
	global photos
	if not os.path.isfile(group):
		messagebox.showerror(message = "No se encontro el grupo que se queria ")
		return False

	photos = []

	hndl = open(group,"r")
	files = hndl.read().split("\n")
	hndl.close()




	for fil in files:
		fil = fil.split("<>")
		if fil[0] != "":
			photos.append([fil[0],fil[1],float(fil[2])])

	return True


###### Create image function

def create_image(url):
	if not os.path.isfile(url):
		print(url)
		return False
	imagen = Img(url)

	w = window.winfo_width()
	h = window.winfo_height()

	if w < width:
		w = width

	if h < height:
		h = height 

	imagen.adjust((w,h-65))

	return imagen



###### add new photo function

def add_photo():

	global photos,lock,indice,run_animation

	if lock:return
	
	names = filedialog.askopenfilenames(filetypes=["jpg .jpg","png .png","gif .gif","JPEG .JPEG","mytermination .pan"])
	for name in names:
		if isinstance(name,str) and os.path.isfile(name):
			add = add_url_photo(name)
			
			if add == None or not add:
				messagebox.showerror(message= "Error el archivo no fue encontrado.")
				continue

			if isinstance(add,str):
				continue


			photos.append([name,str(name.split(r"/")[-1]),1])
			
			indice = len(photos)-1
	run_animation = False
	window.after(70, show_photo)
	return True




def change_picture(label_element):
	global actual_foto,run_animation

	try:
		photos[indice][0].update()
		actual_foto = photos[indice][0].returnTk()
	except:
		pass
	label_element.config(text = photos[indice][1],image =actual_foto)
	
	if len(photos[indice][0].frames)>0 and run_animation:
		window.after(70,change_picture,label_element)

###### Show an picture function

def show_photo(index = None,label_element = None,**kwargs):
	global indice,actual_foto,Image_Label,photos,indice_shower,run_animation

	if index == None: #index
		index = indice


	if not len(photos) > index : return; # verifing
	
	if label_element == None: # label
		label_element = Image_Label

	if isinstance(photos[index][0],str): # Finalizate the photo load
		nuevo_content = create_image(photos[index][0])
		if not nuevo_content:
			return False

		photos[index][0] = nuevo_content
	

	# showing
	try:
		actual_foto = None
		if "zoom" in kwargs and "zoom_center" in kwargs:
			kwargs["zoom"] = kwargs["zoom"]/100
			actual_foto = photos[index][0].zoom_to_tk(kwargs["zoom"],mode = 1,center= kwargs["zoom_center"])



		if actual_foto == None:
			actual_foto = photos[index][0].returnTk()
	
	except Exception as e:
		print(e)
		photos.remove(photos[index])

		if indice == len(photos):
			indice-=1
		run_animation = False
		window.after(70, show_photo)
		return False

	try:
		
		photos[indice][0].update(0)
	except Exception as e:
		pass
	run_animation = True
	change_picture(label_element)	
	if label_element == Image_Label:
		img_name_label.config(text = photos[index][1])
		indice_shower.config(text=index+1) #changing index


###### advance automatic function grupo

def advance_automatic():
	global lock,random_next,indice,photos,advance_automatic_unite,run_animation
	
	while lock:
		if not lock:
			break

		time.sleep(photos[indice][2])

		if random_next:
			indice = randint(0,len(photos)-1)
		else:
			indice+=advance_automatic_unite
			if indice <0 :
				indice =len(photos)-1
			elif indice >= len(photos):
				indice = 0

		run_animation = False
		window.after(70, show_photo)








###### Change photo's index function

def cambiar_datos_de_imagen():
	global new_indice,new_name,new_duration
	error = False

	try : #verifying index
		nuevo_indice= new_indice.get()
		if nuevo_indice <=0 or nuevo_indice > len(photos):
			raise Exception("Burro")
	except:
		messagebox.showerror(message = "Error en el nuevo indice, ponga un valor valido.")
		error = True

	try : #verifying index
		nuevo_name= new_name.get()
		if nuevo_name == "" or re.match(r"\\|\/|:|\*|\?|\"|\'|\{|\}|<|>|\|",nuevo_name):
			raise Exception("Burro")
	except:
		messagebox.showerror(message = "Error en el nuevo nombre, ponga un valor valido.(sin <,>,:,/,\\,|,?,\",\'{,},*)")
		error = True


	try : #verifying index
		nueva_duracion= new_duration.get()
		if nueva_duracion <=0 or nueva_duracion > 15:
			raise Exception("Burro")
	except:
		messagebox.showerror(message = "Error en la nueva duracion, ponga un valor valido.(0 <duracion<= 15)")
		error = True

	if error:
		return
	# changing index

	name_add = ""

	if nuevo_name != photos[indice][1]:
		photos[indice][1] = nuevo_name
		name_add = "del nombre a '{}'".format(nuevo_name)

	duration_add = ""

	if nueva_duracion != photos[indice][2]:
		photos[indice][2] = nueva_duracion
		duration_add = "de la duracion a {} segundos".format(nueva_duracion)


	indice_add = ""

	if nuevo_indice-1 != indice:
		elemento = photos[indice]
		photos.remove(elemento)
		photos.insert(nuevo_indice-1,elemento)

		indice_add = "del indice a "+str(nuevo_indice)

	new_name.set(photos[indice][1])
	new_duration.set(photos[indice][2])

	run_animation = False

	window.after(70, show_photo) # reshowing



	message = "Se finalizo el cambio "
	data_p = " y ".join(list(filter(lambda x : x != "",[name_add,indice_add,duration_add])))

	if data_p != "":
		message+= data_p 
	else:
		message = "No se produjo ningun cambio"
	messagebox.showinfo(message = message)
###### cancel index change function

def cancelar_cambio():
	global lock,focus_control,cambiando_indice
	
	
	#hiding interface

	change_data_frame.pack_forget()	
	image_shower.pack_forget()

	display_main()
	# resetting vars
	focus_control = "Indefined"
	lock = False
	cambiando_indice = False


# o_btn.grid
def display_main():


	main_buttons.place(x = 5 , y = 5)

	
	indice_shower.grid(row = 0)
	img_name_label.grid(row = 1)
	Image_Label.grid(row = 2)

	image_shower.pack()


def change_interface_data():
	global lock,focus_control,cambiando_indice,new_name,new_indice

	if lock or posicionando_indice or invertir: 
		print("jpad")
		return

	main_buttons.place_forget()
	image_shower.pack_forget()



	indice_shower.grid_forget()
	img_name_label.grid_forget()
	image_shower.pack(side = LEFT)
	change_data_frame.pack(side = LEFT)


	# setting vars

	new_name.set(Image_Label.cget("text"))
	new_indice.set(indice+1)
	new_duration.set(photos[indice][2])
	# Setting layout of buttons

	Requesting_box.pack_forget()
	Requesting_box_name.grid_forget()
	Requesting_box_name.pack_forget()
	Requesting_box.grid_forget()
	Requesting_box_duration.grid_forget()

	Requesting_button.grid_forget()
	Requesting_cancel.grid_forget()	


	Requesting_box_name.grid(columnspan = 2,row = 0)
	Requesting_box_duration.grid(columnspan = 2,row = 1)
	Requesting_box.grid(columnspan =2,row = 2)

	Requesting_button.grid(column =0,row = 3,sticky = E)
	Requesting_cancel.grid(column = 1, row = 3,sticky =W)

	
	lock = True
	
	Requesting_box_name.focus_set()

	cambiando_indice = True



###### Keyboard management

def managePhoto(char):

	global indice,actual_foto,lock,focus_control,cambiando_indice,posicionando_indice,random_next,advance_automatic_unite,run_animation


	char = char.keycode
	if char == 39: # Right arrow process , movement in photo's display
		if len(photos) <= 0: return
		if not lock:
			if not random_next:
				indice +=1
				if indice >=len(photos):
					indice = 0
			else:
				indice = randint(0,len(photos)-1)

			if isinstance(photos[indice][0],Img):
				photos[indice][0].last_factor = None
				photos[indice][0].last_center = None


			run_animation = False

			window.after(70, show_photo)

	elif char == 37: # Left arrow process, movement in photo's display		
		if len(photos) <= 0: return
		if not lock:
			if not random_next:
				indice -=1
				if indice <0:
					indice = len(photos)-1
			else:
				indice = randint(0,len(photos)-1)

			if isinstance(photos[indice][0],Img):
				photos[indice][0].last_factor = None
				photos[indice][0].last_center = None

			run_animation = False

			window.after(70, show_photo)


	elif char == 13: #Return, Changing the index of a photo, setting images propertys and others...
		if len(photos) <= 0: return
		
		if not lock and not posicionando_indice and not creating_group and not invertir: # verifing, images property mode
			try:
				change_interface_data()
			except Exception as e:
				cancelar_cambio()
				raise e
		elif lock and cambiando_indice:# verifing, movement in widgets mode
			
			focus_control = window.focus_get()
			
			if focus_control == Requesting_button:
				Requesting_button.invoke()
			elif focus_control == Requesting_cancel:
				Requesting_cancel.invoke()

		elif lock and posicionando_indice:# verifing, movement in index mode
		
			try:
				nuevo =  new_indice.get()-1
				
				if nuevo <0 or nuevo>=len(photos):
					raise Exception("") 
				
				indice = nuevo

				if isinstance(photos[indice][0],Img):
					photos[indice][0].last_factor = None
					photos[indice][0].last_center = None
	

				lock = False
				posicionando_indice = False
				change_data_frame.pack_forget()

				run_animation = False

				window.after(70, show_photo)
			except:
				messagebox.showerror(message="Error con el indice, ponga uno valido.")
		elif lock and invertir:
			invertir_grupo()
	elif char == 69: # 'e', manually movement in images indexs
		if len(photos) <= 0: return
		if not lock and not creating_group and not cambiando_indice and not invertir:

			Requesting_box_duration.grid_forget()
			Requesting_box_name.grid_forget()
			Requesting_button.grid_forget()
			Requesting_cancel.grid_forget()
			Requesting_box.grid_forget()

			change_data_frame.pack()

			new_indice.set(indice+1)
			Requesting_box.pack()
			Requesting_box.focus_set()
			
			lock = True
			posicionando_indice = True
	
	elif char == 82: # 'r', setting random mode
		if lock: return

		if random_next:
			random_next = False
		else:
			random_next = True

	elif char == 83: # 's', setting automatic mode
		
		if len(photos) <= 0: return
		if not lock and not cambiando_indice and not posicionando_indice and not invertir and not creating_group:
			lock= True
			thhread_play = Thread(target=advance_automatic)
			thhread_play.start()
		else:
			if not cambiando_indice and not posicionando_indice and not creating_group and not invertir:
				lock = False
	elif char == 68: # 'd', changing direction in automatic mode
		if lock and not cambiando_indice and not posicionando_indice and not invertir and not creating_group:
			advance_automatic_unite*= -1
	elif char == 73:
		if len(photos) <= 0: return
		if not lock and not cambiando_indice and not creating_group and not posicionando_indice:
			invertir_interface()
	elif char == 32:
		if run_animation:
			run_animation = False
		else:
			change_picture(Image_Label)
	elif char == 80:
		if not run_animation:
			run_animation = True
			change_picture(Image_Label)
	else:
		print(char)
#		print(char)
		#print(window.winfo_size())



###### exit function

def exit_(*args,**kwargs):
	global lock,photos
	
	lock = False
	if len(photos) >0:
		hndl = open("photos_names","w")
		for elemento in photos:
			url_s = elemento[0]
			if not isinstance(url_s,str) and url_s != None:
				try:
					url_s = url_s.file 
				except:
					print(url_s[1],"No se guardo")
					continue
			
			if len(re.split(r"\/|\\",url_s)) <= 1:
				url_s = os.getcwd()+"\\"+url_s

			hndl.write(url_s+"<>"+elemento[1]+"<>"+str(elemento[2])+"\n")
		
		hndl.close()
		photos = []
	exit()




def resize_function(evento,**kwargs):
	global width,height,run_animation
	if (evento.width >= width or evento.height >= height) and len(photos)>0:
		run_animation = False

		window.after(70,change_picture,Image_Label)


def load_group(grupo_name):
	global actual_grupo,start_interface_frame,lock,run_animation,indice

	indice = 0

	loading= load_photos(grupo_name+".pan")

	if loading:
		start_interface_frame.pack_forget()
	
		del(start_interface_frame)
		start_interface_frame = Frame()
	
		display_main()


		lock = False
		actual_grupo = grupo_name
		actual_grupo_label.config(text =actual_grupo)

		run_animation = False
		window.after(70, show_photo)


def recover_sesion():
	if not os.path.isfile("photos_names"):
		hndl = open("photos_names","a+")
		hndl.close()

	handle = open("general.pan","w+")
	handleb = open("photos_names","r")

	handle.write(handleb.read())

	handle.close()
	handleb.close()

	load_group("general")

def display_start():
	global grupos



	funcion = lambda nombre : lambda :load_group(nombre)
	start_interface_frame.pack()
	if len(grupos) <= 0:
		recover_sesion()
		return
	for grupo in grupos:
		grupo = grupo.split(".")[0]
		Button(start_interface_frame,text = grupo,command = funcion(grupo)).pack()

	Button(start_interface_frame,text = "last session",command= recover_sesion).pack()

def load_grupos():
	global grupos,lock
	lock = True
	grupos = list(filter(lambda x :x.split(".")[-1]== "pan",glob.glob("*")))
	display_start()

def cargar_grupo():
	if not lock:
		main_buttons.place_forget()
		image_shower.pack_forget()
		change_data_frame.pack_forget()
		nuevo_grupo_frame.pack_forget()
		load_grupos()

def cancelar_la_creacion_de_grupo():
	global lock,creating_group

	lock = False
	creating_group = False
	display_main()
	nuevo_grupo_frame.pack_forget()

def nuevo_grupo_funct():
	global lock,creating_group

	if lock : return;

	if len(photos)<= 1:
		messagebox.showerror(message = "Imagenes insuficientes para hacer un grupo")
		return
	print("jp")
	lock = True
	creating_group = True
	
	main_buttons.place_forget()
	image_shower.pack_forget()


	nuevo_grupo_frame.pack()

	ngf_desde.set(1)
	ngf_hasta.set(len(photos))

	group_name_label.grid(row= 0,column = 0,sticky = E)
	group_name_box.grid(row= 0,column = 1,columnspan = 3,sticky = W)

	group_from_label.grid(row= 1, column = 0,sticky = E)
	ngf_desde_box.grid(row= 1,column = 1,sticky = W)

	group_to_label.grid(row= 1, column = 2,sticky = E)
	ngf_hasta_box.grid(row= 1,column = 3,sticky = W)


	ngf_confirm_btn.grid(row= 2,columnspan = 2)
	ngf_cancel_btn.grid(row = 2,column = 2,columnspan = 2)


def crear_grupo_nuevo():
	global nombre_del_grupo,ngf_desde,ngf_hasta
	global photos,indice,actual_grupo,run_animation

	nombre= nombre_del_grupo.get()
	desde = ngf_desde.get()
	hasta = ngf_hasta.get()

	error = False
	if nombre == "" or re.match(r"\\|\/|:|\*|\?|\"|\'|\{|\}|<|>|\|",nombre):
		error = True
		messagebox.showerror(message = "Nombre invalido , seleccione uno valido(sin <,>,:,/,\\,|,?,\",\'{,},*)")

	if desde <1 or desde > len(photos):
		messagebox.showerror(message = "minimo indice de foto invalido , seleccione uno entre 1 y {}".format(len(photos)-1))
		error = True

	if hasta <1 or hasta > len(photos):
		messagebox.showerror(message = "Maximo indice de foto invalido , seleccione uno entre 2 y {}".format(len(photos)))
		error = True

	if error:
		return

	if hasta - desde <0:
		messagebox.showerror(message = "No se selecciono un intervalo valido, el maximo indice tiene que ser mayor o igual al minimo")
		return

	arch = list(filter(lambda x: x.split(".")[-1] == "pan",glob.glob("*")))

	if nombre+".pan" in arch:
		messagebox.showerror(message = "Error ya hay un grupo con ese nombre.")
		return

	photos_necesarias = photos[slice(desde-1,hasta)]

	handle = open(nombre+".pan","w+")

	photos = []

	for elemento in photos_necesarias:
		url_s = elemento[0]
		if not isinstance(url_s,str) and url_s != None:
			try:
				url_s = url_s.file 
			except:
				print(url_s[1],"No se guardo")
				continue
			
		if len(re.split(r"\/|\\",url_s)) <= 1:
			url_s = os.getcwd()+"\\"+url_s

		handle.write(url_s+"<>"+elemento[1]+"<>1\n")

		photos.append(elemento)
	handle.close()

	actual_grupo = nombre
	actual_grupo_label.config(text =actual_grupo)
	
	indice = 0
	
	run_animation = False
	window.after(70, show_photo)
	cancelar_la_creacion_de_grupo()


def eliminar_grupo_funct():
	if actual_grupo == "general":
		messagebox.showerror(message="No se puede borrar el grupo 'general'.")
		return

	if os.path.exists(actual_grupo+".pan"):
		os.remove(actual_grupo+".pan")

	load_group("general")	


def eliminar_foto_funct():
	global indice,run_animation
	if not lock:
		photos.remove(photos[indice])

		if indice >= len(photos):
			indice = len(photos)-1

		run_animation = False
		window.after(70, show_photo)


def invertir_interface():
	global invertir,lock
	
	if lock :return

	lock = True
	invertir = True

	ngf_confirm_btn.grid_forget()
	ngf_cancel_btn.grid_forget()
	group_name_label.grid_forget()
	group_name_box.grid_forget()

	nuevo_grupo_frame.pack()


	ngf_desde.set(indice+1)
	ngf_hasta.set(indice+1)

	group_from_label.grid(row= 1, column = 0,sticky = E)
	ngf_desde_box.grid(row= 1,column = 1,sticky = W)

	group_to_label.grid(row= 1, column = 2,sticky = E)
	ngf_hasta_box.grid(row= 1,column = 3,sticky = W)

	ngf_desde_box.focus_set()	

def invertir_grupo():
	global photos,lock,invertir,run_animation

	nuevo_grupo_frame.pack_forget()
	lock = False
	invertir = False
	
	try:
		_from = ngf_desde.get()
		_to = ngf_hasta.get()

		if _from>len(photos) or _from<0:
			raise Exception("El indicador desde es invalido escoja un valor desde 1 hasta {}".format(len(photos)))

		if _to>len(photos) or _to<0:
			raise Exception("El indicador hasta es invalido escoja un valor desde 1 hasta {}".format(len(photos)))


		if _to-_from<0:
			raise Exception("No se puede invertir un intervalo negativo , el  indicador de hasta debe ser mayor que el de desde")

	except Exception as e:
		messagebox.showerror(message = str(e))
		return

	if _to-_from == 0:
		return

	nuevas_fotos = []
	for x in range(1,len(photos)+1):

		if _from<= x<= _to:
			nuevas_fotos.append(photos[_from+_to-x-1])
		else:
			nuevas_fotos.append(photos[x-1])

	photos = nuevas_fotos
	run_animation = False
	window.after(70, show_photo)

def add_zoom(mouse):
	global run_animation
	if photos[indice][0].last_factor != None:
		photos[indice][0].last_factor = None
		
		run_animation = False
		window.after(70, show_photo)
	else:
		run_animation = False
		window.after(70, lambda:show_photo(zoom = 200,zoom_center = [mouse.x,mouse.y]))


def destroy_img_display():
	global display_window
	display_window.destroy()
	display_window = None

#########
######### Variables
#########




###### Global Variables  

### constants

width,height = 631,698#GetSystemMetrics(0)-160,GetSystemMetrics(1)-50#1360,699
sleep_time = 3

images_extensions = ["jpg","png","jpeg","gif"]
images_names = list(filter(lambda x: x.split(".")[-1] in images_extensions, glob.glob("*")))
cantidad_fotos = len(images_names)


### variables
minimo_indice = 0 ## restrict to photos show index.
maximo_indice = cantidad_fotos

window = MyTk() # window creating
window.geometry("{w}x{h}+70+0".format(w=width,h=height))
window.title("Testing2")


photos = [] # photo's control vars
actual_foto = None
indice = 0
lock = True
random_next = False
posicionando_indice= False
cambiando_indice = False
creating_group = False
invertir = False
run_animation = True
advance_automatic_unite = 1

# show_photo

# group control

actual_grupo = ""
grupos = []

### tkinter elements

#start 
start_interface_frame= Frame(window,name = "startFrame")
start_msg_label = Label(start_interface_frame,text = "Elegi el grupo que quieras")

# Main
image_shower = Frame(window,name = "main_frame")

indice_shower= Label(image_shower,text="1",name="indice_shower") #labels
Image_Label = Label(image_shower,name = "label_image")
img_name_label = Label(image_shower,name="image_name")





#  Support

main_buttons = Frame(window,name ="main_btns")

actual_grupo_label = Label(main_buttons,text = "Sin grupo")
add_photo_btn = Button(main_buttons,text="Add photo",command= add_photo,name = "addp") 
eliminar_foto_btn= Button(main_buttons,text = "eliminar foto",command = eliminar_foto_funct,name = "del_f")
save_dispocision_btn = Button(main_buttons,text="save disposition",command=lambda: hold_disposition(actual_grupo),name = "save_p")
nuevo_grupo_btn= Button(main_buttons,text = "nuevo grupo",command = nuevo_grupo_funct,name = "new_g")
eliminar_grupo_btn= Button(main_buttons,text = "eliminar grupo",command = eliminar_grupo_funct,name = "del_g")
load_grupo_btn= Button(main_buttons,text = "cambiar grupo",command = cargar_grupo,name = "change_g")



# Change photo data 

#buttons

change_data_frame = Frame(window,name = "datachange")
Requesting_button = Button(change_data_frame,text="cambiar",command= cambiar_datos_de_imagen,name = "do")
Requesting_cancel = Button(change_data_frame,text="cancelar",command= cancelar_cambio,name = "cancel")


new_indice = IntVar() #Entrys and entrys vars
Requesting_box = Entry(change_data_frame,textvariable=new_indice,name = "index_box")

new_name = StringVar() #Entrys and entrys vars
Requesting_box_name = Entry(change_data_frame,textvariable=new_name,name = "name_box")

new_duration = IntVar()
Requesting_box_duration = Entry(change_data_frame,textvariable =new_duration,name = "duration_box")

# New group interface
nuevo_grupo_frame = Frame(window,name = "newgroup")

group_name_label = Label(nuevo_grupo_frame,text = "Group name:") 
group_from_label = Label(nuevo_grupo_frame,text = "From:") 
group_to_label = Label(nuevo_grupo_frame,text = "To:") 

ngf_desde = IntVar()

ngf_hasta = IntVar()

nombre_del_grupo = StringVar()

group_name_box = Entry(nuevo_grupo_frame,textvariable = nombre_del_grupo)
ngf_desde_box = Entry(nuevo_grupo_frame,textvariable = ngf_desde,name = "ngf_desde",width = 6) 
ngf_hasta_box = Entry(nuevo_grupo_frame,textvariable = ngf_hasta,name = "ngf_hasta",width = 6) 

ngf_confirm_btn = Button(nuevo_grupo_frame,text = "crear",command = crear_grupo_nuevo,width = 15)
ngf_cancel_btn = Button(nuevo_grupo_frame,text = "cancelar",command = cancelar_la_creacion_de_grupo,width = 15)


###### display elements

actual_grupo_label.grid(row = 0,sticky = W)
add_photo_btn.grid(row = 1,sticky = W)
eliminar_foto_btn.grid(row =2,sticky = W)
nuevo_grupo_btn.grid(row = 3,sticky = W)
eliminar_grupo_btn.grid(row = 4,sticky = W)
load_grupo_btn.grid(row = 5,sticky = W)
save_dispocision_btn.grid(row = 6,sticky = W)



###### set event handlers

window.bind("<KeyPress>",managePhoto)
window.bind('<Escape>',exit_)
window.bind('<Configure>',resize_function)


display_window = None
foto = None
mouse_moved = False
clicked_coords = None
showing_foto = None
last_x, last_y = 0,0
w_image = 0
h_image = 0
factor_add= 0
lst_center_y = None
lst_center_x = None
lst_factor = 0

def eximg_click(mouse):
	global clicked_coords

	clicked_coords = [mouse.x,mouse.y]


def eximg_motion(mouse):
	global mouse_moved,lst_center_y,lst_center_x,last_x,last_y


	mouse_moved = True

	label = display_window.winfo_children()[0]


	if lst_center_x == int(display_window.winfo_width()/2):
		lst_center_x *=2

	if lst_center_y == int(display_window.winfo_height()/2):
		lst_center_y *=2

	if 0<(mouse.x-clicked_coords[0])+ lst_center_x-int(display_window.winfo_width()/2)<abs(w_image):
		difx = (last_x+(mouse.x-clicked_coords[0]))
		last_x = difx
		lst_center_x = lst_center_x+(mouse.x-clicked_coords[0])
		label.place(x = last_x)
	
	if  0<(mouse.y-clicked_coords[1])+ lst_center_y-display_window.winfo_height()/2<abs(h_image):
	
		dify = (last_y+(mouse.y-clicked_coords[1]))
		last_y = dify
		lst_center_y = lst_center_y+(mouse.y-clicked_coords[1])
		label.place(y = last_y)



def eximg_release(mouse):
	global mouse_moved,showing_foto,last_x,last_y,w_image,h_image,factor_add,lst_center_x,lst_center_y,lst_factor
	if mouse_moved:
		mouse_moved = False
		return

	factor_add =0
	showing_foto = foto.zoom(factor = factor_add,mode = 0)

	w_image = showing_foto.width
	h_image = showing_foto.height

	showing_foto = ImageTk.PhotoImage(showing_foto)

	label = display_window.winfo_children()[0]
	label.config(image = showing_foto)


	if lst_center_x != None and lst_center_y != None:
		print("lllllllll",last_x,mouse.x,lst_center_x,(factor_add-lst_factor+1))
		last_x = -(factor_add-lst_factor+1)*(mouse.x)+w_image/2
		#last_x = w_image-(factor_add-lst_factor+1)*mouse.x
		last_y = -(factor_add-lst_factor+1)*(mouse.y)+h_image/2
		print(last_x)
	else:
		lst_center_x =  int(display_window.winfo_width()/2)
		lst_center_y =  int(display_window.winfo_height()/2)
		
		print("ssss",lst_center_x,last_x,mouse.x)
		last_x = (last_x+lst_center_x-mouse.x)*(factor_add+1)-int(display_window.winfo_width()/2)*factor_add
		last_y = (last_y+lst_center_y-mouse.y)*(factor_add+1)-int(display_window.winfo_height()/2)*factor_add
		print(last_x)
	lst_center_x = w_image/2-last_x
	lst_center_y = h_image/2-last_y
	lst_factor = factor_add
	label.place(x =last_x,y =last_y)




def display_image(*args):
	global display_window,foto,showing_foto,w_image,h_image,lst_center_x,lst_center_y
	if display_window != None:return
	if isinstance(photos[indice][0],str) :return

	foto = Img(file = photos[indice][0].file,image = photos[indice][0].img)

	foto.adjust((width,height))

	display_window = Toplevel(window,name = "foto_toplevel")

	display_window.resizable(False,False)

	display_window.geometry("{w}x{h}+770+0".format(w = foto.img.width,h = foto.img.height))
	w_image = foto.img.width
	h_image = foto.img.height


	lst_center_x = int(foto.img.width/2)
	lst_center_y = int(foto.img.height/2)

	showing_foto = foto.returnTk()
	photo_exclusive_label = Label(display_window,image= showing_foto,name = "photo_label")


	photo_exclusive_label.place(x = 0,y = 0)

	cc = Frame(display_window,width = 10,height= 10 , bg= "#f21fff")

	cc.place(x = lst_center_x,y = (lst_center_y))


	print(foto.img.width,foto.img.height)

	display_window.bind("<B1-Motion>",eximg_motion)
	display_window.bind("<Button-1>",eximg_click)
	photo_exclusive_label.bind("<ButtonRelease-1>",eximg_release)
	photo_exclusive_label.bind("<ButtonRelease-3>",eximg_release)
	display_window.protocol("WM_DELETE_WINDOW",destroy_img_display)
	display_window.bind("<Escape>",lambda *args:destroy_img_display())
	display_window.bind("<Return>",lambda *args:print("x>:",lst_center_x,"y>:",lst_center_y,"y:",last_y,"x:",last_x))
	display_window.tkraise()

Image_Label.bind('<Button-1>',add_zoom)
Image_Label.bind('<Button-3>',display_image)
###### Initing loop


load_grupos()

window.mainloop()



###### hold new positions, and finalizating
exit_()
