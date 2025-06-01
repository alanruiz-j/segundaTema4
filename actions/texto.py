import pygame
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import *

def draw_text(text, posx, posy, posz, sizeFont, r, g, b, rb, gb, bb):
    font = pygame.font.Font(None, sizeFont)
    text_surface = font.render(text, True, (r,g,b), (rb,gb,bb))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos3d(posx, posy, posz)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)