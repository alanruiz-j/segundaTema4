import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import glutInit, glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18
from pygame.locals import *
from actions import objects
from personajes import chucho
import math
from src import hito
from PIL import Image

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800

cam_pos = [0.0, 1.0, 5.0]  # Camera position
yaw, pitch = 0.0, 0.0      # Camera rotation
sensitivity = 0.1
move_speed = 0.1

maid_x=0.0
maid_y=0.0
maid_z=0.0
playerHealth=3

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = self._load_sound("sonidos/cityRuins(shade).wav")
        self.hit_sound = self._load_sound("sonidos/dbdGenerator.wav")
        self.point_sound = self._load_sound("sonidos/dbd_check_start.wav")
        self.enemyHit = self._load_sound("sonidos/critical-hit-sounds-effect.wav")
        self.game_over_sound = self._load_sound("sonidos/a2_you_re_pretty_useless_you_know_that.wav")
        self.victory_sound = self._load_sound("sonidos/diabolical.wav")
        
        if self.background_music:
            self.background_music.set_volume(0.3)
        if self.hit_sound:
            self.hit_sound.set_volume(0.7)
        if self.point_sound:
            self.point_sound.set_volume(0.8)
        if self.enemyHit:
            self.enemyHit.set_volume(0.7)
        if self.game_over_sound:
            self.game_over_sound.set_volume(1.0)
        if self.victory_sound:
            self.victory_sound.set_volume(1.0)

    def _load_sound(self, path):
        try:
            return pygame.mixer.Sound(path)
        except pygame.error as e:
            print(f"Advertencia: No se pudo cargar el sonido '{path}': {e}")
            return None

    def play_music(self):
        if self.background_music and not pygame.mixer.get_busy(): 
            self.background_music.play(-1) 

    def stop_music(self):
        if self.background_music:
            self.background_music.stop()

    def play_hit_sound(self):
        if self.hit_sound:
            self.hit_sound.play()

    def play_point_sound(self):
        if self.point_sound:
            self.point_sound.play()
    
    def play_enemy_hit_sound(self):
        if self.enemyHit:
            self.enemyHit.play()

    def play_game_over_sound(self):
        if self.game_over_sound:
            self.game_over_sound.play()

    def play_victory_sound(self):
        if self.victory_sound:
            self.victory_sound.play()


def load_texture(path):
    img = Image.open(path)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGBA").tobytes()

    width, height = img.size
    texture_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    return texture_id

def draw_textured_floor(texture_id, size=200, y=-0.1, tile_repeat=40):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    glColor3f(1, 1, 1)

    glBegin(GL_QUADS)
    
    glTexCoord2f(0, 0)
    glVertex3f(-size, y, -size)
    
    glTexCoord2f(tile_repeat, 0)
    glVertex3f(size, y, -size)
    
    glTexCoord2f(tile_repeat, tile_repeat)
    glVertex3f(size, y, size)
    
    glTexCoord2f(0, tile_repeat)
    glVertex3f(-size, y, size)

    glEnd()
    
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)

def draw_skybox(size=35.0, textures=None):
    glPushAttrib(GL_ENABLE_BIT)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDisable(GL_BLEND)
    glEnable(GL_TEXTURE_2D)

    glPushMatrix()
    glLoadIdentity()

    faces = [
        ("right",  [[1, -1, -1], [1, -1,  1], [1,  1,  1], [1,  1, -1]]),
        ("left",   [[-1, -1,  1], [-1, -1, -1], [-1,  1, -1], [-1,  1,  1]]),
        ("top",    [[-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1]]),
        ("bottom", [[-1, -1, 1], [1, -1, 1], [1, -1, -1], [-1, -1, -1]]),
        ("front",  [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1]]),
        ("back",   [[1, -1, 1], [-1, -1, 1], [-1, 1, 1], [1, 1, 1]]),
    ]

    for name, verts in faces:
        glBindTexture(GL_TEXTURE_2D, textures[name])
        glBegin(GL_QUADS)
        for i, (x, y, z) in enumerate(verts):
            u = 0 if i in [0, 3] else 1
            v = 0 if i in [0, 1] else 1
            glTexCoord2f(u, v)
            glVertex3f(x * size, y * size, z * size)
        glEnd()

    glPopMatrix()

    glPopAttrib()

def draw_text(text, x, y, font, color=(0, 0, 0)):
    # Render the text to a surface
    text_surface = font.render(text, True, color)
    text_surface = pygame.transform.flip(text_surface, False, True)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()

    # Prepare OpenGL to draw 2D overlay
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -1, 1)  # 2D projection
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

    # Enable texture drawing
    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Draw textured quad
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + width, y)
    glTexCoord2f(1, 1); glVertex2f(x + width, y + height)
    glTexCoord2f(0, 1); glVertex2f(x, y + height)
    glEnd()

    # Cleanup
    glDeleteTextures([texture_id])
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    # Restore projection
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def create_text_texture(text, font, color=(255, 255, 255), outline_color=(0, 0, 0), outline_width=2):
    # Calculate the size of the text with padding for outline
    text_width, text_height = font.size(text)
    width = text_width + outline_width * 2
    height = text_height + outline_width * 2
    
    # Create a transparent surface
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw outline
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx == 0 and dy == 0:
                continue
            outline_surf = font.render(text, True, outline_color)
            surface.blit(outline_surf, (dx + outline_width, dy + outline_width))

    # Draw main text
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, (outline_width, outline_width))

    # Flip vertically for OpenGL
    surface = pygame.transform.flip(surface, False, True)
    
    # Convert to OpenGL texture
    texture_data = pygame.image.tostring(surface, "RGBA", True)
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return texture_id, width, height

def draw_textured_quad_3d(texture_id, pos, size=(1.0, 0.5), rotation=0):
    x, y, z = pos
    w, h = size
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPushMatrix()
    
    # Move to position
    glTranslatef(x, y, z)
    
    # Rotate around Y-axis (you can change this)
    glRotatef(rotation, 0, 1, 0)
    
    # Draw quad centered at (0,0)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex3f(-w/2, -h/2, 0)
    glTexCoord2f(1, 1); glVertex3f(w/2, -h/2, 0)
    glTexCoord2f(1, 0); glVertex3f(w/2, h/2, 0)
    glTexCoord2f(0, 0); glVertex3f(-w/2, h/2, 0)
    glEnd()
    
    glPopMatrix()
    glDisable(GL_TEXTURE_2D)

def render_text(text, font, color, position):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=position)
    screen = pygame.display.get_surface()
    screen.blit(surface, rect)

def create_text_texture2(text, font, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    surface = pygame.transform.flip(surface, False, True)
    texture_data = pygame.image.tostring(surface, "RGBA", True)
    width, height = surface.get_size()
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return texture_id, width, height

def draw_textured_quad_2d(texture_id, x, y, width, height):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1); glVertex2f(x - width // 2, y - height // 2)
    glTexCoord2f(1, 1); glVertex2f(x + width // 2, y - height // 2)
    glTexCoord2f(1, 0); glVertex2f(x + width // 2, y + height // 2)
    glTexCoord2f(0, 0); glVertex2f(x - width // 2, y + height // 2)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def show_game_over_screen(font):
    running = True
    play = True
    game_over_texture, w1, h1 = create_text_texture2("GAME OVER", font, color=(255, 0, 0))
    instruction_texture, w2, h2 = create_text_texture2("Presiona R para reintentar o ESC para salir", font)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play = False
                    running = False
                if event.key == pygame.K_r:  # Retry
                    play = True
                    running = False

        # Clear screen to black
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set orthographic projection for 2D
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Draw text as OpenGL quads with textures
        draw_textured_quad_2d(game_over_texture, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, w1, h1)
        draw_textured_quad_2d(instruction_texture, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, w2, h2)

        # Restore matrices
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()
        pygame.time.wait(16)
    return play

def get_camera_direction(yaw, pitch):
    rad_yaw = math.radians(yaw)
    rad_pitch = math.radians(pitch)
    x = math.cos(rad_pitch) * math.sin(rad_yaw)
    y = math.sin(rad_pitch)
    z = -math.cos(rad_pitch) * math.cos(rad_yaw)
    return [x, y, z]

def yawToTarget(from_pos, to_pos):
    dx = to_pos[0] - from_pos[0]
    dz = to_pos[2] - from_pos[2]
    yaw = math.degrees(math.atan2(dx, -dz))
    return yaw

def run():
    global yaw, pitch, cam_pos, maid_x, maid_y, maid_z, playerHealth
    display = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(display)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    game_started = False
    sonidos = SoundManager()
    pygame.display.set_caption("Nivel 3: Humano Moderno")
    icon = pygame.image.load("images/miku.png")  # 32x32 recommended
    pygame.display.set_icon(icon)

    if not game_started:
            game_started = True
            sonidos.play_music()

    pygame.font.init()
    font = pygame.font.SysFont('Verdana', 32)
    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, display[0], display[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, (SCREEN_WIDTH / SCREEN_HEIGHT), 0.1, 150.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    floor_texture = load_texture("images/floor.png")
    glEnable(GL_TEXTURE_2D)
    glutInit()

    
    angle = 0
    hitAngle = 0
    hit = False
    rot = 3
    controls = False
    lvl = 1
    start = True

    ene1H = 4
    ene1x = 20.0
    ene1y = 0.0
    ene1z = 20.0
    attack=False
    ene1Yaw = 0.0
    ene1Pos = [ene1x,ene1y,ene1z]

    hito1H = 4
    hito1x = 0.0
    hito1y = 0.0
    hito1z = 20.0

    hito2H = 4
    hito2x = -20.0
    hito2y = 0.0
    hito2z = 20.0

    MIN_X = -60
    MAX_X = 60
    MIN_Y = -60
    MAX_Y = 60

    skybox_textures = {
    "right": load_texture("images/Box_Right.bmp"),
    "left": load_texture("images/Box_Left.bmp"),
    "top": load_texture("images/Box_Top.bmp"),
    "bottom": load_texture("images/Box_Bottom.bmp"),
    "front": load_texture("images/Box_Front.bmp"),
    "back": load_texture("images/Box_Back.bmp"),
    }

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running=False
                if event.key == pygame.K_t:
                    controls = not controls
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Left click")
                    if abs(maid_x-ene1x) < 7 and abs(maid_z-ene1z) < 7 and ene1H > 0:
                        attack=True
                        ene1H=ene1H-1
                        sonidos.play_enemy_hit_sound()
                        print(ene1H)
                    if abs(maid_x-hito1x) < 7 and abs(maid_z-hito1z) < 7 and hito1H > 0:
                        hito1H=0
                        playerHealth-=1
                        sonidos.play_hit_sound()
                    if abs(maid_x-hito2x) < 7 and abs(maid_z-hito2z) < 7 and hito2H > 0:
                        hito2H=0
                        playerHealth-=1
                        sonidos.play_hit_sound()
                elif event.button == 2:
                    print("Middle click")
                elif event.button == 3:
                    print("Right click")

        
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        sensitivity = 0.2
        yaw += mouse_dx * sensitivity
        pitch -= mouse_dy * sensitivity
        pitch = max(-179.0, min(179.0, pitch))

        rad_yaw = math.radians(yaw)
        forward = [math.sin(rad_yaw), 0, -math.cos(rad_yaw)]
        right = [math.sin(rad_yaw - math.pi/2), 0, -math.cos(rad_yaw - math.pi/2)]

        keys = pygame.key.get_pressed()
        move_speed = 0.8
        if keys[pygame.K_w]:
            maid_x += forward[0] * move_speed
            maid_z += forward[2] * move_speed
        if keys[pygame.K_s]:
            maid_x -= forward[0] * move_speed
            maid_z -= forward[2] * move_speed
        if keys[pygame.K_a]:
            maid_x += right[0] * move_speed
            maid_z += right[2] * move_speed
        if keys[pygame.K_d]:
            maid_x -= right[0] * move_speed
            maid_z -= right[2] * move_speed

        maid_x = max(MIN_X, min(maid_x, MAX_X))
        maid_z = max(MIN_Y, min(maid_z, MAX_Y))

        # Up/down
        if keys[pygame.K_SPACE]:
            cam_pos[1] += move_speed
        if keys[pygame.K_c]:
            cam_pos[1] -= move_speed

        cam_distance = 30.0
        cam_height = 23.0
        cam_x = maid_x - forward[0] * cam_distance
        cam_y = maid_y + cam_height
        cam_z = maid_z - forward[2] * cam_distance
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        draw_skybox(size=35.0, textures=skybox_textures)

        gluLookAt(cam_x, cam_y, cam_z,
                  maid_x, maid_y + 20.0, maid_z,
                  0, 1, 0)

        angle += rot
        if angle > 45.0:
            angle = 45.0
            rot = -rot
        elif angle < -45.0:
            angle = -45.0
            rot = -rot
            
        if hit == True:
            hitAngle += 5
            if hitAngle > 90:
                hitAngle = 0
                hit = False
        
        x=0
        y=0
        center=[maid_x,maid_y,maid_z]
        reference_point = [0, 0, 0]
        translation_vector = [maid_x, maid_y, maid_z]
        centerLeg = [1.5+maid_x, 7+maid_y, -0.75+maid_z]
        objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.vestido1,translation_vector),'y',180+yaw*-1,center),chucho.carasVestido1,0,0,0,0,0,1.0,0,0.5)
        objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesLArm,translation_vector),'y',180+yaw*-1,center),chucho.carasLArm,0,0,0,0,1,1.0,0,0.5)
        objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesRArm,translation_vector),'y',180+yaw*-1,center),chucho.carasRArm,0,1,0,0,1,1.0,0,0.5)
        objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesRLeg,translation_vector),'x',angle,centerLeg),'y',180+yaw*-1,center),chucho.carasRLeg,0,1,1,0,0,1.0,0,0.5)
        objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesLLeg,translation_vector),'x',angle*-1,centerLeg),'y',180+yaw*-1,center),chucho.carasLLeg,0,0,1,0,0,1.0,0,0.5)
        objects.draw_line(chucho.rotate_matrix(chucho.translate_matrix(chucho.sonrisa,translation_vector),'y',180+yaw*-1,center),x,y)
        objects.draw_line(chucho.rotate_matrix(chucho.translate_matrix(chucho.ojo1a,translation_vector),'y',180+yaw*-1,center),x,y)
        objects.draw_line(chucho.rotate_matrix(chucho.translate_matrix(chucho.ojo2a,translation_vector),'y',180+yaw*-1,center),x,y)
        #objects.pintar_cosa(x,y,chucho.vestido1,chucho.carasVestido1,0,0,0,0,0,1.0,0,0.5)
        objects.pintar_esfera(maid_x, maid_y+14.5,maid_z,1.5,0,0,0,0)

        if lvl == 1 and start == True:
            sonidos.play_point_sound()
            ene1H = 4
            ene1x = -20.0
            ene1y = 0.0
            ene1z = 20.0

            hito1H = 4
            hito1x = 0.0
            hito1y = 0.0
            hito1z = 20.0

            hito2H = 4
            hito2x = 20.0
            hito2y = 0.0
            hito2z = 20.0

            start = False
        
        if lvl == 2 and start == True:
            sonidos.play_point_sound()
            ene1H = 4
            ene1x = 20.0
            ene1y = 0.0
            ene1z = 20.0

            hito1H = 4
            hito1x = 0.0
            hito1y = 0.0
            hito1z = 20.0

            hito2H = 4
            hito2x = -20.0
            hito2y = 0.0
            hito2z = 20.0

            start = False

        if lvl == 3 and start == True:
            sonidos.play_point_sound()
            ene1H = 4
            ene1x = 0.0
            ene1y = 0.0
            ene1z = 20.0

            hito1H = 4
            hito1x = -20.0
            hito1y = 0.0
            hito1z = 20.0

            hito2H = 4
            hito2x = 20.0
            hito2y = 0.0
            hito2z = 20.0

            start = False

        if lvl == 4 and start == True:
            ene1H = 100
            sonidos.play_victory_sound()
            start = False


        

        if ene1H > 0:
            if attack == False:
                hito.persona(True,ene1H,ene1x,ene1y,ene1z,0.1,1.0,0.1)
            else:
                ene1Yaw = yawToTarget(ene1Pos,center)
                if ene1x > maid_x:
                    ene1x=ene1x-0.05
                if ene1x < maid_x:
                    ene1x=ene1x+0.05
                if ene1z > maid_z:
                    ene1z=ene1z-0.05
                if ene1z < maid_z:
                    ene1z=ene1z+0.05
                hito.personaRot(True,ene1H,ene1x,ene1y,ene1z,ene1Yaw,angle,1.0,0.1,0.1)
        if hito1H > 0:
            hito.persona(True,hito1H,hito1x,hito1y,hito1z,0.1,1.0,0.1)
        if hito2H > 0:
            hito.persona(True,hito2H,hito2x,hito2y,hito2z,0.1,1.0,0.1)

        ####

        if controls:
            draw_text("Atacar: 'Click Izquierdo'", 30, 90, font)
            draw_text("Movimiento: 'W,A,S,D'", 30, 120, font)
            draw_text("Camara: 'Movimiento del mouse'", 30, 150, font)
            draw_text("Salir: 'ESC'", 30, 180, font)

        
        draw_textured_floor(floor_texture)
        
        text_tex_id, tex_w, tex_h = create_text_texture("Lee las preguntas y golpea repetidamente al personaje que indica las respuesta correcta", font)
        draw_textured_quad_3d(text_tex_id, pos=(0, 35, -60), size=(110, 5), rotation=0)
        text_tex_id, tex_w, tex_h = create_text_texture("Golpear al personaje incorrecto te quitara 1 vida", font)
        draw_textured_quad_3d(text_tex_id, pos=(0, 30, -60), size=(55, 5), rotation=0)

        if lvl == 1:
            text_tex_id, tex_w, tex_h = create_text_texture("¿Cuál de las siguientes afirmaciones sobre los primeros homínidos es falsa?", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 20, -60), size=(100, 5), rotation=0)
            text_tex_id, tex_w, tex_h = create_text_texture("A) Australopithecus afarensis caminaba erguido pero también era capaz de trepar árboles.", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 15, -60), size=(110, 5), rotation=0)
            text_tex_id, tex_w, tex_h = create_text_texture("B) Homo habilis es conocido por ser uno de los primeros en fabricar herramientas de piedra.", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 10, -60), size=(115, 5), rotation=0)
            text_tex_id, tex_w, tex_h = create_text_texture("C) Homo sapiens convivió con Australopithecus durante miles de años en África.", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 5, -60), size=(110, 5), rotation=0)

        if lvl == 2:
            text_tex_id, tex_w, tex_h = create_text_texture("¿Cuál de estas afirmaciones sobre el cerebro humano en la evolución es falsa?", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 20, -60), size=(100, 5), rotation=0)
            text_tex_id, tex_w, tex_h = create_text_texture("A) El Homo erectus tenía un cerebro más grande que el del ser humano moderno.", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 15, -60), size=(100, 5), rotation=0)
            text_tex_id, tex_w, tex_h = create_text_texture("B) El tamaño del cerebro aumentó significativamente desde Homo habilis hasta Homo sapiens.", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 10, -60), size=(110, 5), rotation=0)
            text_tex_id, tex_w, tex_h = create_text_texture("C) El desarrollo del lenguaje está relacionado con cambios en el cerebro, especialmente en el área de Broca.", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 5, -60), size=(120, 5), rotation=0)

        if lvl == 3:
            text_tex_id, tex_w, tex_h = create_text_texture("¿Cuál de las siguientes afirmaciones sobre los primeros homínidos es falsa?", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 20, -60), size=(100, 5), rotation=0)
            text_tex_id, tex_w, tex_h = create_text_texture("A) Australopithecus afarensis caminaba erguido pero también era capaz de trepar árboles.", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 15, -60), size=(110, 5), rotation=0)
            text_tex_id, tex_w, tex_h = create_text_texture("B) Homo habilis es conocido por ser uno de los primeros en fabricar herramientas de piedra.", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 10, -60), size=(115, 5), rotation=0)
            text_tex_id, tex_w, tex_h = create_text_texture("C) Homo sapiens convivió con Australopithecus durante miles de años en África.", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 5, -60), size=(110, 5), rotation=0)

        if lvl == 4:
            text_tex_id, tex_w, tex_h = create_text_texture("Nivel terminado!!!", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 20, -60), size=(30, 5), rotation=0)
            text_tex_id, tex_w, tex_h = create_text_texture("Presiona 'ESC' para salir", font)
            draw_textured_quad_3d(text_tex_id, pos=(0, 15, -60), size=(35, 5), rotation=0)

        if ene1H == 0:
            lvl=lvl+1
            attack = False
            start = True

        if playerHealth == 0:
            sonidos.play_game_over_sound()
            play = show_game_over_screen(font)
            if play == False:
                running = False
                playerHealth = 3
                lvl = 1
                start = True
                attack = False
                maid_x = 0.0
                maid_y = 0.0
                maid_z = 0.0
            else:
                playerHealth = 3
                lvl = 1
                start = True
                attack = False
                maid_x = 0.0
                maid_y = 0.0
                maid_z = 0.0
        
        text_tex_id, tex_w, tex_h = create_text_texture("A", font)
        draw_textured_quad_3d(text_tex_id, pos=(20, 20, 20), size=(2, 2), rotation=180)
        text_tex_id, tex_w, tex_h = create_text_texture("B", font)
        draw_textured_quad_3d(text_tex_id, pos=(0, 20, 20), size=(2, 2), rotation=180)
        text_tex_id, tex_w, tex_h = create_text_texture("C", font)
        draw_textured_quad_3d(text_tex_id, pos=(-20, 20, 20), size=(2, 2), rotation=180)
        draw_text(f"VIDAS: {playerHealth}", 30, 30, font)
        draw_text("Controles: 'T'", 30, 60, font)
        pygame.display.flip()
        clock.tick(60)

    sonidos.stop_music()
    return "menu"