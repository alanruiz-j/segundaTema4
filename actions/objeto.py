from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from pygame.locals import *

def draw_sphere(radius, slices, segments):
    for i in range(slices+1):
        lat0 = math.pi*(-0.5*(i-1)/slices)
        lat1 = math.pi*(-0.5*i/slices)
        z0 = radius*math.sin(lat0)
        zr0 = radius*math.cos(lat0)
        z1 = radius*math.sin(lat1)
        zr1 = radius*math.cos(lat1)
        glBegin(GL_QUAD_STRIP)
        for j in range(segments+1):
            lng = 2*math.pi*j/segments
            x = zr0*math.cos(lng)
            y = zr0*math.sin(lng)
            glNormal3f(x,y,z0)
            glVertex3f(x,y,z0)
            x = zr1*math.cos(lng)
            y = zr1*math.sin(lng)
            glNormal3f(x,y,z1)
            glVertex3f(x,y,z1)
        glEnd()

def draw_cylinder(radius, height, segments):
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        theta = i * (2 * math.pi / segments)
        x = height / 2  
        y = radius * math.cos(theta)  
        z = radius * math.sin(theta)  
        glVertex3f(x, y, z)  
        glVertex3f(-x, y, z)  
    glEnd()


def draw_cylinderM(radius, height, segments):
    glBegin(GL_QUAD_STRIP)
    for i in range(segments+1):
        theta = i*(2*math.pi/segments)
        x = radius*math.cos(theta)
        y = radius*math.sin(theta)
        glVertex3f(x, height/2, y)
        glVertex3f(x, -height/2, y)
    glEnd()
def emocionFeliz():
    glColor3f(0.0, 0.0, 0.0)  
    glLineWidth(3.0)
    glBegin(GL_LINES)
    a = 0.5  
    b = 0    
    for i in range(-10, 11): 
        x1 = i / 10.0  
        y1 = a * (x1 ** 2) + b     
        x2 = (i + 1) / 10.0  
        y2 = a * (x2 ** 2) + b 
        glVertex3f(x1, y1, 0)  
        glVertex3f(x2, y2, 0)  
    glEnd()

# def emocionFeliz1():
#     glColor3f(0.0, 0.0, 0.0)  
#     glLineWidth(3.0)
#     glBegin(GL_LINES)
#     a = 0.8
#     b = 0    
#     for i in range(-5, 6): 
#         x1 = i / 10.0  
#         y1 = a * (x1 ** 2) + b     
#         x2 = (i + 1) / 10.0  
#         y2 = a * (x2 ** 2) + b 
#         glVertex3f(x1, y1, 0)  
#         glVertex3f(x2, y2, 0)  

#     glEnd()

def emocionTriste():
    glColor3f(0.0, 0.0, 0.0)  
    glLineWidth(3.0)
    glBegin(GL_LINES)

    a = -0.5
    b = 0   
    
    for i in range(-10, 11):
        x1 = i / 10.0   
        y1 = a * (x1 ** 2) + b 
        glVertex3f(x1, y1, 0) 
        x2 = (i + 1) / 10.0  
        y2 = a * (x2 ** 2) + b 
        glVertex3f(x2, y2, 0) 
    
    glEnd()

def emocionEnojo():
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(6.0)

    # Línea de la boca enojada
    glBegin(GL_LINES)
    glVertex3f(-0.5, -0.5, 0)
    glVertex3f(0.5, -0.5, 0)
    glEnd()

    # Cejas fruncidas
    glBegin(GL_LINES)
    glVertex3f(-0.5, 0.6, 0)
    glVertex3f(-0.2, 0.4, 0)

    glVertex3f(0.5, 0.6, 0)
    glVertex3f(0.2, 0.4, 0)
    glEnd()

def emocionSorpresa():
    glColor3f(0.0, 0.0, 0.0)  
    glLineWidth(6.0)
    radio = 0.5
    centro_x = 0  
    centro_y = -0.5 
    angulo_inicio = math.radians(0)  
    angulo_fin = math.radians(360)  
    glBegin(GL_LINE_STRIP) 
    for i in range(101):  
        t = i / 100.0  
        angulo = angulo_inicio + t * (angulo_fin - angulo_inicio)
        x = centro_x + radio * math.cos(angulo)
        y = centro_y + radio * math.sin(angulo)
        glVertex3f(x, y, 0)  
    glEnd()

def emocionSonrojado():
    # Dibuja la sonrisa (negro)
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    a = 0.8
    b = 0
    for i in range(-5, 6):
        x1 = i / 10.0
        y1 = a * (x1 ** 2) + b
        x2 = (i + 1) / 10.0
        y2 = a * (x2 ** 2) + b
        glVertex3f(x1, y1, 0)
        glVertex3f(x2, y2, 0)
    glEnd()

    # Dibuja el sonrojo (rosado)
   # glTranslate(6.6, 6.5, 1)
    glColor3f(0.964, 0.419, 0.5254)
    glLineWidth(4.0)
    radio = 0.3
    centro_x = 0
    centro_y = -0.5
    angulo_inicio = math.radians(0)
    angulo_fin = math.radians(360)

    glBegin(GL_POLYGON)
    for i in range(101):
        t = i / 100.0
        angulo = angulo_inicio + t * (angulo_fin - angulo_inicio)
        x = centro_x + radio * math.cos(angulo)
        y = centro_y + radio * math.sin(angulo)
        glVertex3f(x, y, 0)
    glEnd()

    ###glTranslate(8.92, 6.5, 1)
    glColor3f(0.964, 0.419, 0.5254)
    glLineWidth(4.0)
    radio = 0.3
    centro_x = 0
    centro_y = -0.5
    angulo_inicio = math.radians(0)
    angulo_fin = math.radians(360)

    glBegin(GL_POLYGON)
    for i in range(101):
        t = i / 100.0
        angulo = angulo_inicio + t * (angulo_fin - angulo_inicio)
        x = centro_x + radio * math.cos(angulo)
        y = centro_y + radio * math.sin(angulo)
        glVertex3f(x, y, 0)
    glEnd()


def emocionDisgusto():
    glColor3f(0.0, 0.0, 0.0)  
    glLineWidth(3.0)  
    glBegin(GL_LINES)    
    a = 0.3 
    b = 0.0  
    frequency = 2.0     
    for i in range(-10, 11): 
        x1 = i / 10.0  
        y1 = a * math.sin(frequency * math.pi * x1) + b          
        x2 = (i + 1) / 10.0  
        y2 = a * math.sin(frequency * math.pi * x2) + b          
        glVertex3f(x1, y1, 0)  
        glVertex3f(x2, y2, 0) 
    glEnd()
   

def emocionNormal():
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(6.0)
    glBegin(GL_LINES)
    glVertex3f(-0.5, -0.5, 0)
    glVertex3f(0.5, -0.5, 0)
    glEnd()

def draw_cube():
    glBegin(GL_QUADS)
    
    # Cara frontal (Z = 5.0)
    glVertex3f(-2.0, -2.0, 2.0)
    glVertex3f(2.0, -2.0, 2.0)
    glVertex3f(2.0, 2.0, 2.0)
    glVertex3f(-2.0, 2.0, 2.0)
    
    # Cara trasera (Z = -2.0)
    glVertex3f(-2.0, -2.0, -2.0)
    glVertex3f(2.0, -2.0, -2.0)
    glVertex3f(2.0, 2.0, -2.0)
    glVertex3f(-2.0, 2.0, -2.0)
    
    # Cara inferior (Y = -2.0)
    glVertex3f(-2.0, -2.0, 2.0)
    glVertex3f(2.0, -2.0, 2.0)
    glVertex3f(2.0, -2.0, -2.0)
    glVertex3f(-2.0, -2.0, -2.0)
    
    # Cara superior (Y = 2.0)
    glVertex3f(-2.0, 2.0, 2.0)
    glVertex3f(2.0, 2.0, 2.0)
    glVertex3f(2.0, 2.0, -2.0)
    glVertex3f(-2.0, 2.0, -2.0)
    
    # Cara izquierda (X = -2.0)
    glVertex3f(-2.0, -2.0, 2.0)
    glVertex3f(-2.0, 2.0, 2.0)
    glVertex3f(-2.0, 2.0, -2.0)
    glVertex3f(-2.0, -2.0, -2.0)
    
    # Cara derecha (X = 2.0)
    glVertex3f(2.0, -2.0, 2.0)
    glVertex3f(2.0, 2.0, 2.0)
    glVertex3f(2.0, 2.0, -2.0)
    glVertex3f(2.0, -2.0, -2.0)
    
    glEnd()

def draw_rectanguloColi():
    glBegin(GL_QUADS)
    # Cara inferior (Y = -0.5 para centrar el cubo en Y)
    glVertex3f(-3.0, -0.5, -3.0)  # Vértice inferior izquierdo
    glVertex3f(3.0, -0.5, -3.0)   # Vértice inferior derecho
    glVertex3f(3.0, -0.5, 3.0)    # Vértice superior derecho
    glVertex3f(-3.0, -0.5, 3.0)   # Vértice superior izquierdo
    glEnd()
   
