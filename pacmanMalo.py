import pygame
import math
from random import *
from primerJuego import *
'''
Este programa me permite desplazar un sprite en pantalla desde una posicion inicial hasta una posicion dada por el cursor.
'''
ANCHO = 800
ALTO = 600
AZUL = (0,0,255)
ROJO = (255,0,0)
VERDE = (0,255,0)
BLANCO = (255,255,255)
NEGRO = (0,0,0)

class Pacman(pygame.sprite.Sprite):
    def __init__(self, m):
        pygame.sprite.Sprite.__init__(self)
        self.dir=0
        self.m=m
        self.image=self.m[self.dir][0]
        self.rect=self.image.get_rect()
        self.var_x=5 #que tantos pixeles se mueve en x
        self.x=0 #me va a permitir recorrer cada columna de mi matriz
        self.pen=0 #para la pendiente de la ecuacion
        self.inter=0 # calcula el intercepto de la ecuacion
        self.p1=0  #posicion 1 del mouse
        self.p2=0  #posicion 2 del mouse
        self.controlTiempo=0 #si esta en 0, pac se movera en la parte de arriba, si es uno, perseguira al jugador.

    def update(self):
        self.rect.x+=self.var_x
        if self.x<3:
        	self.image=self.m[self.dir][self.x] #Me permite visualizar el movimiento de cada img (columna) segun la fila.
        	self.x+=1
        else:
	        self.x=0

        if self.controlTiempo==0: #controlo la movencion en Y y el desplazamiento en x
            self.rect.y=0
            if self.rect.x>=ANCHO-self.rect.w:
                self.var_x=-5
                self.dir=1
            elif self.rect.x<=0:
                self.var_x=5
                self.dir=0
        elif self.controlTiempo==1:
            if self.pen>=50 and self.pen<=600:
                self.rect.y=-50
            elif self.pen<=-50 and self.pen<=600:
                self.rect.y=50
            else:
                self.rect.y=int(self.pen*self.rect.x+self.inter)

        if self.rect.y>=ALTO-self.rect.h:
            self.rect.y=ALTO-self.rect.h
        elif self.rect.y<=0:
            self.rect.y=0
        elif self.rect.x>=ANCHO-self.rect.w:
            self.rect.x=ANCHO-self.rect.w
        elif self.rect.x<=0:
            self.rect.x=0
        
    def Pendiente(self):
        if self.rect.x-self.p1==0:
            self.pen=self.rect.y-self.p2
        else:
            self.pen=(float(self.rect.y-self.p2))/(float(self.rect.x-self.p1))
        self.inter=float(self.pen*(-self.p1)+self.p2)

class Fantasmas(pygame.sprite.Sprite):
    def __init__(self, m,posxImg,posx,posy):
        pygame.sprite.Sprite.__init__(self)
        self.posx_fant=posxImg
        self.m=m
        self.image=self.m[1][0]
        self.rect=self.image.get_rect()
        self.var_x=0 #que tantos pixeles se mueve en x
        self.var_y=0
        self.x=posxImg #me va a permitir recorrer cada columna de mi matriz
        self.rect.x=posx
        self.rect.y=posy
        self.cont_balas=0 #me permite saber cuantas balas han colisionado con cada fantasma, para luego eliminarlo.
        self.dir=0 #al momento de pausar el juego, voy a tener las direcciones de cada fantasma.
        self.pausa=0 #si pauso el juego, deja de actualizar las direcciones.

    def update(self):
        self.rect.x+=self.var_x
        self.rect.y+=self.var_y
        if self.x<self.posx_fant+2:
            self.image=self.m[1][self.x] #Me permite visualizar el movimiento de cada img (columna) segun la fila.
            self.x+=1
        else:
            self.x=self.posx_fant

        if self.rect.x>=ANCHO-self.rect.w:
            self.var_x=-20
        elif self.rect.x<=0:
            self.var_x=20

        #son todas las posibles direcciones de mis fantasmas.
        if self.pausa!=1:
            if self.var_x==20 and self.var_y==0: 
                self.dir=1
            if self.var_x==-20 and self.var_y==0:
                self.dir=2
            if self.var_x==0 and self.var_y==0:
                self.dir=3
            if self.var_x==0 and self.var_y==5:
                self.dir=4
            if self.var_x==40 and self.var_y==0:
                self.dir=5
            if self.var_x==-40 and self.var_y==0:
                self.dir=6
            if self.var_x==0 and self.var_y==-5:
                self.dir=7
            if self.var_x==0 and self.var_y==50:
                self.dir=8

def Recorte2(imagen,an_img_recorte,al_img_recorte): # funcion que me retorna una matriz con todos los recortes hechos a una imagen.
	matriz = []
	for i in range(2):
		matriz.append([])
		for j in range(3):
			cuadro=(j*an_img_recorte,i*al_img_recorte,an_img_recorte,al_img_recorte) #posicion del recorte de la imagen
			recorte=imagen.subsurface(cuadro) #me va a tener el recorte de cierta posicion de una imagen 
			matriz[i].append(recorte)
	return matriz

def main2(lista): #el primer elemento es jp, el segundo es el grupo general,tiene el grupo balas,luego la desicion, el sonido de disparo
                  #recorte que es la bala, b que es una bala, el tiempo que ha transcurrido del otro juego

    ex2=pygame.mixer.Sound('explosion.ogg')
    dragonball=pygame.mixer.Sound('dragonball.ogg')
    derrota=pygame.mixer.Sound('derrota.ogg')
    sirena=pygame.mixer.Sound('sirena.ogg')
    alarma=pygame.mixer.Sound('alarma.ogg')
    pygame.init()
    ventana=pygame.display.set_mode([ANCHO,ALTO])
    pacm=pygame.image.load('fondoPacman2.jpg')
    pacman=pygame.image.load('pacman.png').convert_alpha()
    ancho_img,alto_img=pacman.get_size()
    sp_fil=2    
    sp_col=3
    m=Recorte2(pacman,ancho_img/sp_col,alto_img/sp_fil)

    imag=pygame.image.load('explosion3.png').convert_alpha()
    ancho_img,alto_img=imag.get_size()
    sp_fil=4
    sp_col=4
    m2=Recorte(imag,sp_fil,sp_col,ancho_img,alto_img)

    fantasmas=pygame.image.load('fantasmas.png').convert_alpha()
    ancho_img,alto_img=fantasmas.get_size()
    sp_fil=4
    sp_col=14
    m3=Recorte(fantasmas,sp_fil,sp_col,ancho_img,alto_img)

    enter=pygame.image.load('enter.png')

    fantas=pygame.sprite.Group()
    perder=pygame.sprite.Group() #tiene los sprites que hace que mi jugador muera.
    constante=150 #me permite dar la separcion entre cada fantasma de la segunda fila, con respecto a x.
    constante2=80

    for i in range(5): #-------------Estos ciclos son para ubicar mis sprites fantasmas en pantalla.-------------
        if i<2:
            f=Fantasmas(m3,0,constante2*i+30,300)
            fantas.add(f)
            perder.add(f)
        elif i==4:
            f=Fantasmas(m3,0,constante2*i+30-276,200)
            fantas.add(f)
            perder.add(f)
        else:
            f=Fantasmas(m3,0,constante2*i-constante,250)
            fantas.add(f)
            perder.add(f)

    for i in range(5,10):
        if i<7:
            f=Fantasmas(m3,2,constante2*(i-3)+30,300)
            fantas.add(f)
            perder.add(f)
        elif i==9:
            f=Fantasmas(m3,2,constante2*(i-3)+30-276,200)
            fantas.add(f)
            perder.add(f)
        else:
            f=Fantasmas(m3,2,constante2*(i-3)-constante,250)
            fantas.add(f)
            perder.add(f)

    for i in range(10,15):
        if i<12:
            f=Fantasmas(m3,4,constante2*(i-6)+30,300)
            fantas.add(f)
            perder.add(f)
        elif i==14:
            f=Fantasmas(m3,4,constante2*(i-6)+30-276,200)
            fantas.add(f)
            perder.add(f)
        else:
            f=Fantasmas(m3,4,constante2*(i-6)-constante,250)
            fantas.add(f)
            perder.add(f)

    for i in range(15,20):
        if i<17:
            f=Fantasmas(m3,6,constante2*(i-9)+30,300)
            fantas.add(f)
            perder.add(f)
        elif i==19:
            f=Fantasmas(m3,6,constante2*(i-9)+30-276,200)
            fantas.add(f)
            perder.add(f)
        else:
            f=Fantasmas(m3,6,constante2*(i-9)-constante,250)
            fantas.add(f)
            perder.add(f)

    for i in range(20,25):
        if i<22:
            f=Fantasmas(m3,8,constante2*(i-12)+30,300)
            fantas.add(f)
            perder.add(f)
        elif i==24:
            f=Fantasmas(m3,8,constante2*(i-12)+30-276,200)
            fantas.add(f)
            perder.add(f)
        else:
            f=Fantasmas(m3,8,constante2*(i-12)-constante,250)
            fantas.add(f)
            perder.add(f)

    for f in fantas:  #Hago que los fantasmas de la primera fila se muevan.
        if f.rect.y==200:
            f.var_x=20



    bart=pygame.image.load('bart.jpg')

    pc=Pacman(m)

    pajaros=pygame.sprite.Group()
    pajaros.add(pc)
    perder.add(pc)
    

    fin = True
    reloj=pygame.time.Clock()
    jp=lista[0]
    general=lista[1]
    balas=lista[2]
    decision=0
    d=lista[4]
    recorte=lista[5]
    b=lista[6]
    vidas=lista[7]
    fuente1=pygame.font.Font(None,30)
    contador_balas=0 #es para saber cuantas balas le han dado a pacman
    fuente=pygame.font.Font(None,40)
    contador=0 #Es para que despues de matar a pacman, se pueda ver la explosion
    t_seg=0
    nivel=2
    puntos=0
    control_fantasmas=0 #Me a a permitir establecer un criterio en el cual se van a realizar los patrones.
    patron=1 #Me permite saber en que patorn estoy.
    num_aleatorio=0 #va a tener un numero aleatorio para elegir a cierto fantasma
    pos_inicialy=0 #me va a contener la pos en y inicial de cada fantasma.
    pos_inicialx=0 #tinie la pos inicial en x de cada fantas, es util, ya que me perite identificar a cada fantasma.
    aux_t=0 #me va a permitir reiniciar el tiempo para que se ejecuten los patrones.
    fan_eliminado=0 #me va contando los fantasmas eliminados, para poder dar rangos con respecto a esto.
    contnumAleatorio=0
    aux2_t=0 #es otro reloj y lo utilizo cada vez que pierda una vida para que pacman reinicie desde 0.
    contFanEliminados=0
    pausa=0
    aux3_t=0 #este reloj es para cuando pause el juego, me empiece a contar el tiempo que lleva pausado y luego se lo resto a los otros relojes.
    t_seg2=0

    while fin:
        for b in balas: #elimino las balas que colisionan con cada fantasma, y a los fantasmas que les disparan ciertas veces.
            ls_col1=pygame.sprite.spritecollide(b,fantas,False)
            for c in ls_col1:
                balas.remove(b)
                c.cont_balas+=1
                if c.cont_balas==10:               
                    fantas.remove(c)
                    perder.remove(c)
                    puntos+=1
                    contFanEliminados+=1
                    if fan_eliminado!=20: #porque son solo 20 fantasmas a los que les aplico rango, no hay rango negativo.
                        fan_eliminado+=1

        ls_col2=pygame.sprite.spritecollide(jp,perder,False) #---------------CUANDO PIERDO UNA VIDA-------------------  
        for p in ls_col2:
            vidas-=1
            fantas.empty()
            perder.empty()
            balas.empty()
            perder.add(pc)
            jp.rect.x=ANCHO-jp.rect.w
            jp.rect.y=ALTO-jp.rect.h
            aux2_t=0
            aux_t=0
            puntos=0
            fan_eliminado=0
            patron=1
            contnumAleatorio=0
            print control_fantasmas
            control_fantasmas=0
            print control_fantasmas
            for i in range(5): #-------------Estos ciclos me vuelven a ubicar desde cero mis sprites fantasmas en pantalla.-----------
                if i<2:
                    f=Fantasmas(m3,0,constante2*i+30,300)
                    fantas.add(f)
                    perder.add(f)
                elif i==4:
                    f=Fantasmas(m3,0,constante2*i+30-276,200)
                    fantas.add(f)
                    perder.add(f)
                else:
                    f=Fantasmas(m3,0,constante2*i-constante,250)
                    fantas.add(f)
                    perder.add(f)

            for i in range(5,10):
                if i<7:
                    f=Fantasmas(m3,2,constante2*(i-3)+30,300)
                    fantas.add(f)
                    perder.add(f)
                elif i==9:
                    f=Fantasmas(m3,2,constante2*(i-3)+30-276,200)
                    fantas.add(f)
                    perder.add(f)
                else:
                    f=Fantasmas(m3,2,constante2*(i-3)-constante,250)
                    fantas.add(f)
                    perder.add(f)

            for i in range(10,15):
                if i<12:
                    f=Fantasmas(m3,4,constante2*(i-6)+30,300)
                    fantas.add(f)
                    perder.add(f)
                elif i==14:
                    f=Fantasmas(m3,4,constante2*(i-6)+30-276,200)
                    fantas.add(f)
                    perder.add(f)
                else:
                    f=Fantasmas(m3,4,constante2*(i-6)-constante,250)
                    fantas.add(f)
                    perder.add(f)

            for i in range(15,20):
                if i<17:
                    f=Fantasmas(m3,6,constante2*(i-9)+30,300)
                    fantas.add(f)
                    perder.add(f)
                elif i==19:
                    f=Fantasmas(m3,6,constante2*(i-9)+30-276,200)
                    fantas.add(f)
                    perder.add(f)
                else:
                    f=Fantasmas(m3,6,constante2*(i-9)-constante,250)
                    fantas.add(f)
                    perder.add(f)

            for i in range(20,25):
                if i<22:
                    f=Fantasmas(m3,8,constante2*(i-12)+30,300)
                    fantas.add(f)
                    perder.add(f)
                elif i==24:
                    f=Fantasmas(m3,8,constante2*(i-12)+30-276,200)
                    fantas.add(f)
                    perder.add(f)
                else:
                    f=Fantasmas(m3,8,constante2*(i-12)-constante,250)
                    fantas.add(f)
                    perder.add(f)

            for f in fantas:  #Hago que los fantasmas de la primera fila se muevan.
                if f.rect.y==200:
                    f.var_x=20

        tiempo=pygame.time.get_ticks()/1000 #divido entre 1000 porque 1s son 1000ms y get_ticks me devuelve en ms.
        if tiempo-lista[7]-6==t_seg: #le resto el tiempo que lleva del anterior nivel y resto 6 porque empieza desde 6
           t_seg+=1
           t_seg2+=1
           aux_t+=1
           aux2_t+=1
           if pausa==1:
                aux3_t+=1

        if t_seg2==30:
            sirena.play()
        if t_seg2==75:
            sirena.stop()
            alarma.play()

        #print tiempo-lista[7]-6,t_seg

        #-------------------------------DEFINICION DE PATRONES---------------------------------------------

        if aux2_t==100:
            pc.controlTiempo=1
        elif aux2_t<100:
            pc.controlTiempo=0

        #----------------------------------------------PATRON 1--------------------------------------------
        if pausa!=1:
            if patron==1:
                if aux_t==5:  #ME va a definir la movencion de los primeros 4 fantasmas.
                    for f in fantas:
                        if (f.rect.x==10 and f.rect.y==250) or (f.rect.x==730 and f.rect.y==250) or (f.rect.x==30 and f.rect.y==300) or (f.rect.x==750 and f.rect.y==300):
                            f.var_y=5

                for f in fantas: #ciclo para la movencion horizontal de los primeros 4 fantasmas
                    if f.rect.y>=ALTO-f.rect.h:
                        if f.rect.x==30:
                            f.var_y=0
                            f.var_x=40
                        if f.rect.x==750:
                            f.var_y=0
                            f.var_x=-40

                    if f.rect.y>=ALTO-f.rect.h-50:
                        if f.rect.x==10:
                            f.var_y=0
                            f.var_x=40
                        if f.rect.x==730:
                            f.var_y=0
                            f.var_x=-40

                for f in fantas: #Esta parte es para fundamental ya que me permite aumentar control_fant.. al detectar que uno de los
                        if (f.rect.x==10 and f.rect.y>=ALTO-f.rect.h-50): #cuatro fantasmas "choca contra la pared", con solo uno que de
                            control_fantasmas+=1                          #tecte ya aumenta mi variable y me permite hacer mas estable el
                            print control_fantasmas                       #cambio de patron.
                            break
                        elif (f.rect.x==730 and f.rect.y>=ALTO-f.rect.h-50):
                            control_fantasmas+=1
                            print control_fantasmas
                            break
                        elif (f.rect.x==30 and f.rect.y>=ALTO-f.rect.h):
                            control_fantasmas+=1
                            print control_fantasmas
                            break
                        elif (f.rect.x==750 and f.rect.y>=ALTO-f.rect.h):
                            control_fantasmas+=1
                            print control_fantasmas
                            break

                if control_fantasmas==9:
                    for f in fantas:
                        if (f.rect.x==10 and f.rect.y>=ALTO-f.rect.h-50) or (f.rect.x==730 and f.rect.y>=ALTO-f.rect.h-50) or (f.rect.x==30 and f.rect.y>=ALTO-f.rect.h) or (f.rect.x==750 and f.rect.y>=ALTO-f.rect.h):
                            f.var_y=-5   
                            f.var_x=0  

                if control_fantasmas==9:
                    for f in fantas: 
                        if (f.rect.x==10 and f.rect.y==250) or (f.rect.x==730 and f.rect.y==250) or (f.rect.x==30 and f.rect.y==300) or (f.rect.x==750 and f.rect.y==300):
                            patron=2
                            f.var_y=0
                            control_fantasmas=0 
        #--------------------------------------PATRON 2----------------------------------------------------------------------------- 

        if patron==2:   #Voy a hacer que cada fantasma decienda en determinado momento.
            #print patron
            if aux_t==35 and contnumAleatorio==0:   #meto el contnumA porque el aux_t toma varias veces el mismo tiempo y necesito que solo lo reconozca 
                num_aleatorio=randrange(20)         #como una vez.
                for pos,f in enumerate(fantas):
                    if f.rect.y==300 or f.rect.y==250:
                        if pos==num_aleatorio: #elijo el fantasma que coincida con el numero aleatorio
                            f.var_y=50
                            pos_inicialx=f.rect.x
                            pos_inicialy=f.rect.y
                            contnumAleatorio+=1   
            else:
                for f in fantas: #fantas tiene mis fantasmas pero cada vez que hago el ciclo, este cambia de posicion a mis fantasmas
                    if pos_inicialy==f.rect.y and pos_inicialx==f.rect.x:  #dando indices diferentes, por eso esta condicion se puede
                        f.var_y=0                                          #ejecutar varias veces mientras hago un recorrido de 
                        num_aleatorio=randrange(20-fan_eliminado)          #todos mis fantasmas en fantas, por eso en el ultimo condi
                        contnumAleatorio+=1                                #cional establesco un rango. if contnumAle>=....
                        #print contnumAleatorio
                        if contnumAleatorio>=30 and contnumAleatorio<=35: #esta condicion es para que mis fantasmas siempre queden
                            pass                                          #bien posicionados en caso de que el patron 2 termine.
                        else:
                            for pos,f in enumerate(fantas):
                                if f.rect.y==300 or f.rect.y==250:
                                    if pos==num_aleatorio:
                                        f.var_y=50
                                        pos_inicialx=f.rect.x
                                        pos_inicialy=f.rect.y
                    else:
                        for f in fantas:
                            if f.rect.y>=ALTO:
                                f.rect.y=0

            if contnumAleatorio>=30 and contnumAleatorio<=35: #este rango es por la razon antes dada.
                contnumAleatorio=0
                aux_t=0
                patron=1

        #----------------------------------------------------------------------------------------------------------
        if contFanEliminados==12: #por cada 12 fantasmas que elimine doy una vida.
            contFanEliminados=0
            vidas+=1
            puntos=0

        if vidas==0: #-------------------------------------DERROTA--------------------------
            derrota.play()
            texto=fuente.render("FIN DEL JUEGO",True,BLANCO)
            texto4=fuente.render("TIEMPO TOTAL: "+str(t_seg2)+"s",True,BLANCO)
            texto6=fuente.render("MAXIMO NIVEL: "+str(nivel),True,BLANCO)
            ventana.fill(NEGRO)
            ventana.blit(texto,[300,200])
            ventana.blit(texto4,[300,250])
            ventana.blit(texto6,[300,300])
            pygame.display.flip()
            reloj.tick(0.3)
            fin=False

                

        ls_col1=pygame.sprite.spritecollide(pc,balas,True)#------------------DESTRUIR A PACMAN-------------------
        for e in ls_col1:
            contador_balas+=1
            if contador_balas==20:
                expl=Explosion(m2,220,80)
                ex2.play()
                pajaros.remove(pc)
                pajaros.add(expl)
                for i in range(40):
                    pajaros.update()
                    ventana.fill(NEGRO)
                    pajaros.draw(ventana)
                    reloj.tick(10)
                    pygame.display.flip()
                ex2.stop()
                dragonball.play()
                texto=fuente.render("FELICITACIONES!",True,BLANCO)
                texto4=fuente.render("HAS GANADO EL JUEGO: ",True,BLANCO)
                texto6=fuente.render("MATO A  P A C M A N --> MALO ",True,BLANCO)
                ventana.blit(bart,[0,0])
                ventana.blit(texto,[200,200])
                ventana.blit(texto4,[200,250])
                ventana.blit(texto6,[200,300])
                pygame.display.flip()
                reloj.tick(0.1)
                fin=False


    #Gestion de eventos
        for evento in pygame.event.get():
            if evento.type==pygame.KEYDOWN:
            	if evento.key==pygame.K_ESCAPE:
                    fin=False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and pausa==0:
                    jp.varx=-8
                    jp.col=4
                    jp.dir=1
                    jp.x=0
                    decision=2
                if evento.key == pygame.K_RIGHT and pausa==0:
                    jp.varx=8
                    jp.col=4
                    jp.dir=2
                    jp.x=0
                    decision=1
                if evento.key == pygame.K_UP and pausa==0:
                    jp.col=4
                    jp.dir=3
                    jp.x=0
                    decision=3

                if evento.key == pygame.K_SPACE and pausa==0:
                        jp.vary=-20

                if evento.key == pygame.K_d and pausa==0: #Para disparar
                    d.play()
                    posDisparox=0
                    if decision==1:
                        b=Proyectil(10,0,recorte,0)
                        posDisparox=jp.rect.w+1
                        b.decision=1
                    elif decision==2:
                        b=Proyectil(-10,0,recorte,0)
                        posDisparox=-36
                        b.decision=2
                    elif decision==3:
                        b=Proyectil(0,-10,recorte,0)
                        posDisparox=-36
                        b.decision=3
                    b.rect.x=jp.rect.x+posDisparox
                    b.rect.y=jp.rect.y+10 #para que el tiro sea mas acorde con la pos del jugador
                    balas.add(b)#a es para pausar el juego.
                if evento.key == pygame.K_a:
                    pausa=1
                    pygame.mixer.pause()
                    for f in fantas:
                        f.var_x=0
                        f.var_y=0
                        f.pausa=1
                    pc.var_y=0
                    pc.var_x=0
                    ventana.blit(enter,[300,200])
                    pygame.display.flip()
                    for b in balas:
                        b.var_y=0
                        b.var_x=0

                if evento.key == pygame.K_RETURN and pausa==1: #despausa el juego.
                    aux_t=aux_t-aux3_t
                    aux2_t=aux2_t-aux3_t
                    t_seg2=t_seg2-aux3_t
                    pygame.mixer.unpause()
                    aux3_t=0
                    pausa=0
                    for f in fantas:
                        if f.dir==1:
                            f.var_x=20
                            f.var_y=0
                            f.pausa=0
                        elif f.dir==2:
                            f.var_x=-20
                            f.var_y=0
                            f.pausa=0
                        elif f.dir==3:
                            f.var_x=0
                            f.var_y=0
                            f.pausa=0
                        elif f.dir==4:
                            f.var_x=0
                            f.var_y=5
                            f.pausa=0
                        elif f.dir==5:
                            f.var_x=40
                            f.var_y=0
                            f.pausa=0
                        elif f.dir==6:
                            f.var_x=-40
                            f.var_y=0
                            f.pausa=0
                        elif f.dir==7:
                            f.var_x=0
                            f.var_y=-5
                            f.pausa=0
                        elif f.dir==8:
                            f.var_x=0
                            f.var_y=50
                            f.pausa=0
                    for b in balas:
                        if b.decision==1:  #------------------------prestar atencion a decision, puede que este disparando a todas
                            b.var_x=10      #partes, y decision me devia todas las balas a la misma direccion.
                        elif b.decision==2:
                            b.var_x=-10
                        elif b.decision==3:
                            b.var_y=-10
                if evento.key == pygame.K_ESCAPE:
                    fin=False

        if pc.controlTiempo==1: #si esta en 1, pacman persigue al jugador
            pc.p1=jp.rect.x
            pc.p2=jp.rect.y
            if pc.rect.x<pc.p1:  #dependiendo si la pos del mouse esta a la izq o der del sprite, voy a sumar o a restar la pos x.
                pc.var_x=5
                pc.dir=0
            elif pc.rect.x>pc.p1:
                pc.var_x=-5
                pc.dir=1
            pc.Pendiente()
        if pausa==0:
            fantas.update()
            pajaros.update()
            general.update()
            balas.update()
            ventana.blit(pacm,[0,0])
            pajaros.draw(ventana)
            general.draw(ventana)
            fantas.draw(ventana)
            texto2=fuente1.render("Nivel: "+str(nivel)+"   Vidas: "+str(vidas)+"  Tiempo: "+str(t_seg2)+"   Puntos: "+str(puntos),True,BLANCO)
            ventana.blit(texto2,[400,5])
            balas.draw(ventana)
            reloj.tick(10)
            pygame.display.flip()