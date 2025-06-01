from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from actions import objeto as obj

angulo_brazo = 0
esfera_x, esfera_y, esfera_z = 8, 6.5, 4
bI_x, bI_y, bI_z = 4.9, 5.5, 4 
bD_x, bD_y, bD_z = 11.5, 5.5, 4
pD_x, pD_y, pD_z = 6, 2.5, 4
iD_x, iD_y, iD_z = 10.6, 2.5, 4
ojoI_x, ojoI_y, ojoI_z = 7, 7, 1.7
ojoI1_x, ojoI1_y, ojoI1_z = 6.9, 7, 1.2555
ojoI2_x, ojoI2_y, ojoI2_z = 6.9, 7, 1
ojoDx, ojoDy, ojoDz = 8.5, 7, 1.6
ojoD_1x, ojoD_1y, ojoD_1z = 8.5, 7.01, 1.25555
ojoD_2x, ojoD_2y, ojoD_2z = 8.49, 7, 1




def set_posicion_esfera(x, y, z):
    global esfera_x, esfera_y, esfera_z
    esfera_x, esfera_y, esfera_z = x, y, z
def pinEsferaCuer():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(esfera_x, esfera_y, esfera_z)  
    glColor3f(0.1529, 0.8353, 0.0)
    obj.draw_sphere(3, 40, 40)
    glPopMatrix()

def set_posicion_BrazoI(x, y, z):
    global bI_x, bI_y, bI_z
    bI_x, bI_y, bI_z = x, y, z
def set_angulo_brazo(angulo):
    global angulo_brazo
    angulo_brazo = angulo
def pinBrazoI():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(bI_x, bI_y, bI_z)  
    glRotatef(angulo_brazo, 0, 0, 1)  
    glTranslate(0, -1, 0)  
    glColor3f(0.1529, 0.8353, 0.0)
    obj.draw_cylinderM(0.4, 1.5, 40)  
    glPopMatrix()


def set_posicion_BrazoD(x, y, z):
    global bD_x, bD_y, bD_z
    bD_x, bD_y, bD_z = x, y, z
def set_angulo_brazo2(angulo2):
    global angulo_brazo2
    angulo_brazo2 = angulo2
def pinBrazoD():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(bD_x, bD_y, bD_z)  
    glRotatef(-angulo_brazo2, 0, 0, 1)  
    glTranslate(0, -1, 0)  
    glColor3f(0.1529, 0.8353, 0.0)
    obj.draw_cylinderM(0.4, 1.5, 40)  
    glPopMatrix()

def set_posicion_PieD(x, y, z):
    global pD_x, pD_y, pD_z
    pD_x, pD_y, pD_z = x, y, z
def pinPieD():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(pD_x, pD_y, pD_z)
    glColor3f(0.1529, 0.8353, 0.0)
    obj.draw_cylinder(0.4,1,40)
    glPopMatrix()

def set_posicion_PieI(x, y, z):
    global iD_x, iD_y, iD_z
    iD_x, iD_y, iD_z = x, y, z
def pinPieI():
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(iD_x, iD_y, iD_z)
    glColor3f(0.1529, 0.8353, 0.0)
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
    glColor3f(0.1529, 0.8353, 0.0)
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
    glColor3f(0.1529, 0.8353, 0.0)
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

def mostrar_emocion_relativa(nombre_emocion):
    glPushMatrix()
    if nombre_emocion == 'feliz':
        glTranslate(esfera_x + -0.25, esfera_y + -1, esfera_z + -3) 
        obj.emocionFeliz()
    elif nombre_emocion == 'feliz1':
        glTranslate(esfera_x + -0.25, esfera_y + -1, esfera_z + -3) 
        obj.emocionFeliz1()
    elif nombre_emocion == 'triste':
        glTranslate(esfera_x + -0.25, esfera_y, esfera_z + -3) 
        obj.emocionTriste()
    elif nombre_emocion == 'enojo':
        glTranslate(esfera_x + -0.25, esfera_y + 0.5, esfera_z + -3) 
        obj.emocionEnojo()
    elif nombre_emocion == 'sorpresa':
        glTranslate(esfera_x + -0.25, esfera_y + 0.3, esfera_z + -3) 
        obj.emocionSorpresa()
    elif nombre_emocion == 'disgusto':
        glTranslate(esfera_x + -0.25, esfera_y + -1, esfera_z + -3)
        obj.emocionDisgusto()
    elif nombre_emocion == 'sonrojado':
        glTranslate(esfera_x + -0.25, esfera_y + -1, esfera_z + -3)
        obj.emocionSonrojado()
    elif nombre_emocion == 'normal':
        glTranslate(esfera_x + -0.25, esfera_y, esfera_z + -3)
        obj.emocionNormal()
    glPopMatrix()
