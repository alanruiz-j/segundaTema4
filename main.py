from tkinter import messagebox
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from pygame.locals import *
import sys
from OpenGL.GLUT import glutInit
from actions.objects import resetear_opengl

from src import menu 
import src
import src.lvl1
import src.lvl2
import src.lvl3

def main():

    while True:
        pygame.display.init()
        pygame.init()
        pygame.mixer.init()
        SCREEN_WIDTH = 1500
        SCREEN_HEIGHT = 800

        display = (SCREEN_WIDTH, SCREEN_HEIGHT)
        screen = pygame.display.set_mode(display)
        clock = pygame.time.Clock()    
        pygame.display.set_caption("Menu")    
        icon = pygame.image.load("images/tfdBunny.png")  # 32x32 recommended
        pygame.display.set_icon(icon)

        if not menu.start_menu(screen, clock, display):
            pygame.quit()
            sys.exit()
        screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
        glutInit()  # Required for GLUT shapes
        menu.character_select(screen, clock, display)
        pygame.display.quit()
        #Niveles
        if menu.selected_index==0:
            pygame.display.init()
            print("lvl 1")
            result = src.lvl1.run()
        elif menu.selected_index==1:
            pygame.display.init()
            print("lvl 2")
            result = src.lvl2.run()
        elif menu.selected_index==2:    
            pygame.display.init()
            print("lvl 3")
            result = src.lvl3.run()
        
        if result == "quit":
            break
        elif result == "next":
            print("Load next level...")

    resetear_opengl()

if __name__ == "__main__":
    main()