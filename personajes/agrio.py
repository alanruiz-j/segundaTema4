from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from actions import objects as obj

angulo_brazo = 0
angulo_brazo2 = 0

def agrio(ilu=True):
    ojoD_1()
    ojoD_2()
    pinEsferaCuer(ilu)
    pinBrazoD(ilu)
    pinBrazoI(ilu)
    pinPieD(ilu)
    pinPieI(ilu)
    ojoI()
    ojoI_1()
    ojoI_2()
    ojoD()


def set_posicion_esfera(x, y, z):
    global esfera_x, esfera_y, esfera_z
    esfera_x, esfera_y, esfera_z = x, y, z
def pinEsferaCuer(ilu=True):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(esfera_x, esfera_y, esfera_z)  
    if ilu:glColor3f(0.0, 1.0, 0.0)
    else:glColor3f(0.0/5, 1.0/5, 0.0/5)
    obj.draw_sphere(4.2, 40, 40)
    glPopMatrix()

def set_posicion_BrazoI(x, y, z):
    global bI_x, bI_y, bI_z
    bI_x, bI_y, bI_z = x, y, z
def set_angulo_brazo(angulo):
    global angulo_brazo
    angulo_brazo = angulo
def pinBrazoI(ilu=True):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(bI_x, bI_y, bI_z)  
    glRotatef(angulo_brazo, 0, 0, 1)  
    glTranslate(0, -1, 0)  
    if ilu:glColor3f(0.0, 1.0, 0.0)
    else:glColor3f(0.0/5, 1.0/5, 0.0/5)
    obj.draw_cylinderM(0.4, 1.5, 40)  
    glPopMatrix()


def set_posicion_BrazoD(x, y, z):
    global bD_x, bD_y, bD_z
    bD_x, bD_y, bD_z = x, y, z
def set_angulo_brazo2(angulo2):
    global angulo_brazo2
    angulo_brazo2 = angulo2
def pinBrazoD(ilu=True):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(bD_x, bD_y, bD_z)  
    glRotatef(-angulo_brazo2, 0, 0, 1)  
    glTranslate(0, -1, 0)  
    if ilu:glColor3f(0.0, 1.0, 0.0)
    else:glColor3f(0.0/5, 1.0/5, 0.0/5)
    obj.draw_cylinderM(0.4, 1.5, 40)  
    glPopMatrix()

def set_posicion_PieD(x, y, z):
    global pD_x, pD_y, pD_z
    pD_x, pD_y, pD_z = x, y, z
def pinPieD(ilu=True):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(pD_x, pD_y, pD_z)
    if ilu:glColor3f(0.0, 1.0, 0.0)
    else:glColor3f(0.0/5, 1.0/5, 0.0/5)
    obj.draw_cylinder(0.4,1,40)
    glPopMatrix()

def set_posicion_PieI(x, y, z):
    global iD_x, iD_y, iD_z
    iD_x, iD_y, iD_z = x, y, z
def pinPieI(ilu=True):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(iD_x, iD_y, iD_z)
    if ilu:glColor3f(0.0, 1.0, 0.0)
    else:glColor3f(0.0/5, 1.0/5, 0.0/5)
    obj.draw_cylinder(0.4,1,40)
    glPopMatrix()

def set_posicion_OjoI(x, y, z):
    global ojoI_x, ojoI_y, ojoI_z
    ojoI_x, ojoI_y, ojoI_z = x, y, z
def ojoI():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(ojoI_x, ojoI_y, ojoI_z)
    glColor3f(1.0, 1.0, 1.0)
    obj.draw_sphere(0.7, 40, 40)
    glPopMatrix()

def set_posicion_OjoI_1(x, y, z):
    global ojoI1_x, ojoI1_y, ojoI1_z
    ojoI1_x, ojoI1_y, ojoI1_z = x, y, z
def ojoI_1():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(ojoI1_x, ojoI1_y, ojoI1_z)
    glColor3f(0.0, 1.0, 0.0)
    obj.draw_sphere(0.4, 40, 40)
    glPopMatrix()

def set_posicion_OjoI_2(x, y, z):
    global ojoI2_x, ojoI2_y, ojoI2_z
    ojoI2_x, ojoI2_y, ojoI2_z = x, y, z
def ojoI_2():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(ojoI2_x, ojoI2_y, ojoI2_z)
    glColor3f(0.0, 0.0, 0.0)
    obj.draw_sphere(0.2, 40, 40)
    glPopMatrix()

def set_posicion_OjoD(x, y, z):
    global ojoDx, ojoDy, ojoDz
    ojoDx, ojoDy, ojoDz = x, y, z
def ojoD():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(ojoDx, ojoDy, ojoDz)
    glColor3f(1.0, 1.0, 1.0)
    obj.draw_sphere(0.7, 40, 40)
    glPopMatrix()

def set_posicion_OjoD_1(x, y, z):
    global ojoD_1x, ojoD_1y, ojoD_1z
    ojoD_1x, ojoD_1y, ojoD_1z = x, y, z
def ojoD_1():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(ojoD_1x, ojoD_1y, ojoD_1z)
    glColor3f(0.0, 1.0, 0.0)
    obj.draw_sphere(0.44, 40, 40)
    glPopMatrix()

def set_posicion_OjoD_2(x, y, z):
    global ojoD_2x, ojoD_2y, ojoD_2z
    ojoD_2x, ojoD_2y, ojoD_2z = x, y, z
def ojoD_2():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(ojoD_2x, ojoD_2y, ojoD_2z)
    glColor3f(0.0, 0.0, 0.0)
    obj.draw_sphere(0.233, 40, 40)
    glPopMatrix()


def set_posicioin_emNomral(x, y, z):
    global emNormalx, emNormaly, emNormalz
    emNormalx, emNormaly, emNormalz = x, y, z
def emNormal():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(emNormalx, emNormaly, emNormalz) 
    obj.emocionEnojo()  
    glPopMatrix()

def emFeliz():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(7.8, 5.8, 1)  
    obj.emocionFeliz()  
    glPopMatrix()

def emFeliz1():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(7.8, 5.5, 1)  
    obj.emocionFeliz1()  
    glPopMatrix()
   
def emTriste():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(7.8, 5.8, 1) 
    obj.emocionTriste() 
    glPopMatrix()

def emSorpresa():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(7.8, 6.5, 1) 
    obj.emocionSorpresa()  
    glPopMatrix()

def emEnojo():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(7.8, 6.5, 1) 
    obj.emocionEnojo()  
    glPopMatrix()

def emEnojo_Cejas():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(7.7, 7.2, 1) 
    obj.cejas()  
    glPopMatrix()

def emSonrojado(): 
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(6.6, 6.5, 1)  
    obj.emocionSonrojado()  
    glPopMatrix()

def emSonrojado1():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(8.92, 6.5, 1)  
    obj.emocionSonrojado()  
    glPopMatrix()

def emDisgusto():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(7.8, 5.8, 1) 
    obj.emocionDisgusto() 
    glPopMatrix()

