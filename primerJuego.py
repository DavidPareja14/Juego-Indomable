'''
Este programa me permite controlar la gravedad del jugador, me permite posicionarlo en una plataforma y controla los limites.

-- if jp.rect.y>=elemento.rect.y-jp.rect.h and jp.rect.y<=elemento.rect.y+(elemento.rect.h/1.2)-jp.rect.h: es para detectar si el objeto o
jugador esta callendo desde arriba a la plataforma, se hace de esta manera, ya que cuando spritecollide detecta la colision, no lo
hace justo cuando el objeto toca la plataforma, por eso toca establecer un rango.

en el grupo PERROS va a estar los lobos, la explosion
en el grupo GENERAL va a estar mi jugador
en el grupo PISTOLAS va a estar las dos pistolas
en el grupo balas va a estar las balas del jugador y la de las pistolas.
en el grupo struc_mapa van a estar los bloques
'''

import pygame
import random	
import ConfigParser
from pacmanMalo import *

ANCHO = 800
ALTO = 600

NEGRO    = (   0,   0,   0)
BLANCO   = ( 255, 255, 255)
AZUL     = (   0,   0, 255)
ROJO     = ( 255,   0,   0)
VERDE    = (   0, 255,   0)
AMARILLO = ( 255, 255,   0)

class Jugador(pygame.sprite.Sprite):

	def __init__(self, m):
		pygame.sprite.Sprite.__init__(self)
		self.dir=0
		self.m=m
		self.image=self.m[self.dir][0]
		self.rect = self.image.get_rect()
		self.varx=0
		self.vary=0
		self.rect.y=ALTO-self.rect.h
		self.x=-1 #inicializo con este valor para que la imagen no se quede moviendo
		self.col=4 #me va a dar el numero de columnas que me debo desplazar para mostrar las img de una fila

	def gravedad(self):
			if self.vary==0:
				self.vary=1
			else:
				self.vary+=1.5

	def update(self):
		self.gravedad()
		self.rect.x+=self.varx
		if self.x!=-1:
			if self.x<self.col:
				self.image=self.m[self.dir][self.x]
				self.x+=1
			elif self.x!=0: #Puse esta condicion porque si solo pongo el else, lo toma como si fuera del primer if, esto esta mal, NO ENTIENDO QUE PASA!
				self.x=0
	        
		self.rect.y+=self.vary
		if self.rect.x>ANCHO-self.rect.w:
			self.rect.x=ANCHO-self.rect.w
		if self.rect.y>ALTO-self.rect.h:
			self.rect.y=ALTO-self.rect.h
		if self.rect.x<0:
			self.rect.x=0
		if self.rect.y<0:
			self.vary=0
			self.rect.y=0

class Muros(pygame.sprite.Sprite):
    def __init__(self, img,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=img
        self.rect=self.image.get_rect()
        self.rect.x=x 
        self.rect.y=y 

class Barra(pygame.sprite.Sprite):
    def __init__(self,img,x,y,var):
        pygame.sprite.Sprite.__init__(self)
        self.image=img
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y 
        self.varx=var

    def update(self):
		self.rect.x+=self.varx
		if self.rect.x>=ANCHO+200:
			self.rect.x=-200

class PerroRival(pygame.sprite.Sprite):
    def __init__(self,m,y,var,parametro):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.image=self.m[1][0]
        self.rect=self.image.get_rect()
        self.rect.x=ALTO+parametro
        self.rect.y=y
        self.varx=var
        self.x=0

    def update(self):
    		self.rect.x+=self.varx
    		if self.x<6:
    			self.image=self.m[1][self.x]
    			self.x+=1
    		else:
    			self.x=0
    		if self.rect.x<-200:
    			self.rect.x=ANCHO+200

class Proyectil(pygame.sprite.Sprite):
    def __init__(self,varx,vary,img,desc):
        pygame.sprite.Sprite.__init__(self)
        self.image=img
        self.rect=self.image.get_rect()
        self.var_y=vary
        self.var_x=varx
        self.des=desc #me permite decidir cuales balas van a cierta posicion en pantalla.
        self.decision=0 #va a ser inportante para saber la direccion de las balas cuando despause el juego.

    def update(self):   #modifica la pos del rival.
        self.rect.y+=self.var_y
        self.rect.x+=self.var_x
        if self.des==1:
	        if self.rect.x>ANCHO:
	        	self.rect.x=70

class Explosion(pygame.sprite.Sprite):

	def __init__(self, m,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.dir=0
		self.m=m
		self.image=self.m[0][0]
		self.rect = self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		self.x=0

	def update(self):
		if self.x!=-1:
			if self.x<4:
				self.image=self.m[0][self.x]
				self.x+=1
			elif self.x!=0: #Puse esta condicion porque si solo pongo el else, lo toma como si fuera del primer if, esto esta mal, NO ENTIENDO QUE PASA!
				self.x=0

def Recorte(imagen,sp_fil,sp_col,ancho_img,alto_img): # funcion que me retorna una matriz con todos los recortes hechos a una imagen.
	an_img_recorte=ancho_img/sp_col
	al_img_recorte=alto_img/sp_fil
	matriz = []
	for i in range(sp_fil):
		matriz.append([])
		for j in range(sp_col):
			cuadro=(j*an_img_recorte,i*al_img_recorte,an_img_recorte,al_img_recorte) #posicion del recorte de la imagen
			recorte=imagen.subsurface(cuadro) #me va a tener el recorte de cierta posicion de una imagen
			matriz[i].append(recorte)
	return matriz

def mapa(recorte1,recorte2,an_img_recorte1,al_img_recorte1,an_img_recorte2,al_img_recorte2):
	interprete=ConfigParser.ConfigParser()
	interprete.read('mapa.map') #La variable interprete me va a leer el mapa
	dicc={}	
	for seccion in interprete.sections():
		descripcion=dict(interprete.items(seccion))
		dicc[seccion]=descripcion

	mapa=dicc['nivel1']['mapa']
	lineas=mapa.split('\n')
	plataformas=pygame.sprite.Group() #Grupo que me va a contener todos los recortes con respecto al mapa.
	pistolas=pygame.sprite.Group() #Grupo que me va a contener todos los recortes con respecto al mapa de pistolas.
	for pos,n in enumerate(lineas):    #Estos ciclos me permiten establecer las posiciones de cada recorte y ademas, me reemplaza
		for indice,elem in enumerate(lineas[pos]): #los simbolos del mapa por imagenes reales, cada recorte lo agrego a un grupo,
			if elem=='$':                          #para luego dibujar el mapa de una.
				mr=Muros(recorte1,an_img_recorte1*indice,al_img_recorte1*pos)
				plataformas.add(mr)
			elif elem=='p':
				mr=Muros(recorte2,-50,31*pos)#defino los valores, ya que las armas tienen medidas diferent a los muros.
				pistolas.add(mr)

	return [plataformas,pistolas]

def main1():
	pygame.init()
	ventana=pygame.display.set_mode([ANCHO,ALTO],pygame.FULLSCREEN)
	#GRUPOS, FALTAN CREO QUE DOS, LOS CUALES ESTAN EN LA PARTE DE ABAJO.
	general=pygame.sprite.Group()
	perros=pygame.sprite.Group()
	balas=pygame.sprite.Group()
	global nivel #a nivel lo estoy manejando de manera global.

	#SONIDOS
	gr=pygame.mixer.Sound('grito.ogg')
	ninos=pygame.mixer.Sound('ni_os.ogg')
	d=pygame.mixer.Sound('disparo.oga')
	ex=pygame.mixer.Sound('explosion.ogg')
	derrota=pygame.mixer.Sound('derrota.ogg')
	wp=pygame.mixer.Sound('warPigs.ogg')
	wp.play()
	am=pygame.mixer.Sound('ametralladora.ogg')
	am.play(-1)
	am.set_volume(0.2)
	l=pygame.mixer.Sound('Ladridos.ogg.ogx')
	l.play(-1) #Hago que los ladridos se repitan indefinidamente
	l.set_volume(0.3)
	imag=pygame.image.load('sold.png').convert_alpha()
	ancho_img,alto_img=imag.get_size()
	sp_fil=4
	sp_col=4
	m=Recorte(imag,sp_fil,sp_col,ancho_img,alto_img)
	#Muro seran las imagenes que se cargaran en mi mapa.
	muro=pygame.image.load('terrenogen.png').convert()
	ancho_img1,alto_img1=muro.get_size()
	sp_fil1=12
	sp_col1=32
	cuadro=((ancho_img1/sp_col1)*22,(alto_img1/sp_fil1)*3,ancho_img1/sp_col1,alto_img1/sp_fil1) #22 es el num de img horizontalmente hasta la que quiero cortar y 3 contando vertical.
	recorte1=muro.subsurface(cuadro) #me va a tener el recorte de cierta posicion de una imagen
	muro=pygame.image.load('armas.png').convert()
	ancho_img2,alto_img2=muro.get_size()
	sp_fil2=5
	sp_col2=5
	cuadro=((ancho_img2/sp_col2)*4,0,ancho_img2/sp_col2-50,alto_img2/sp_fil2-20) 
	recorte2=muro.subsurface(cuadro) #me va a tener el recorte de cierta posicion de una imagen

	estruc_map,pistolas=mapa(recorte1,recorte2,ancho_img1/sp_col1,alto_img1/sp_fil1,ancho_img2/sp_col2,alto_img2/sp_fil2) #------------

	barra=pygame.image.load('barra.jpg').convert()
	cuadro=(0,10,150,20) 
	recorte=barra.subsurface(cuadro) #me va a tener el recorte de cierta posicion de una imagen
	br=Barra(recorte,-200,412,4)
	estruc_map.add(br) #meto la barra en este grupo para que tenga las mismas propiedades que los muros con el jugador

	perro=pygame.image.load('lobo.png').convert_alpha()
	ancho_img,alto_img=perro.get_size()
	sp_fil=6
	sp_col=9
	m2=Recorte(perro,sp_fil,sp_col,ancho_img,alto_img)
	pr=PerroRival(m2,ALTO-60,-10,0) #Para el perro de la parte inferior
	perros.add(pr)
	for i in range(3): #creo los 3 perros de la parte superior
		pr=PerroRival(m2,ALTO-500,-15,(i+1)*370) #380 para que haya espacio entre los perros.
		perros.add(pr)

	disp=pygame.image.load('disparo.png').convert_alpha() #utilizo el primer sprite de la img para usarlo como disparo
	cuadro=(15,30,15,5) 
	recorte=disp.subsurface(cuadro) #me va a tener el recorte de cierta posicion de una imagen

	enter=pygame.image.load('enter.png')

	for i in range(25): #Van a ser las balas que me dispara la prier pistola
		b=Proyectil(10,0,recorte,1)
		b.rect.x=70+(i*30)
		b.rect.y=390
		balas.add(b)

	for i in range(3): #Van a ser las balas que me dispara la prier pistola
		b=Proyectil(3,0,recorte,1)
		b.rect.x=70+(i*30)
		b.rect.y=330
		balas.add(b)

	disp=pygame.image.load('disparo.png').convert_alpha() #utilizo el primer sprite de la img para usarlo como disparo
	cuadro=(15,15,35,35) 
	recorte=disp.subsurface(cuadro) #me va a tener el recorte de cierta posicion de una imagen

	imag=pygame.image.load('explosion1.png').convert_alpha()
	ancho_img,alto_img=imag.get_size()
	sp_fil=4
	sp_col=4
	m2=Recorte(imag,sp_fil,sp_col,ancho_img,alto_img)


	jp=Jugador(m)
	general.add(jp)
	

	imagen=pygame.image.load('fondo3.jpg')
	imagen2=pygame.image.load('meta.png')

	reloj=pygame.time.Clock()
	aux=0 #Me va a servir para saber cuando hacer un salto, para cuando deje de presionar una tecla, el salto se ejecute bien.
	t_seg=0
	fin = True
	control_salto=0 #doy el tiempo para que el objeto salte y despues se detenga, asi deja de avanzar.
	decision=1 #Me permite disparar hacia la direccion correcta.
	contBalas=0 #Me va a contar las balas que impacta a cada pistola
	control_vidas=0 #Me va a permitir aumentar o disminuir las vidas.
	vidas=3
	puntos=0 #si destruyo las dos armas, son dos puntos y gano vida.
	fuente=pygame.font.Font(None,30)
	pausa=0
	eliminar_balas=0
	aux_t=0 #Para controlar bien el tiempo cuando pause el juego.
	aux_t2=0 #Va a ser el tiempo real que el jugador lleva jugando.

	while fin:
		tiempo=pygame.time.get_ticks()/1000 #divido entre 1000 porque 1s son 1000ms y get_ticks me devuelve en ms.
		#print tiempo
		if tiempo-4==t_seg: #le resto 3 porque el tiempo esta empezando en 3
			t_seg+=1
			aux_t2+=1
			if pausa==1:
				aux_t+=1

		ls_col1=pygame.sprite.spritecollide(jp,estruc_map,False)
		ls_col2=pygame.sprite.spritecollide(jp,balas,False)
		ls_col3=pygame.sprite.spritecollide(jp,perros,False)
		for elemento in ls_col1:
			if jp.rect.y>=elemento.rect.y-jp.rect.h and jp.rect.y<=elemento.rect.y+(elemento.rect.h/1.001)-jp.rect.h: #--
				jp.vary=0
				aux=2 #Para que el jugador pueda saltar en una plataforma.
				jp.rect.y=elemento.rect.y-(jp.rect.h+int(0.1)) #hago que el jug quede 0.1 pixel arriba de la plataforma.
			else:
				jp.vary=0 #el jugador empieza a descender.
				jp.aux=0 #habilito la gravedad
				jp.rect.y=elemento.rect.y+(jp.rect.h+1) #hago que el jug quede un pixel abajo de la plataforma.

		for elemento in ls_col2:
			control_vidas=1
			gr.play()

		for elemento in ls_col3:
			control_vidas=1
			gr.play()

		if control_vidas==1: #-----------------vidas----------
			vidas-=1
			jp.rect.x=500
			jp.rect.y=432
			control_vidas=0
			jp.vary=0

		if control_vidas==2:
			puntos+=1
			control_vidas=0

		if puntos==2:
			vidas+=1
			puntos=0

		if vidas==0:
			derrota.play()
			texto=fuente.render("FIN DEL JUEGO",True,BLANCO)
			texto4=fuente.render("TIEMPO TOTAL: "+str(aux_t2)+"s",True,BLANCO)
			texto6=fuente.render("MAXIMO NIVEL: "+str(nivel),True,BLANCO)
			ventana.fill(NEGRO)
			ventana.blit(texto,[300,200])
			ventana.blit(texto4,[300,250])
			ventana.blit(texto6,[300,300])
			wp.stop()
			am.stop()
			l.stop()
			pygame.display.flip()
			reloj.tick(0.3)
			fin=False

		for b in balas:
			ls_col4=pygame.sprite.spritecollide(b,estruc_map,False)
			for e in ls_col4:
				balas.remove(b)

		for b in balas:
			ls_col=pygame.sprite.spritecollide(b,perros,False)
			for e in ls_col:
				balas.remove(b)

		for b in balas:
			ls_col5=pygame.sprite.spritecollide(b,pistolas,False)#estos for son para que despues de 50 disparos se quite la pistola 
																 #y tambien para que se quiten las balas q dispara cada pistola
			for e in ls_col5:
				contBalas+=1
				balas.remove(b)
				if contBalas==2:
					if e.rect.y>=300 and e.rect.y<=320:
						eliminar_balas=2
						expl=Explosion(m2,0,300)
						perros.add(expl)
						ex.play()
						control_vidas=2
					elif e.rect.y>=362 and e.rect.y<=382:
						eliminar_balas=1
						expl=Explosion(m2,0,372)				#tambien utilizo esta parte(los ciclos) para meter la explosion
						perros.add(expl)
						am.stop()
						ex.play()
						control_vidas=2
					contBalas=0
					pistolas.remove(e)							#----------------
			if eliminar_balas==1:                               
				for bal in balas:
					if bal.rect.y>=380 and bal.rect.y<=400:							#----------------
						balas.remove(bal)						#----------------
			if eliminar_balas==2:
				for bal in balas:								
					if bal.rect.y>=320 and bal.rect.y<=340:  	#----------------
						balas.remove(bal)						#----------------
					


		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				fin=False
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_LEFT and pausa==0:
					jp.varx=-5
					aux=0
					jp.col=4
					jp.dir=1
					jp.x=0
					decision=2
				if evento.key == pygame.K_RIGHT and pausa==0:
					jp.varx=5
					aux=0
					jp.col=4
					jp.dir=2
					jp.x=0
					decision=1
				if evento.key == pygame.K_p: #me va a permitir un atajo, para pasar mi primer nivel mas facil
					jp.rect.x=20
					jp.rect.y=20
					eliminar_balas=2
					for b in balas:
						balas.remove(b)
				if evento.key == pygame.K_d and pausa==0: #Para disparar
					d.play()
					if decision==1:
						b=Proyectil(5,0,recorte,0)
						posDisparox=jp.rect.w+1
						b.decision=1
					elif decision==2:
						b=Proyectil(-5,0,recorte,0)
						posDisparox=-36
						b.decision=2
					elif decision==3:
						b=Proyectil(0,-5,recorte,0)
						posDisparox=-36
						b.decision=3
					b.rect.x=jp.rect.x+posDisparox
					b.rect.y=jp.rect.y+10 #para que el tiro sea mas acorde con la pos del jugador
					balas.add(b)#a es para pausar el juego.
				if evento.key == pygame.K_a:
					ventana.blit(enter,[300,200]) #---------------------------------ERROR----------------no muestra la imagen
					pausa=1
					pygame.mixer.pause()
					for b in balas:		#a todos mis objetos los pauso.
						b.var_x=0
					for p in perros:
						p.varx=0
					br.varx=0
					pygame.display.flip()
					
				if evento.key == pygame.K_RETURN and pausa==1: #despausa el juego.
					pausa=0
					if eliminar_balas==1 or eliminar_balas==2:
						pass
					else:
						am.set_volume(0.3)
					pygame.mixer.unpause()
					for b in balas:
						if b.rect.y==330:
							b.var_x=3
						elif b.rect.y==390:
							b.var_x=10
						elif b.decision==1:  #------------------------prestar atencion a decision, puede que este disparando a todas
							b.var_x=5      #partes, y decision me devia todas las balas a la misma direccion.
						elif b.decision==2:
							b.var_x=-5
						elif b.decision==3:
							b.var_y=-5
					for p in perros:
						if p.rect.y==ALTO-60:
							p.varx=-10
						elif p.rect.y==ALTO-500:
							p.varx=-15
					br.varx=4
					aux_t2=aux_t2-aux_t
					aux_t=0
				if evento.key == pygame.K_UP and pausa==0:
					aux=0
					jp.col=4
					jp.dir=3
					jp.x=0
					decision=3

				if evento.key == pygame.K_SPACE and pausa==0:
					if jp.rect.y>=ALTO-jp.rect.h or aux==2: #Esta cond es para que solo salte una vez si esta en el aire.
						jp.vary=-20
						aux=1
						jp.aux=0 #habilito la gravedad.
				if evento.key == pygame.K_ESCAPE:
					fin=False

			if evento.type == pygame.KEYUP:
				if aux!=1:
					jp.varx=0
					jp.vary=0
					jp.x=-1

		for b in balas: #--------------ELIMINO LAS BALAS QUE VAN A SALIR POR EL TECHO--para las lateralas hay un muro que no se ve.
			if b.rect.y<0: 
				balas.remove(b)

		for b in balas:     #Es para que suene las balas del pistolon de arriba.
			if b.rect.y==330 and b.rect.x>=ANCHO-b.rect.w:
				d.play()

		if pausa==0:
			
			balas.update()
			general.update()
			perros.update()
			br.update()
			ventana.blit(imagen,[0,0])
			ventana.blit(imagen2,[5,64])
			texto2=fuente.render("Nivel: "+str(nivel)+"   Vidas: "+str(vidas)+"  Tiempo: "+str(aux_t2)+"   Puntos: "+str(puntos),True,BLANCO)
			ventana.blit(texto2,[400,5])
			general.draw(ventana)
			balas.draw(ventana)
			perros.draw(ventana)
			pistolas.draw(ventana)
			estruc_map.draw(ventana)
			reloj.tick(35)
			pygame.display.flip()

		if jp.rect.x<=100 and jp.rect.y<=150 and eliminar_balas==2:  #-----------------VICTORIA----------------------------
			nivel=2
			ninos.play()
			texto=fuente.render("FELICITACIONES",True,BLANCO)
			texto4=fuente.render("SIGUIENTE NIVEL",True,BLANCO)
			pac=pygame.image.load("pacman.jpg").convert()
			ventana.blit(pac,[0,0])
			ventana.blit(texto,[450,360])
			ventana.blit(texto4,[450,410])
			wp.stop()
			am.stop()
			l.stop()
			pygame.display.flip()
			reloj.tick(0.2)
			ninos.stop()
			fin=False

	return [jp,general,balas,decision,d,recorte,b,tiempo,vidas]

if __name__==	'__main__':
	nivel=1
	if nivel==1:
		lista=main1()
	if nivel==2:
		lista[0].rect.y=ALTO-lista[0].rect.h
		lista[0].rect.x=ANCHO-lista[0].rect.w
		main2(lista)
