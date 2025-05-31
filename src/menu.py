import pygame
from tkinter import messagebox
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from actions import objects
from personajes import chucho, toonix, agrio

def start_menu(screen, clock, display_size):
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)
    options = ['Start', 'Quit']
    selected = 0
    try:
        bg = pygame.image.load("images/imgMenu.png").convert()
    except pygame.error:
        bg = None
    else:
        bg = pygame.transform.scale(bg, display_size)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return (options[selected] == 'Start')
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((0, 0, 0))
        for i, text in enumerate(options):
            color = (0, 200, 0) if i == selected else (200, 200, 200)
            surf = font.render(text, True, color)
            rect = surf.get_rect(center=(display_size[0] // 2,
                                         display_size[1] // 2 + i * 60))
            screen.blit(surf, rect)

        pygame.display.flip()
        clock.tick(30)

pygame.font.init()
font = pygame.font.SysFont("Arial", 90)
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
selected_index = 1
def load_background(): #465464654654weruiytre4w
        bg_surface = pygame.image.load("images/menu_background.png").convert()
        bg_surface = pygame.transform.scale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_surface = pygame.transform.flip(bg_surface, False, True)
        bg_data = pygame.image.tostring(bg_surface, "RGB", True)

        bg_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, bg_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, SCREEN_WIDTH, SCREEN_HEIGHT, 0, GL_RGB, GL_UNSIGNED_BYTE, bg_data)
        glBindTexture(GL_TEXTURE_2D, 0)
        return bg_texture
def draw_background():
        bg_texture = load_background() if "images/menu_background.png" else None
        if bg_texture:
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            glDisable(GL_DEPTH_TEST)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, bg_texture)
            glColor4f(1, 1, 1, 1)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 1); glVertex2f(0, 0)
            glTexCoord2f(1, 1); glVertex2f(SCREEN_WIDTH, 0)
            glTexCoord2f(1, 0); glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT)
            glTexCoord2f(0, 0); glVertex2f(0, SCREEN_HEIGHT)
            glEnd()
            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)
            glEnable(GL_DEPTH_TEST)
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()

def draw_text(text, font, x, y):
    text_surface = font.render(text, True, (255, 255, 255))  # White text on black background
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2i(x, SCREEN_HEIGHT - y - height)  # Flip y for OpenGL
    glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

CHARACTER_POSITIONS = [-13.5, 0, 11.5]

def draw_triangle_indicator(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-6.0, 6.0, 0.0)
    glVertex3f(6.0, 6.0, 0.0)
    glVertex3f(0.0, -6.0, 0.0)
    glEnd()
    glPopMatrix()

def character_select(screen, clock, display_size):
    global game_state
    # Set up OpenGL 3D view
    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, display_size[0], display_size[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (SCREEN_WIDTH / SCREEN_HEIGHT), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    global selected_index
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                            messagebox.showinfo("CREDITOS:",
                                                "JESÚS ANTONIO GARCÍA CRUZ - 22280706\n"
                                                "ALAN RUIZ JUAREZ - 22281371\n"
                                                "MONSERRAT GUADALUPE VEGA VILCHIS - 2281374")
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % 3
                elif event.key == pygame.K_RETURN:
                    print(f"Selected character: {selected_index}")
                    running = False  # Proceed to game
                elif event.key == pygame.K_ESCAPE:
                    running = False  # Optionally return to menu

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_background()
        glLoadIdentity()
        gluLookAt(0, 0, 50, 0, 7, 1, 0, 1, 0)

        indicator_x = CHARACTER_POSITIONS[selected_index]
        draw_triangle_indicator(indicator_x, 20, 2)

        #Maid
        x=0
        y=0
        reference_point = [0, 0, 0]
        tra = [12,0,1]
        translation_vector = [11.5, -3, 2]
        objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.scale_matrix_relative(chucho.vestido1,0.8,reference_point),tra),chucho.carasVestido1,0,0,0,0,0,1.0,0,0.5)
        objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.scale_matrix_relative(chucho.verticesLArm,0.8,reference_point),tra),chucho.carasLArm,0,0,0,0,1,1.0,0,0.5)
        objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.scale_matrix_relative(chucho.verticesRArm,0.8,reference_point),tra),chucho.carasRArm,0,1,0,0,1,1.0,0,0.5)
        objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.scale_matrix_relative(chucho.verticesRLeg,0.8,reference_point),tra),chucho.carasRLeg,0,1,1,0,0,1.0,0,0.5)
        objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.scale_matrix_relative(chucho.verticesLLeg,0.8,reference_point),tra),chucho.carasLLeg,0,0,1,0,0,1.0,0,0.5)
        objects.draw_line(chucho.translate_matrix(chucho.sonrisa,translation_vector),x,y)
        objects.draw_line(chucho.translate_matrix(chucho.ojo1a,translation_vector),x,y)
        objects.draw_line(chucho.translate_matrix(chucho.ojo2a,translation_vector),x,y)
        objects.pintar_esfera(12, 12, 1.3,1.5,0,0,0,0)
        
        #toonix
        
        toonix.pintar_torso(2-2,0.7,1,0.3, 0.2, 1) #torso
        toonix.pintar_cabeza(2-2,0.7,1,0.3, 0.2, 1) #cabeza
        toonix.pintar_frente(2-2,0.7,1,0.992,0.701,0.349) #frente
        toonix.pintar_esfera(2-2,11.2,1,0.161, 0.161, 0.161) #cabello
        toonix.pintar_esfera(0-2,3.2,1,0.3, 0.2, 1) #hombro derech
        toonix.pintar_esfera(4-2,3.2,1,0.3, 0.2, 1) #hombro izquierdo
        toonix.pintar_extremidad(1-2,1,1   ,0.3,0.2,1) #pierna izquierda
        toonix.pintar_extremidad(3-2,1,1   ,0.3,0.2,1) #pierna derecha
        toonix.pintar_extremidad(0-2,2.5,1   ,0.3,0.2,1) #brazo izquierdo
        toonix.pintar_extremidad(4-2,2.5,1   ,0.3,0.2,1) #brazo derecho 
        objects.draw_line(chucho.translate_matrix(toonix.marca_frente_v,[0, -7, 3]),0,0) #marca de la frente vertical
        objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h,[0, -7, 3]),0,0) #marca de la frente horizontal
        objects.draw_line(chucho.translate_matrix(toonix.marca_frente_v,[-1, -10, 3]),0,0) #ojo izquierdo
        objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h,[-1, -10, 3]),0,0) #ojo izquierdo
        objects.draw_line(chucho.translate_matrix(toonix.marca_frente_v,[1, -10, 3]),0,0) #ojo derecho
        objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h,[1, -10, 3]),0,0) #ojo derecho
        objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h,[0, -11, 3]),0,0) #ojo derecho
        objects.draw_line(chucho.translate_matrix(toonix.marca_torso,[0, 3, 3]),0,0,(1,1,0,1)) #boca

        ## agrio 
        esfera_x, esfera_y, esfera_z = -14, 6, -1
        bI_x, bI_y, bI_z = -11, 3.5, 21 
        bD_x, bD_y, bD_z = -5.3, 3.5, 21
        pD_x, pD_y, pD_z = -9, 0.5, 21
        iD_x, iD_y, iD_z = -7, 0.5, 21

        ojoI_x, ojoI_y, ojoI_z = -10, 4, 18.7
        ojoI1_x, ojoI1_y, ojoI1_z = -9.6, 3.7, 20
        ojoI2_x, ojoI2_y, ojoI2_z = -9.3, 3.5, 21

        ojoDx, ojoDy, ojoDz = -8, 4, 18.6
        ojoD_1x, ojoD_1y, ojoD_1z = -7.6, 3.7, 20
        ojoD_2x, ojoD_2y, ojoD_2z = -7.3, 3.5, 21.2

        agrio.set_posicion_esfera(esfera_x, esfera_y, esfera_z)
        agrio.set_posicion_BrazoD(bI_x, bI_y, bI_z)
        agrio.set_posicion_BrazoI(bD_x, bD_y, bD_z)
        agrio.set_posicion_PieD(pD_x, pD_y, pD_z)
        agrio.set_posicion_PieI(iD_x, iD_y, iD_z)
        agrio.set_posicion_OjoI(ojoI_x, ojoI_y, ojoI_z)
        agrio.set_posicion_OjoI_1(ojoI1_x, ojoI1_y, ojoI1_z)
        agrio.set_posicion_OjoI_2(ojoI2_x, ojoI2_y, ojoI2_z)
        agrio.set_posicion_OjoD(ojoDx, ojoDy, ojoDz)
        agrio.set_posicion_OjoD_1(ojoD_1x, ojoD_1y, ojoD_1z)
        agrio.set_posicion_OjoD_2(ojoD_2x, ojoD_2y, ojoD_2z)

        agrio.agrio()

        pygame.display.flip()
        clock.tick(60)