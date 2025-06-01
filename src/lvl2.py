import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from . import pinta_toonix as p
from tkinter import messagebox
from personajes import toonix

# Constantes
CAMERA_SPEED = 0.6
MOUSE_SENSITIVITY = 0.1
MOVE_SPEED = 0.3
DISPLAY = (1500, 800)

# Variables de estado (serán inicializadas en run)
expresion = 1
pose = 1
fondo = 1
volumen = True
cube_pos = [11.5, 0.5, 1.5]

# Diccionarios para mapeo de teclas
expresiones_keys = {K_r: 1, K_t: 2, K_y: 3, K_u: 4, K_i: 5, K_8: 6, K_9: 7}
poses_keys = {K_f: 1, K_g: 2, K_h: 3, K_j: 4, K_k: 5, K_l: 6, K_0: 7}
fondos_keys = {
    K_1: (1, "sonidos/steven.wav"),
    K_2: (2, "sonidos/gumball.wav"),
    K_3: (3, "sonidos/powerpuff.wav"),
    K_4: (4, "sonidos/adventure.wav"),
    K_5: (5, "sonidos/bears.wav"),
    K_6: (6, "sonidos/courage.wav"),
    K_7: (7, "sonidos/regular.wav")
}

# Funciones auxiliares
def manejar_input():
    global expresion, pose, fondo, volumen, cube_pos
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key in [K_ESCAPE, K_RETURN]):
            toonix.sonidoOff()
            return False
        if event.type == KEYDOWN:
            if event.key == K_p:
                volumen = True
            if event.key == K_o:
                toonix.sonidoOff()
                volumen = False

    keys = pygame.key.get_pressed()
    mover_camara(keys)
    actualizar_estado(keys)
    mover_personaje(keys)
    mostrar_mensajes(keys)
    return True

def mover_camara(keys):
    if keys[K_w]: glTranslate(0, 0, -CAMERA_SPEED)
    if keys[K_s]: glTranslate(0, 0, CAMERA_SPEED)
    if keys[K_a]: glTranslate(CAMERA_SPEED, 0, 0)
    if keys[K_d]: glTranslate(-CAMERA_SPEED, 0, 0)
    if keys[K_z]: glTranslate(0, -CAMERA_SPEED, 0)
    if keys[K_x]: glTranslate(0, CAMERA_SPEED, 0)

def actualizar_estado(keys):
    global expresion, pose, fondo
    for key, val in expresiones_keys.items():
        if keys[key]: expresion = val
    for key, val in poses_keys.items():
        if keys[key]: pose = val
    for key, (f, sound) in fondos_keys.items():
        if keys[key]:
            fondo = f
            if volumen:
                toonix.sonidoOn(sound)

def mover_personaje(keys):
    global cube_pos
    if keys[K_LEFT]:
        cube_pos[0] -= MOVE_SPEED
    if keys[K_RIGHT]:
        cube_pos[0] += MOVE_SPEED
    if keys[K_DOWN]:
        cube_pos[2] -= MOVE_SPEED
    if keys[K_UP]:
        cube_pos[2] += MOVE_SPEED

def mostrar_mensajes(keys):
    if keys[K_F1]:
        messagebox.showinfo("Instrucciones", 
            "Mover cámara: W,A,S,D\n" +
            "Rotar vista: Ratón\n\n" +
            "Mover personaje: Flechas\n" +
            "POSES: F=1, G=2, H=3, J=4, K=5, L=6, 0=7\n" +
            "EXPRESIONES: R=1, T=2, Y=3, U=4, I=5, 8=6, 9=7\n" +
            "ESCENARIOS: 1 a 7\n" +
            "Encender sonido: P\nApagar sonido: O\nInstrucciones: F1\nDesarrollador: F2")
    if keys[K_F2]:
        messagebox.showinfo("", "Programa creado por Alan Ruiz Juárez")

def controlar_mouse():
    x, y = pygame.mouse.get_rel()
    x *= MOUSE_SENSITIVITY
    if x != 0:
        glRotate(x, 0, 1, 0)
    pygame.mouse.set_pos(DISPLAY[0] // 2, DISPLAY[1] // 2)

def renderizar():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Dibujar texto en pantalla (instrucciones)
    toonix.text("Instrucciones", -5, 10, -4, 40, 255, 255, 255, 0, 0, 0)

    # Dibujar escenario (no se mueve con personaje)
    if fondo == 1:
        toonix.drawEscenario("images/toonix_fondo1.jpg")
        toonix.drawPiso("images/toonix_suelo1.jpg")
    elif fondo == 2:
        toonix.drawEscenario("images/toonix_fondo2.jpg")
        toonix.drawPiso("images/toonix_suelo2.jpg")
    elif fondo == 3:
        toonix.drawEscenario("images/toonix_fondo3.jpg")
        toonix.drawPiso("images/toonix_suelo3.jpg")
    elif fondo == 4:
        toonix.drawEscenario("images/toonix_fondo4.jpg")
        toonix.drawPiso("images/toonix_suelo4.jpg")
    elif fondo == 5:
        toonix.drawEscenario("images/toonix_fondo5.jpg")
        toonix.drawPiso("images/toonix_suelo5.jpg")
    elif fondo == 6:
        toonix.drawEscenario("images/toonix_fondo6.jpg")
        toonix.drawPiso("images/toonix_suelo6.jpg")
    elif fondo == 7:
        toonix.drawEscenario("images/toonix_fondo7.jpg")
        toonix.drawPiso("images/toonix_suelo7.jpg")

    # Dibujar personaje centrado en cube_pos
    glPushMatrix()
    
    #cubos
    p.pintar_colision(11, 3, -2, 1, 0, 1)
    p.pintar_colision(-11, 3, -2, 0, 1, 1)
    
    glTranslatef(cube_pos[0], cube_pos[1], cube_pos[2])
    # Personaje (poses)
    #cara
    if expresion == 1: #normal
        p.pintar_ojo_normal(-12.3,6.5,-0.55,0,0,0) #ojo izquierdo
        p.pintar_ojo_normal(-10,6.5,-0.55,0,0,0) #ojo derecho
        p.pintar_boca_normal(-11.2,5.5,-0.55,0,0,0) #ojo derecho
    elif expresion == 2: #feliz
        p.pintar_ojo_feliz(-12.3,6.5,-0.55,0,0,0) #ojo izquierdo
        p.pintar_ojo_feliz(-10,6.5,-0.55,0,0,0) #ojo derecho
        p.pintar_boca_feliz(-11.2,5.5,-0.55,0,0,0) #ojo derecho
    elif expresion == 3: #triste
        p.pintar_ojo_triste(-12.3,6.5,-0.55,0,0,0) #ojo izquierdo
        p.pintar_ojo_triste(-10,6.5,-0.55,0,0,0) #ojo derecho
        p.pintar_boca_triste(-11.2,5.5,-0.55,0,0,0) #ojo derecho
    elif expresion == 4: #enojado
        p.pintar_ojo_enojado1(-12.3,6.5,-0.55,0,0,0) #ojo izquierdo
        p.pintar_ojo_enojado2(-10,6.5,-0.55,0,0,0) #ojo derecho
        p.pintar_boca_enojado(-11.2,5.5,-0.55,0,0,0) #ojo derecho
    elif expresion == 5: #sorprendido
        p.pintar_ojo_normal(-12.3,6.5,-0.55,0,0,0) #ojo izquierdo
        p.pintar_ojo_normal(-10,6.5,-0.55,0,0,0) #ojo derecho
        p.pintar_boca_sorprendido(-11.2,5.5,-0.55,0,0,0) #ojo derecho
    elif expresion == 6: #guiño
        p.pintar_ojo_normal(-12.3,6.5,-0.55,0,0,0) #ojo izquierdo
        p.pintar_ojo_feliz(-10,6.5,-0.55,0,0,0) #ojo derecho
        p.pintar_boca_feliz(-11.2,5.5,-0.55,0,0,0) #ojo derecho
    elif expresion == 7: #muerto
        p.pintar_ojo_muerto(-12.3,6.5,-0.55,0,0,0) #ojo izquierdo
        p.pintar_ojo_muerto(-10,6.5,-0.55,0,0,0) #ojo derecho
        p.pintar_boca_sorprendido(-11.2,5.5,-0.55,0,0,0) #ojo derecho
    
    if pose == 1:
        p.pintar_extremidad(-12, 1, 1, 0.3, 0.2, 1)
        p.pintar_extremidad(-10, 1, 1, 0.3, 0.2, 1)
        p.pintar_extremidad(-13, 2.5, 1, 0.3, 0.2, 1)
        p.pintar_extremidad(-9, 2.5, 1, 0.3, 0.2, 1)
    elif pose == 2:
        p.pintar_extremidad(-12, 1, 1, 0.3, 0.2, 1)
        p.pintar_extremidad(-10, 1, 1, 0.3, 0.2, 1)
        p.pintar_extremidad_der_arriba(-6.8, 1.7, 0.6, 0.3, 0.2, 1)
        p.pintar_extremidad(-9, 2.5, 1, 0.3, 0.2, 1)
    elif pose == 3:
        p.pintar_extremidad(-12, 1, 1, 0.3, 0.2, 1)
        p.pintar_extremidad(-10, 1, 1, 0.3, 0.2, 1)
        p.pintar_extremidad(-13, 2.5, 1, 0.3, 0.2, 1)
        p.pintar_extremidad_izq_arriba(-4.2, 1.7, 0.6, 0.3, 0.2, 1)
    elif pose == 4:
        p.pintar_extremidad_izq_arriba(-6.3, 0.7, 0.6, 0.3, 0.2, 1)
        p.pintar_extremidad(-10, 1, 1, 0.3, 0.2, 1)
        p.pintar_extremidad_der_arriba(-6.8, 1.7, 0.6, 0.3, 0.2, 1)
        p.pintar_extremidad(-9, 2.5, 1, 0.3, 0.2, 1)
    elif pose == 5:
        p.pintar_extremidad_izq_arriba(-6.3, 0.7, 0.6, 0.3, 0.2, 1)
        p.pintar_extremidad_der_arriba(-4.5, 0.7, 0.6, 0.3, 0.2, 1)
        p.pintar_extremidad_der_arriba(-6.8, 1.7, 0.6, 0.3, 0.2, 1)
        p.pintar_extremidad_izq_arriba(-4.2, 1.7, 0.6, 0.3, 0.2, 1)
    elif pose == 6:
        p.pintar_extremidad(-12, 1, 1, 0.3, 0.2, 1)
        p.pintar_extremidad(-10, 1, 1, 0.3, 0.2, 1)
        p.pintar_extremidad_der_arriba(-6.8, 1.7, 0.6, 0.3, 0.2, 1)
        p.pintar_extremidad_izq_arriba(-4.2, 1.7, 0.6, 0.3, 0.2, 1)
    elif pose == 7:
        p.pintar_extremidad(-12, 1, 1, 0.3, 0.2, 1)
        p.pintar_extremidad_der_arriba(-4.5, 0.7, 0.6, 0.3, 0.2, 1)
        p.pintar_extremidad_der_arriba(-6.8, 1.7, 0.6, 0.3, 0.2, 1)
        p.pintar_extremidad_izq_arriba(-4.2, 1.7, 0.6, 0.3, 0.2, 1)

    p.pintar_torso(-11, 0.7, 1, 0.3, 0.2, 1)
    p.marca_torso(-11, 3.4, 0.4, 0.992, 0.701, 0.349)
    p.pintar_cabeza(-11, 0.7, 1, 0.3, 0.2, 1)
    p.pintar_frente(-11, 0.7, 1, 0.992, 0.701, 0.349)
    p.marca_frente(-11.25, 10, -0.55, 0, 0, 0)
    p.pintar_esfera(-11, 11.2, 1, 0.161, 0.161, 0.161)
    p.pintar_esfera(-13, 3.2, 1, 0.3, 0.2, 1)
    p.pintar_esfera(-9, 3.2, 1, 0.3, 0.2, 1)

    glPopMatrix()

def run():
    global expresion, pose, fondo, volumen, cube_pos
    # Reiniciar estado al iniciar
    expresion = 1
    pose = 1
    fondo = 1
    volumen = True
    cube_pos = [11.5, 0.5, 1.5]

    # Inicialización
    pygame.init()
    pygame.mixer.init()
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(True)
    pygame.display.set_mode(DISPLAY, DOUBLEBUF | OPENGL)
    gluPerspective(45, (DISPLAY[0] / DISPLAY[1]), 0.1, 50.0)
    glTranslate(0, 0, 0)
    glOrtho(0, 15, 0, 15, 0, 6)
    #messagebox.showinfo("Instrucciones", "Presiona F1 para leer las instrucciones")
    toonix.sonidoOn("sonidos/steven.wav")

    # Loop principal
    running = True
    while running:
        running = manejar_input()
        controlar_mouse()
        renderizar()
        pygame.display.flip()
        pygame.time.wait(10)

# Si se ejecuta directamente
if __name__ == "__main__":
    run()
