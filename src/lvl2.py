# Archivo principal del juego (p.ej., game.py)
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from personajes import toonix, chucho
from .preguntas_lvl2 import QUESTIONS
import random
from actions import objects


# --- Definiciones Globales y Constantes ---
COLORS = {
    'blue': (208/255.0, 255/255.0, 248/255.0), # Azul Pastel
    'green': (222/255.0, 255/255.0, 160/255.0), # Verde Pastel
    'red': (249/255.0, 224/255.0, 224/255.0),   # Rojo Pastel
    'white': (0.2, 0.45, 0.15)                     # Blanco se mantiene
}

CHARACTER_VISUAL_SCALE_FACTOR = 0.1

# Dimensiones BASE del CUBOIDE DE COLISIÓN (a escala 100% del modelo Toonix)
BASE_PLAYER_COLLISION_WIDTH = 4.0
BASE_PLAYER_COLLISION_HEIGHT = 14.0
BASE_PLAYER_COLLISION_DEPTH = 1.0

# Dimensiones EFECTIVAS del CUBOIDE DE COLISIÓN (escaladas por el factor visual)
PLAYER_COLLISION_WIDTH = BASE_PLAYER_COLLISION_WIDTH * CHARACTER_VISUAL_SCALE_FACTOR
_player_collision_height_scaled = BASE_PLAYER_COLLISION_HEIGHT * CHARACTER_VISUAL_SCALE_FACTOR
PLAYER_COLLISION_DEPTH = BASE_PLAYER_COLLISION_DEPTH * CHARACTER_VISUAL_SCALE_FACTOR

# Aumentar la altura del colisionador en un 10% adicional (solicitud anterior)
PLAYER_COLLISION_HEIGHT = _player_collision_height_scaled * 1.10

# Medias dimensiones para cálculos
collider_half_width = PLAYER_COLLISION_WIDTH / 2.0
collider_half_height = PLAYER_COLLISION_HEIGHT / 2.0 # Usa la altura final, escalada y aumentada
collider_half_depth = PLAYER_COLLISION_DEPTH / 2.0

# Constantes para centrar el modelo visual de Toonix.
TOONIX_DESIGN_CENTER_X = 11.0
Y_PIES_DISEÑO_ORIGINAL = 0.25 
TOONIX_DESIGN_CENTER_Y = Y_PIES_DISEÑO_ORIGINAL + (BASE_PLAYER_COLLISION_HEIGHT / 2.0)
TOONIX_DESIGN_CENTER_Z = 0.5

# --- Funciones de Dibujo Auxiliares (en el archivo principal del juego) ---

def draw_player_character():
    offsetX = -TOONIX_DESIGN_CENTER_X
    offsetY = -TOONIX_DESIGN_CENTER_Y 
    offsetZ = -TOONIX_DESIGN_CENTER_Z
    # Dibujo básico de cuerpo y cabeza
    toonix.pintar_torso(11 + offsetX, 0.7 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_cabeza(11 + offsetX, 0.7 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_frente(11 + offsetX, 0.7 + offsetY, 1 + offsetZ, 0.992, 0.701, 0.349)
    toonix.pintar_esfera(11 + offsetX, 11.2 + offsetY, 1 + offsetZ, 0.161, 0.161, 0.161)  # cabello
    # Extremidades
    toonix.pintar_esfera(9 + offsetX, 3.2 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_esfera(13 + offsetX, 3.2 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_extremidad(10 + offsetX, 1.0 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_extremidad(12 + offsetX, 1.0 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_extremidad(9  + offsetX, 2.5 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_extremidad(13 + offsetX, 2.5 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_v, [11 + offsetX, -7 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [11 + offsetX, -7 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_v, [10 + offsetX, -10 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [10 + offsetX, -10 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [12 + offsetX, -10 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [11 + offsetX, -11 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_torso, [11 + offsetX, 3 + offsetY, 3 + offsetZ]),0, 0,(1, 1, 0, 1))
    
def draw_player_character():
    offsetX = -TOONIX_DESIGN_CENTER_X
    offsetY = -TOONIX_DESIGN_CENTER_Y 
    offsetZ = -TOONIX_DESIGN_CENTER_Z

    # Cuerpo y cabeza igual que antes
    toonix.pintar_torso(11 + offsetX, 0.7 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_cabeza(11 + offsetX, 0.7 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_frente(11 + offsetX, 0.7 + offsetY, 1 + offsetZ, 0.992, 0.701, 0.349)
    toonix.pintar_esfera(11 + offsetX, 11.2 + offsetY, 1 + offsetZ, 0.161, 0.161, 0.161)

    # Extremidades en reposo
    toonix.pintar_extremidad(10 + offsetX, 1.0 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_extremidad(12 + offsetX, 1.0 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_extremidad( 9 + offsetX, 2.5 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_extremidad(13 + offsetX, 2.5 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)

    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_v, [11 + offsetX, -7 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [11 + offsetX, -7 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_v, [10 + offsetX, -10 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [10 + offsetX, -10 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [12 + offsetX, -10 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [11 + offsetX, -11 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_torso, [11 + offsetX, 3 + offsetY, 3 + offsetZ]),0, 0,(1, 1, 0, 1))

def draw_player_jump_character():
    offsetX = -TOONIX_DESIGN_CENTER_X
    offsetY = -TOONIX_DESIGN_CENTER_Y 
    offsetZ = -TOONIX_DESIGN_CENTER_Z

    # Cuerpo y cabeza igual que antes
    toonix.pintar_torso(11 + offsetX, 0.7 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_cabeza(11 + offsetX, 0.7 + offsetY, 1 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_frente(11 + offsetX, 0.7 + offsetY, 1 + offsetZ, 0.992, 0.701, 0.349)
    toonix.pintar_esfera(11 + offsetX, 11.2 + offsetY, 1 + offsetZ, 0.161, 0.161, 0.161)

    # Extremidades en pose de salto
    #piernas
    toonix.pintar_extremidad_izq_arriba(10 + offsetX, 4.4 + offsetY, 0.6 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_extremidad_der_arriba(12   + offsetX, 4.4 + offsetY, 0.6 + offsetZ, 0.3, 0.2, 1)
    #brazos
    toonix.pintar_extremidad_der_arriba(10+ offsetX, 5.4 + offsetY, 0.6 + offsetZ, 0.3, 0.2, 1)
    toonix.pintar_extremidad_izq_arriba(12 + offsetX, 5.4 + offsetY, 0.6 + offsetZ, 0.3, 0.2, 1)

    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_v, [11 + offsetX, -7 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [11 + offsetX, -7 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_v, [10 + offsetX, -10 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [10 + offsetX, -10 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [12 + offsetX, -10 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_frente_h, [11 + offsetX, -11 + offsetY, 3 + offsetZ]),0, 0)
    objects.draw_line(chucho.translate_matrix(toonix.marca_torso, [11 + offsetX, 3 + offsetY, 3 + offsetZ]),0, 0,(1, 1, 0, 1))
    
def run():
    # --- Inicialización de Pygame, OpenGL y Audio ---
    pygame.init()
    pygame.mixer.init()
    display_width, display_height = 1500, 800
    pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Nivel 2: Organismo multicelular")
    glEnable(GL_DEPTH_TEST)

    # Música de fondo
    pygame.mixer.music.load("sonidos/cancion.wav")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    # Efectos de sonido
    jump_sfx        = pygame.mixer.Sound("sonidos/jump.wav")
    land_sfx        = pygame.mixer.Sound("sonidos/land.wav")
    correct_sfx     = pygame.mixer.Sound("sonidos/correct.wav")
    incorrect_sfx   = pygame.mixer.Sound("sonidos/incorrect.wav")
    end_success_sfx = pygame.mixer.Sound("sonidos/success_end.wav")
    end_fail_sfx    = pygame.mixer.Sound("sonidos/failure_end.wav")

    # Cargar el fondo como textura
    bg_surface = pygame.image.load("images/fondo_lvl2.jpg").convert_alpha()
    bg_w, bg_h = bg_surface.get_size()
    bg_data = pygame.image.tostring(bg_surface, "RGBA", True)
    bg_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, bg_tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, bg_w, bg_h, 0, GL_RGBA, GL_UNSIGNED_BYTE, bg_data)

    # Proyección 3D
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, display_width / display_height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    clock = pygame.time.Clock()

    # Estadísticas
    correctas = 0
    rondas    = 1
    end_game  = False

    # Auxiliar para preguntas
    def pick_question():
        sel = random.choice(QUESTIONS)
        return sel['question'], sel['choices'], sel['correct']

    # Pregunta inicial
    q_text, (choice1, choice2, choice3), correct_index = pick_question()

    # Parámetros de la plataforma blanca y muros
    y_bot     = -1.0
    plat_y_min, plat_y_max = -0.5, 0.5
    plat_z_min, plat_z_max = -0.25, 0.25
    white_left  = -30
    white_right =  30
    white_top   = y_bot + plat_z_max

    # Definición de plataformas de respuesta
    plat_x_min, plat_x_max = -2, 2
    gap     = 1
    small_w = plat_x_max - plat_x_min
    plataformas_colision = [
        # Blanca (suelo)
        {
            'id': 'white',
            'abs_x_min': white_left, 'abs_x_max': white_right,
            'y_top': white_top,
            'abs_z_min': plat_y_min, 'abs_z_max': plat_y_max,
            'draw_args': (white_left, white_right, plat_y_min - 3, plat_y_max + 1, plat_z_min, plat_z_max),
            'center_x_for_draw': 0.0, 'center_y_for_draw': y_bot,
            'color': COLORS['white']
        },
        # Verde (reintentar)
        {
            'id': 'green',
            'abs_x_min': -(small_w + gap) + plat_x_min, 'abs_x_max': -(small_w + gap) + plat_x_max,
            'y_top': white_top + 2.0,
            'abs_z_min': plat_y_min, 'abs_z_max': plat_y_max,
            'draw_args': (plat_x_min, plat_x_max, plat_y_min, plat_y_max, plat_z_min, plat_z_max),
            'center_x_for_draw': -(small_w + gap), 'center_y_for_draw': y_bot + 2.0,
            'color': COLORS['green']
        },
        # Azul (mensaje)
        {
            'id': 'blue',
            'abs_x_min': plat_x_min, 'abs_x_max': plat_x_max,
            'y_top': white_top + 2.0,
            'abs_z_min': plat_y_min, 'abs_z_max': plat_y_max,
            'draw_args': (plat_x_min, plat_x_max, plat_y_min, plat_y_max, plat_z_min, plat_z_max),
            'center_x_for_draw': 0.0, 'center_y_for_draw': y_bot + 2.0,
            'color': COLORS['blue']
        },
        # Roja (volver al menú)
        {
            'id': 'red',
            'abs_x_min': (small_w + gap) + plat_x_min, 'abs_x_max': (small_w + gap) + plat_x_max,
            'y_top': white_top + 2.0,
            'abs_z_min': plat_y_min, 'abs_z_max': plat_y_max,
            'draw_args': (plat_x_min, plat_x_max, plat_y_min, plat_y_max, plat_z_min, plat_z_max),
            'center_x_for_draw': small_w + gap, 'center_y_for_draw': y_bot + 2.0,
            'color': COLORS['red']
        }
    ]

    mapping = {'green': 0, 'blue': 1, 'red': 2}

    # Estado del jugador
    player_x = 0.0
    player_y = white_top + collider_half_height
    player_z = 0.0
    player_vy= 0.0
    speed    = 0.15
    gravity  = 0.04
    jump_v   = math.sqrt(2 * gravity * PLAYER_COLLISION_HEIGHT * 1.5) + 0.1
    is_grounded = True

    # Bucle principal
    while True:
        # --- Manejo de eventos ---
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "menu"
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                return "menu"
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE and is_grounded:
                player_vy = jump_v
                is_grounded = False
                jump_sfx.play()

        # Fin de juego
        if not end_game and rondas > 7:
            end_game = True
            q_text   = f"Fin del juego                  Puntuación final: {correctas}/5"
            choice1  = "Reintentar"
            choice2  = "¡Felicidades!" if correctas >= 5 else "Lástima :("
            choice3  = "Volver al menú"
            correct_index = -1
            (end_success_sfx if correctas >= 5 else end_fail_sfx).play()

        # Física vertical
        if not is_grounded:
            player_vy -= gravity
        next_y = player_y + player_vy

        # Colisión vertical
        landed = False
        plat_landed = None
        bot_cur = player_y - collider_half_height
        bot_nxt = next_y  - collider_half_height
        if player_vy <= 0:
            for p in plataformas_colision:
                lx, rx = player_x - collider_half_width, player_x + collider_half_width
                nz, fz = player_z - collider_half_depth, player_z + collider_half_depth
                if lx < p['abs_x_max'] and rx > p['abs_x_min'] and nz < p['abs_z_max'] and fz > p['abs_z_min']:
                    if bot_cur >= p['y_top'] and bot_nxt <= p['y_top']:
                        next_y = p['y_top'] + collider_half_height
                        player_vy = 0
                        landed = True
                        plat_landed = p
                        break
        player_y = next_y

        if landed and not is_grounded:
            land_sfx.play()

        # Lógica de fin de juego o respuesta
        if end_game and landed and plat_landed:
            if plat_landed['id'] == 'green':
                correctas, rondas, end_game = 0, 1, False
                q_text, (choice1, choice2, choice3), correct_index = pick_question()
                player_y = white_top + collider_half_height
                is_grounded = True
            elif plat_landed['id'] == 'red':
                pygame.mixer.music.stop()
                return "menu"
        elif not end_game and landed and plat_landed and plat_landed['id'] in mapping:
            idx = mapping[plat_landed['id']]
            if idx == correct_index:
                correctas += 1
                correct_sfx.play()
            else:
                incorrect_sfx.play()
            rondas += 1
            q_text, (choice1, choice2, choice3), correct_index = pick_question()
            player_y = white_top + collider_half_height
            is_grounded = True

        # Movimiento horizontal con colisión en muros
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * speed
        player_x += dx
        min_x = white_left  + collider_half_width + 20
        max_x = white_right - collider_half_width - 20
        player_x = max(min_x, min(player_x, max_x))

        is_grounded = landed

        # --- Render ---
        # 1) Fondo en 2D
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix(); glLoadIdentity()
        glOrtho(0, display_width, display_height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix(); glLoadIdentity()

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, bg_tex)
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(0, 0)
        glTexCoord2f(1, 0); glVertex2f(display_width, 0)
        glTexCoord2f(1, 1); glVertex2f(display_width, display_height)
        glTexCoord2f(0, 1); glVertex2f(0, display_height)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

        # 2) Escena 3D
        glClear(GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(-player_x, -(player_y + 1.5), -15)

        # Dibujar muros
        wall_h = 15.0; wt = 1.2; wy = white_top + wall_h/2
        for wx in (white_left + 19.3, white_right - 19.3):
            glPushMatrix()
            glTranslatef(wx, wy, 0)
            toonix.setColor(0.36, 0.29, 0.18)
            toonix.draw_cube(-wt/2, wt/2, plat_y_min, plat_y_max, -wall_h/2, wall_h/2)
            glPopMatrix()

        # Dibujar plataformas
        for p in plataformas_colision:
            glPushMatrix()
            glTranslatef(p['center_x_for_draw'], p['center_y_for_draw'], 0.0)
            toonix.setColor(*p['color'])
            toonix.draw_cube(*p['draw_args'])
            glPopMatrix()

        # Dibujar personaje
        glPushMatrix()
        glTranslatef(player_x, player_y, player_z)
        glScalef(CHARACTER_VISUAL_SCALE_FACTOR,
                 CHARACTER_VISUAL_SCALE_FACTOR,
                 CHARACTER_VISUAL_SCALE_FACTOR)
        if is_grounded:
            draw_player_character()
        else:
            draw_player_jump_character()
        glPopMatrix()

        # UI
        glPushMatrix()
        toonix.text("Muevete con A y D, salta con espacio para responder",-4, -1, 2, 30, 255,255,255, 0,0,0)
        toonix.text(q_text, -6.5, 4, 0.7, 42, 255,255,255, 0,0,0)
        toonix.text(choice1, -6.8, 0.8, 0.7, 35,34,34,59,222,255,160)
        toonix.text(choice2, -1.9, 0.8, 0.7, 35,34,34,59,208,255,248)
        toonix.text(choice3, 3.0, 0.8, 0.7, 35,34,34,59,249,224,224)
        toonix.text(f"Ronda: {rondas} / 7", 3, -2, 0.7, 45,34,34,59,249,224,224)
        toonix.text(f"Correctas: {correctas} / 5", -6, -2, 0.7, 45,34,34,59,249,224,224)
        toonix.text("Presiona ESC para volver al menú", -3, -3, 0.7, 35,34,34,59,249,224,224)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)





if __name__ == '__main__':
    run()