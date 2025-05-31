import pygame
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import *

def iluminacion (R,G,B):
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0) #Te dice que hay una fuente de luz
    glEnable(GL_DEPTH_TEST) #Habilita la primer fuente de luz
    posicion_luz=(9.0,10.0,4.0,1.0)
    luz_ambiental=(1.0, 1.0, 1.0, 1.0)
    difusion=(R,G,B,1.0)
    luz_especular = (1.0, 1.0, 1.0, 1.0)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
    glLightfv(GL_LIGHT0,GL_POSITION,posicion_luz)
    glLightfv(GL_LIGHT0,GL_AMBIENT,luz_ambiental)
    glLightfv(GL_LIGHT0,GL_DIFFUSE,difusion)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)