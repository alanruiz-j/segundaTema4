import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from . import pinta_agrio as p
from actions import sonido as sonido
from tkinter import messagebox
from actions import escenario as esc
from actions import texto as txt
from actions import objeto as obj
from actions import colisiones as coli 

def run():
    pygame.init()
    pygame.mixer.init()

    display = (600, 600)
    pygame.display.set_caption("A G R I O")
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslate(0, 0, 0)
    glOrtho(0, 15, 0, 15, 0, 6) 

    camera_speed = 0.6
    mouse_sensivity = 0.1
    velocidad = 0.2
    velocidad1 = 0.3


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
    

    vel_y = 0
    gravedad = -0.2
    en_suelo = True 

    angulo_brazo = 0
    angulo_brazo2 = 0

    scene = 1 

    colision1 = False
    colision2 = False 

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)

    pColision_posX = -7 
    pColision_posY = 0  
    pColision_posZ = -7 - 5 - 3 

    pColision_col_width = 2.0
    pColision_col_height = 0.5 
    pColision_col_depth = 2.0

    
    obj1_posX = 20 # Posición base (X)
    obj1_posY = 0  # Posición base (Y)
    obj1_posZ = 0  # Posición base (Z)
    # Dimensiones reales del Cubo (AABB)
    cubo_col_width = 3.0
    cubo_col_height = 3.0
    cubo_col_depth = 3.0


    esfera_radio = 2.0 
    esfera_col_width = esfera_radio * 2
    esfera_col_height = esfera_radio * 2
    esfera_col_depth = esfera_radio * 2

    emocion_actual = None



    def Colision():
        glEnable(GL_DEPTH_TEST)
        glPushMatrix()
        glTranslatef(pColision_posX, pColision_posY, pColision_posZ)
        glColor3f(0.3, 0.5, 0.3)
        obj.draw_rectanguloColi()
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glPopMatrix()

    def Cubo():
        glEnable(GL_DEPTH_TEST)
        glPushMatrix()
        glTranslatef(obj1_posX, obj1_posY, obj1_posZ)
        glTranslatef(0, 3.5, 4)
        if colision1: 
            glColor3f(0.9, 0.2, 0.2)
        else:
            glColor3f(0.7, 0.7, 0.8)
        obj.draw_cube()
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glPopMatrix()

    def Esfera(): 
        glEnable(GL_DEPTH_TEST)
        glPushMatrix()
        glTranslatef(esfera_x, esfera_y, esfera_z)
        if colision2: 
            glColor3f(0.9, 0.2, 0.2)
        else:
            glColor3f(0.2, 0.9, 0.7)
            #lc.iluminacion(0.2, 0.9, 0.7)
        obj.draw_sphere(esfera_radio, 40, 40) 
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glPopMatrix()


    # messagebox.showinfo("Instrucciones",
    #                     "F1 - Mostrar instrucciones\n"
    #                     "F2 - Encender sonido\n"
    #                     "F3 - Apagar sonido\n"
    #                     "F4 - Acerca de quien lo desarrollo\n"
    #                     "ESCAPE - Salir\n"
    #                     "Movimiento:\n"
    #                     "W/A/S/D - Mover cámara\n"
    #                     "Ratón - Rotar vista\n"
    #                     "1 al 7 - Cambiar escenario/Sonidos/Emociones\n"
    #                     "Acciones del personaje:\n"
    #                     "B - Levanta brazo izquierdo\n"
    #                     "I - Levanta brazo derecho\n"
    #                     "SPACE - Salto\n"
    #                     "← - Derecha\n"
    #                     "→ - Izquierda\n"
    #                     "↑ - Sube \n" 
    #                     "↓ - Baja \n")

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                
                if event.key == pygame.K_1:
                    scene = 1
                if event.key == pygame.K_2:
                    scene = 2
                if event.key == pygame.K_3:
                    scene = 3
                if event.key == pygame.K_4:
                    scene = 4
                if event.key == pygame.K_5:
                    scene = 5
                if event.key == pygame.K_6:
                    scene = 6
                if event.key == pygame.K_7:
                    scene = 7
                
                
                if event.key == pygame.K_SPACE and en_suelo:
                    vel_y = 0.2 
                    en_suelo = False
        
        key = pygame.key.get_pressed()

        if key[pygame.K_s]:
            glTranslatef(0, 0, camera_speed)
        if key[pygame.K_w]:
            glTranslatef(0, 0, -camera_speed)
        if key[pygame.K_a]:
            glTranslatef(camera_speed, 0, 0)
        if key[pygame.K_d]:
            glTranslatef(-camera_speed, 0, 0)

        
        x, y = pygame.mouse.get_rel()
        x *= mouse_sensivity
        y *= mouse_sensivity
        if x != 0:
            glRotatef(x, 0, 1, 0)
        if y != 0:
            glRotatef(y, 1, 0, 0)
        pygame.mouse.set_pos(display[0] // 2, display[1] // 2)

        txt.draw_text("Instrucciones F1", -5, 15, 4, 20, 255, 255, 255, 0, 0, 0)
        p.set_angulo_brazo(angulo_brazo)
        p.set_angulo_brazo2(angulo_brazo2)
        p.set_posicion_esfera(esfera_x, esfera_y, esfera_z)
        p.set_posicion_BrazoD(bI_x, bI_y, bI_z)
        p.set_posicion_BrazoI(bD_x, bD_y, bD_z)
        p.set_posicion_PieD(pD_x, pD_y, pD_z)
        p.set_posicion_PieI(iD_x, iD_y, iD_z)
        p.set_posicion_OjoI(ojoI_x, ojoI_y, ojoI_z)
        p.set_posicion_OjoI_1(ojoI1_x, ojoI1_y, ojoI1_z)
        p.set_posicion_OjoI_2(ojoI2_x, ojoI2_y, ojoI2_z)
        p.set_posicion_OjoD(ojoDx, ojoDy, ojoDz)
        p.set_posicion_OjoD_1(ojoD_1x, ojoD_1y, ojoD_1z)
        p.set_posicion_OjoD_2(ojoD_2x, ojoD_2y, ojoD_2z)

        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



        p.ojoD_1()
        p.ojoD_2()
        p.pinEsferaCuer() 
        p.pinBrazoD()
        p.pinBrazoI()
        p.pinPieD()
        p.pinPieI()
        p.ojoI()
        p.ojoI_1()
        p.ojoI_2()
        p.ojoD()

        if emocion_actual:
            p.mostrar_emocion_relativa(emocion_actual)

        
        if scene == 1:
            esc.drawEscenario("images/escenarioA.jpg")
            esc.drawCielo("images/escenarioA.jpg")
            esc.drawPiso("images/escenarioA.jpg")
        elif scene == 2:
            esc.drawCielo("images/escenarioB.jpg")
            esc.drawPiso("images/escenarioB.jpg")
            esc.drawEscenario("images/escenarioB.jpg")
        elif scene == 3:
            esc.drawCielo("images/escenarioC.jpg")
            esc.drawPiso("images/escenarioC.jpg")
            esc.drawEscenario("images/escenarioC.jpg")
        elif scene == 4:
            esc.drawPiso("images/escenarioD.jpg")
            esc.drawCielo("images/escenarioD.jpg")
            esc.drawEscenario("images/escenarioD.jpg")
        elif scene == 5:
            esc.drawCielo("images/escenarioE.jpg")
            esc.drawPiso("images/escenarioE.jpg")
            esc.drawEscenario("images/escenarioE.jpg")
        elif scene == 6:
            esc.drawPiso("images/escenarioF.jpg")
            esc.drawCielo("images/escenarioF.jpg")
            esc.drawEscenario("images/escenarioF.jpg")
        elif scene == 7:
            esc.drawCielo("images/escenarioA.jpg")
            esc.drawPiso("images/escenarioA.jpg")
            esc.drawEscenario("images/escenarioA.jpg")

        
        if key[pygame.K_F1]:
            messagebox.showinfo("Instrucciones",
                                "F1 - Mostrar instrucciones\n"
                                "F2 - Encender sonido\n"
                                "F3 - Apagar sonido\n"
                                "F4 - Acerca de quien lo desarrollo\n"
                                "ESCAPE - Salir\n"
                                "Movimiento:\n"
                                "W/A/S/D - Mover cámara\n"
                                "Ratón - Rotar vista\n"
                                "1 al 7 - Cambiar escenario/Sonidos/Emociones\n"
                                "Acciones del personaje:\n"
                                "B - Levanta brazo izquierdo\n"
                                "I - Levanta brazo derecho\n"
                                "SPACE - Salto\n"
                                "← - Derecha\n"
                                "→ - Izquierda\n"
                                "↑ - Sube (personaje)\n"
                                "↓ - Baja (personaje)\n")
        if key[pygame.K_F2]:
            sonido.sonidoOn("sonidos/cancion.wav")
        if key[pygame.K_F3]:
            sonido.sonidoOff()
        if key[pygame.K_F4]:
            txt.draw_text("Realizado por:", -5, 19, 4, 20, 255, 255, 255, 0, 0, 0)
            txt.draw_text("Monserrat Guadalupe Vega Vilchis", -5, 17, 4, 20, 255, 255, 255, 0, 0, 0)
            txt.draw_text("Número de Control: 22281374", -5, 15, 4, 20, 255, 255, 255, 0, 0, 0)
        
        if key[pygame.K_1]:
            print("Emoción actual:", emocion_actual)
            emocion_actual = 'feliz'  
            sonido.sonidoOn("sonidos/candy.wav")
        if key[pygame.K_2]:
            emocion_actual = 'enojo'
            sonido.sonidoOn("sonidos/carrera.wav")
        if key[pygame.K_3]:
            emocion_actual = 'sorpresa'
            sonido.sonidoOn("sonidos/disparo.wav")
        if key[pygame.K_4]:
            emocion_actual = 'sonrojado'
            sonido.sonidoOn("sonidos/ganar.wav")
        if key[pygame.K_5]:
            emocion_actual = 'triste'
            sonido.sonidoOn("sonidos/perder.wav")
        if key[pygame.K_6]:
            emocion_actual = 'normal'
            sonido.sonidoOn("sonidos/normal.wav")
        if key[pygame.K_7]:
            emocion_actual = 'disgusto'
            sonido.sonidoOn("sonidos/disgusto.wav")

        if key[pygame.K_LEFT]:
            esfera_x -= velocidad
            bI_x -= velocidad
            bD_x -= velocidad
            iD_x -= velocidad
            pD_x -= velocidad
            ojoI_x -= velocidad
            ojoI1_x -= velocidad
            ojoI2_x -= velocidad
            ojoDx -= velocidad
            ojoD_1x -= velocidad
            ojoD_2x -= velocidad
        if key[pygame.K_RIGHT]:
            esfera_x += velocidad
            bI_x += velocidad
            bD_x += velocidad
            iD_x += velocidad
            pD_x += velocidad
            ojoI_x += velocidad
            ojoI1_x += velocidad
            ojoI2_x += velocidad
            ojoDx += velocidad
            ojoD_1x += velocidad
            ojoD_2x += velocidad
        if key[pygame.K_UP]: 
            esfera_z -= velocidad 
            bI_z -= velocidad
            bD_z -= velocidad
            iD_z -= velocidad
            pD_z -= velocidad
            ojoI_z -= velocidad
            ojoI1_z -= velocidad
            ojoI2_z -= velocidad
            ojoDz -= velocidad
            ojoD_1z -= velocidad
            ojoD_2z -= velocidad
        if key[pygame.K_DOWN]: 
            esfera_z += velocidad
            bI_z += velocidad
            bD_z += velocidad
            iD_z += velocidad
            pD_z += velocidad
            ojoI_z += velocidad
            ojoI1_z += velocidad
            ojoI2_z += velocidad
            ojoDz += velocidad
            ojoD_1z += velocidad
            ojoD_2z += velocidad

        if key[pygame.K_b]: 
            angulo_brazo = 80
        else:
            angulo_brazo = 0
        if key[pygame.K_i]: 
            angulo_brazo2 = 80
        else:
            angulo_brazo2 = 0

        if not en_suelo:
            esfera_y += vel_y 
            pD_y += vel_y
            iD_y += vel_y
            bI_y += vel_y
            bD_y += vel_y
            ojoI_y += vel_y
            ojoI1_y += vel_y
            ojoI2_y += vel_y
            ojoDy += vel_y
            ojoD_1y += vel_y
            ojoD_2y += vel_y

            vel_y += gravedad 
            if esfera_y <= 6.5: 
                esfera_y = 6.5
                en_suelo = True
                vel_y = 0
                pD_y = 2.5 
                iD_y = 2.5
                bI_y = 5.5
                bD_y = 5.5
                ojoI_y = 7
                ojoI1_y = 7
                ojoI2_y = 7
                ojoDy = 7
                ojoD_1y = 7.01
                ojoD_2y = 7

        esfera_centro_x, esfera_centro_y, esfera_centro_z = esfera_x, esfera_y, esfera_z

        cubo_centro_x = obj1_posX
        cubo_centro_y = obj1_posY + 3.5
        cubo_centro_z = obj1_posZ + 4.0

        
        pColision_centro_x = pColision_posX
        pColision_centro_y = pColision_posY
        pColision_centro_z = pColision_posZ

        
        colision1 = coli.aabbCollision(
            esfera_centro_x, esfera_centro_y, esfera_centro_z,
            esfera_col_width, esfera_col_height, esfera_col_depth,
            cubo_centro_x, cubo_centro_y, cubo_centro_z,
            cubo_col_width, cubo_col_height, cubo_col_depth
        )

        colision2 = coli.aabbCollision(
            esfera_centro_x, esfera_centro_y, esfera_centro_z,
            esfera_col_width, esfera_col_height, esfera_col_depth,
            pColision_centro_x, pColision_centro_y, pColision_centro_z,
            pColision_col_width, pColision_col_height, pColision_col_depth
        )

        
        if colision1 or colision2: 
            txt.draw_text("C O L I S I O N", -5, 15, 4, 20, 255, 255, 255, 0, 0, 0)
            

        Colision() 
        Cubo()     
        Esfera()   

        pygame.display.flip()