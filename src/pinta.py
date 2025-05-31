from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from personajes import toonix

#cubo

def pintar_pared(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],1)
    toonix.draw_cube(0,1,0,1,0,3)
    glPopMatrix()

#personaje

def pintar_cabeza(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],1)
    toonix.draw_cube(2,-2,-1.5,1.5,3.5,7.5)
    glPopMatrix()

def pintar_frente(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],10)
    toonix.draw_cube(2,-2,-1.5,1.5,7.5,10.5)
    glPopMatrix()

def marca_frente(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0,0.5,0,1,7)
    toonix.draw_line(0.25,0.25,0.25,-0.25,1,4)
    glPopMatrix()

def pintar_torso(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_cube(-1.5,1.5,-0.5,0.5,1,3.5)
    glPopMatrix()

def marca_torso(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0,-0.2,-0.4,1,7)
    toonix.draw_line(-0.2,-0.4,0.1,-0.4,1,4)
    toonix.draw_line(0.1,-0.4,-0.3,-0.8,1,7)
    glPopMatrix()

def pintar_extremidad(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_cylinder(0.5,1.5,50)
    glPopMatrix()

def pintar_esfera(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_sphere(0.5,50,50)
    glPopMatrix()

#expresiones

#normal
def pintar_ojo_normal(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0,0.5,0,1,7)
    toonix.draw_line(0.25,0.25,0.25,-0.25,1,7)
    glPopMatrix()

def pintar_boca_normal(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0,0.5,0,1,7)
    glPopMatrix()

#feliz
def pintar_ojo_feliz(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0,0.25,0.25,1,7)
    toonix.draw_line(0.25,0.25,0.5,0,1,7)
    glPopMatrix()

def pintar_boca_feliz(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0,0.5,0,1,7)
    toonix.draw_line(0.5,0,0.6,0.2,1,7)
    glPopMatrix()


#triste
def pintar_ojo_triste(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0,0.25,-0.25,1,7)
    toonix.draw_line(0.25,-0.25,0.5,0,1,7)
    glPopMatrix()

def pintar_boca_triste(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0,0.5,0,1,7)
    toonix.draw_line(0.5,0,0.6,-0.2,1,7)
    toonix.draw_line(0,0,-0.1,-0.2,1,7)
    glPopMatrix()

#enojado
def pintar_ojo_enojado1(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0.7,0.6,0.5,1,7)
    toonix.draw_line(0,0,0.5,0,1,7)
    toonix.draw_line(0.25,0.25,0.25,-0.25,1,7)
    glPopMatrix()

def pintar_ojo_enojado2(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(-0.1,0.5,0.5,0.7,1,7)
    toonix.draw_line(0,0,0.5,0,1,7)
    toonix.draw_line(0.25,0.25,0.25,-0.25,1,7)
    glPopMatrix()

def pintar_boca_enojado(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0,0.5,0,1,7)
    toonix.draw_line(0.5,0,0.6,-0.2,1,7)
    toonix.draw_line(0,0,-0.1,-0.2,1,7)
    glPopMatrix()

#sorprendido
def pintar_boca_sorprendido(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0,0.5,0,1,7)
    toonix.draw_line(0,0,0,0.5,1,7)
    toonix.draw_line(0,0.5,0.5,0.5,1,7)
    toonix.draw_line(0.5,0.5,0.5,0,1,7)
    glPopMatrix()

#muerto

def pintar_ojo_muerto(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_line(0,0,0.5,0.5,1,7)
    toonix.draw_line(0,0.5,0.5,0,1,7)
    glPopMatrix()

#poses

#extremidad a 45 grados
def pintar_extremidad_der_arriba(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_cylinder2(0.5,1.5,50,(posx,posy,posz), (1,-0.5,0))
    glPopMatrix()

#exremidad a 135 grados
def pintar_extremidad_izq_arriba(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    iluminacion(0,0,0)
    setColor([r,g,b,1],[r,g,b,1],[0.0,0.0,0.0,1],30)
    toonix.draw_cylinder2(0.5,1.5,50,(posx,posy,posz), (1,0.5,0))
    glPopMatrix()


def setColor(ambiente, difusor, especular, shine):
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambiente)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, difusor)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, especular)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, shine)
    
def iluminacion(r,g,b):
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    pos_luz = (5.0,5.0,5.0,1.0)
    luz_ambiental = (1.0,0.7,0.2,1.0)
    difusion = (r,g,b,1.0)
    glLightfv(GL_LIGHT0, GL_POSITION, pos_luz)
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiental)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, difusion)