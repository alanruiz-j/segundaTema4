import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *
from actions import objects
from personajes import chucho
import math
from src import lvl3

health = 0
posx = 0.0
posy = 0.0
posz = 0.0
enemy = False

def persona(ene,vida, x, y, z, red, green, blue):
    global health, posx, posy, posz, enemy
    health = vida
    enemy = ene
    posx = x
    posy = y
    posz = z
    center = [posx,posy,posz]
    translation_vector=[posx,posy,posz]
    objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.vestido1,translation_vector),'y',180,center),chucho.carasVestido1,0,0,0,0,0,red,green,blue)
    objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesLArm,translation_vector),'y',180,center),chucho.carasLArm,0,0,0,0,1,red,green,blue)
    objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesRArm,translation_vector),'y',180,center),chucho.carasRArm,0,1,0,0,1,red,green,blue)
    objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesRLeg,translation_vector),'y',180,center),chucho.carasRLeg,0,1,1,0,0,red,green,blue)
    objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesLLeg,translation_vector),'y',180,center),chucho.carasLLeg,0,0,1,0,0,red,green,blue)
    objects.draw_line(chucho.rotate_matrix(chucho.translate_matrix(chucho.sonrisa,translation_vector),'y',180,center),x,y)
    objects.draw_line(chucho.rotate_matrix(chucho.translate_matrix(chucho.ojo1a,translation_vector),'y',180,center),x,y)
    objects.draw_line(chucho.rotate_matrix(chucho.translate_matrix(chucho.ojo2a,translation_vector),'y',180,center),x,y)
    objects.pintar_esfera(posx, posy+14.5,posz,1.5,0,0,0,0)

def personaRot(ene,vida, x, y, z, yaw, angle, red, green, blue):
    global health, posx, posy, posz, enemy
    health = vida
    enemy = ene
    posx = x
    posy = y
    posz = z
    center = [posx,posy,posz]
    translation_vector=[posx,posy,posz]
    centerLeg = [1.5+posx, 7+posy, -0.75+posz]
    objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.vestido1,translation_vector),'y',180+yaw*-1,center),chucho.carasVestido1,0,0,0,0,0,red,green,blue)
    objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesLArm,translation_vector),'y',180+yaw*-1,center),chucho.carasLArm,0,0,0,0,1,red,green,blue)
    objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesRArm,translation_vector),'y',180+yaw*-1,center),chucho.carasRArm,0,1,0,0,1,red,green,blue)
    objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesRLeg,translation_vector),'x',angle,centerLeg),'y',180+yaw*-1,center),chucho.carasRLeg,0,1,1,0,0,red,green,blue)
    objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesLLeg,translation_vector),'x',angle*-1,centerLeg),'y',180+yaw*-1,center),chucho.carasLLeg,0,0,1,0,0,red,green,blue)
    objects.draw_line(chucho.rotate_matrix(chucho.translate_matrix(chucho.triste,translation_vector),'y',180+yaw*-1,center),x,y)
    objects.draw_line(chucho.rotate_matrix(chucho.translate_matrix(chucho.ojo1b,translation_vector),'y',180+yaw*-1,center),x,y)
    objects.draw_line(chucho.rotate_matrix(chucho.translate_matrix(chucho.ojo2b,translation_vector),'y',180+yaw*-1,center),x,y)
    objects.draw_line(chucho.rotate_matrix(chucho.translate_matrix(chucho.ceja1,translation_vector),'y',180+yaw*-1,center),x,y)
    objects.draw_line(chucho.rotate_matrix(chucho.translate_matrix(chucho.ceja2,translation_vector),'y',180+yaw*-1,center),x,y)
    objects.pintar_esfera(posx, posy+14.5,posz,1.5,0,0,0,0)
