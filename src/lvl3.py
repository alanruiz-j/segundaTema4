import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import glutInit, glutBitmapCharacter, GLUT_BITMAP_HELVETICA_18
from pygame.locals import *
from actions import objects
from actions import luces
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
maid_y=5.0
maid_z=0.0
playerHealth=3

min_x, max_x = -35, 35
min_y, max_y = -35, 35

cube_x, cube_y = 0.0, 0.0
vel_x, vel_y = 0.2, 0.15 

def draw_cube():
    glBegin(GL_QUADS)

    # Front face
    glColor3f(1.0, 0.0, 0.0)  # Red
    glVertex3f(-1.0, -1.0,  1.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glVertex3f(-1.0,  1.0,  1.0)

    # Back face
    glColor3f(0.0, 1.0, 0.0)  # Green
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0,  1.0, -1.0)
    glVertex3f( 1.0,  1.0, -1.0)
    glVertex3f( 1.0, -1.0, -1.0)

    # Top face
    glColor3f(0.0, 0.0, 1.0)  # Blue
    glVertex3f(-1.0,  1.0, -1.0)
    glVertex3f(-1.0,  1.0,  1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glVertex3f( 1.0,  1.0, -1.0)

    # Bottom face
    glColor3f(1.0, 1.0, 0.0)  # Yellow
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f( 1.0, -1.0, -1.0)
    glVertex3f( 1.0, -1.0,  1.0)
    glVertex3f(-1.0, -1.0,  1.0)

    # Right face
    glColor3f(1.0, 0.0, 1.0)  # Magenta
    glVertex3f( 1.0, -1.0, -1.0)
    glVertex3f( 1.0,  1.0, -1.0)
    glVertex3f( 1.0,  1.0,  1.0)
    glVertex3f( 1.0, -1.0,  1.0)

    # Left face
    glColor3f(0.0, 1.0, 1.0)  # Cyan
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0,  1.0)
    glVertex3f(-1.0,  1.0,  1.0)
    glVertex3f(-1.0,  1.0, -1.0)

    glEnd()

def draw_movable_cube():
    glPushMatrix()
    glTranslatef(cube_x, 8.0, cube_y)  # Move in X and Y
    draw_cube()
    glPopMatrix()

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


def drawEscenario(fileImage):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, load_texture(fileImage))
    
    # Cara frontal
    glBegin(GL_QUADS)
    glColor(1,1,1)
    glTexCoord2f(0,0)
    glVertex3f(-50,0,50)    # Esquina inferior izquierda
    glTexCoord2f(1,0)
    glVertex3f(50,0,50)     # Esquina inferior derecha
    glTexCoord2f(1,1)
    glVertex3f(50,100,50)   # Esquina superior derecha
    glTexCoord2f(0,1)
    glVertex3f(-50,100,50)  # Esquina superior izquierda
    glEnd()

    # Cara lateral derecha
    glBegin(GL_QUADS)
    glColor(1,1,1)
    glTexCoord2f(0,0)
    glVertex3f(50,0,50)     # Esquina inferior izquierda
    glTexCoord2f(1,0)
    glVertex3f(50,0,-50)    # Esquina inferior derecha
    glTexCoord2f(1,1)
    glVertex3f(50,100,-50)  # Esquina superior derecha
    glTexCoord2f(0,1)
    glVertex3f(50,100,50)   # Esquina superior izquierda
    glEnd()

    # Cara trasera
    glBegin(GL_QUADS)
    glColor(1,1,1)
    glTexCoord2f(0,0)
    glVertex3f(50,0,-50)    # Esquina inferior izquierda
    glTexCoord2f(1,0)
    glVertex3f(-50,0,-50)   # Esquina inferior derecha
    glTexCoord2f(1,1)
    glVertex3f(-50,100,-50) # Esquina superior derecha
    glTexCoord2f(0,1)
    glVertex3f(50,100,-50)  # Esquina superior izquierda
    glEnd()

    # Cara lateral izquierda
    glBegin(GL_QUADS)
    glColor(1,1,1)
    glTexCoord2f(0,0)
    glVertex3f(-50,0,-50)   # Esquina inferior izquierda
    glTexCoord2f(1,0)
    glVertex3f(-50,0,50)    # Esquina inferior derecha
    glTexCoord2f(1,1)
    glVertex3f(-50,100,50)  # Esquina superior derecha
    glTexCoord2f(0,1)
    glVertex3f(-50,100,-50) # Esquina superior izquierda
    glEnd()

def drawPiso(fileImage):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, load_texture(fileImage))
    # Tapa inferior
    glBegin(GL_QUADS)
    glColor(1,1,1)
    glTexCoord2f(0,0)
    glVertex3f(-50, 0, 50)   # Esquina inferior izquierda
    glTexCoord2f(1,0)
    glVertex3f(50, 0, 50)    # Esquina inferior derecha
    glTexCoord2f(1,1)
    glVertex3f(50, 0, -50)   # Esquina superior derecha
    glTexCoord2f(0,1)
    glVertex3f(-50, 0, -50)  # Esquina superior izquierda
    glEnd()

def drawCielo(fileImage):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, load_texture(fileImage))
    # Tapa superior
    glBegin(GL_QUADS)
    glColor(1,1,1)
    glTexCoord2f(0,0)
    glVertex3f(-50, 100, 50)  # Esquina inferior izquierda
    glTexCoord2f(1,0)
    glVertex3f(50, 100, 50)   # Esquina inferior derecha
    glTexCoord2f(1,1)
    glVertex3f(50, 100, -50)  # Esquina superior derecha
    glTexCoord2f(0,1)
    glVertex3f(-50, 100, -50) # Esquina superior izquierda
    glEnd()

def sonidoOn(fileName):
    audio_file=fileName
    pygame.mixer.music.load(audio_file)
    pygame.mixer_music.play()

def sonidoOff():
    pygame.mixer_music.stop()

def run():
    global yaw, pitch, cam_pos, maid_x, maid_y, maid_z, playerHealth, cube_x, cube_y, vel_x, vel_y
    display = (SCREEN_WIDTH, SCREEN_HEIGHT)
    #screen = pygame.display.set_mode(display)
    clock = pygame.time.Clock()
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    game_started = False
    #sonidos = SoundManager()
    pygame.mixer.init()
    pygame.display.set_caption("Nivel 3: Humano Moderno")
    icon = pygame.image.load("images/miku.png")  # 32x32 recommended
    pygame.display.set_icon(icon)


    pygame.font.init()
    font = pygame.font.SysFont('Verdana', 32)
    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, display[0], display[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslate(0, 0, 0)
    glOrtho(0, 15, 0, 15, 0, 6)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glutInit()

    
    angle = 0
    hitAngle = 0
    hit = False
    rot = 3
    controls = False
    creditos = False
    cam_pos = [0, 0, 5]  # x, y, z
    yaw = 0.0  # horizontal rotation
    pitch = 0.0  # optional for looking up/down
    camera_speed = 0.6
    mouse_sensitivity = 0.2
    camera_x, camera_y, camera_z = 0, 5, -20
    camera_rot_y, camera_rot_x = 180, 0
    state = 0
    MOVE_SPEED = 2

    red = 0.9
    green = 0.2
    blue = 0.7

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sonidoOff()
                    running=False
                if event.key == pygame.K_F1:
                    controls = not controls
                if event.key == pygame.K_F2:
                    creditos = not creditos
                if event.key == pygame.K_p:
                    sonidoOn("sonidos/DependentWeakling.mp3")
                if event.key == pygame.K_o:
                    sonidoOff()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Left click")
                elif event.button == 2:
                    print("Middle click")
                elif event.button == 3:
                    print("Right click")


        # Update position
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            camera_z -= camera_speed
        if keys[pygame.K_w]:
            camera_z += camera_speed
        if keys[pygame.K_a]:
            camera_x -= camera_speed
        if keys[pygame.K_d]:
            camera_x += camera_speed
        if keys[pygame.K_SPACE]:
            camera_y += camera_speed
        if keys[pygame.K_c]:
            camera_y -= camera_speed

        m_x, m_y = pygame.mouse.get_rel()
        camera_rot_y += m_x * mouse_sensitivity
        camera_rot_x += m_y * mouse_sensitivity

        if keys[pygame.K_0]:
            state = 0
        if keys[pygame.K_1]:
            state = 1
            sonidoOn("sonidos/a2shutup.mp3")
        if keys[pygame.K_2]:
            state = 2
            sonidoOn("sonidos/kainedumbass.mp3")
        if keys[pygame.K_3]:
            state = 3
            sonidoOn("sonidos/kaine-there-you-are.mp3")
        if keys[pygame.K_4]:
            state = 4
            sonidoOn("sonidos/kaine-youre-an-ass.mp3")
        if keys[pygame.K_5]:
            state = 5
            sonidoOn("sonidos/bingo.mp3")
        if keys[pygame.K_6]:
            state = 6
            sonidoOn("sonidos/a2useless.mp3")
        if keys[pygame.K_7]:
            state = 7
            sonidoOn("sonidos/diabolical.mp3")
        
        if keys[K_LEFT]:
            maid_x -= MOVE_SPEED
        if keys[K_RIGHT]:
            maid_x += MOVE_SPEED
        if keys[K_DOWN]:
            maid_z -= MOVE_SPEED
        if keys[K_UP]:
            maid_z += MOVE_SPEED
        maid_x = max(min_x, min(max_x, maid_x))
        maid_z = max(min_y, min(max_y, maid_z))

        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(-camera_x, -camera_y, -camera_z)
        glRotatef(camera_rot_x, 1, 0, 0)  # pitch (look up/down)
        glRotatef(camera_rot_y, 0, 1, 0)  # yaw (look left/right)
        


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

        if state == 0:#Expresion movimiento sonido escenario
            drawEscenario("images/copiedCity.jpg")
            drawCielo("images/whiteSky.jpg")
            drawPiso("images/whiteFloor.jpg")

            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.vestido1,translation_vector),chucho.carasVestido1,0,0,0,0,0,1.0,0,0.5)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLArm,translation_vector),chucho.carasLArm,0,0,0,0,1,1.0,0,0.5)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRArm,translation_vector),chucho.carasRArm,0,1,0,0,1,1.0,0,0.5)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRLeg,translation_vector),chucho.carasRLeg,0,1,1,0,0,1.0,0,0.5)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLLeg,translation_vector),chucho.carasLLeg,0,0,1,0,0,1.0,0,0.5)
            objects.draw_line(chucho.translate_matrix(chucho.sonrisa,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo1a,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo2a,translation_vector),x,y)
            objects.pintar_esfera(maid_x, maid_y+14.5,maid_z,1.5,0,0,0,0)

            cube_x += vel_x
            cube_y += vel_y
            if cube_x < min_x or cube_x > max_x:
                vel_x *= -1
            if cube_y < min_y or cube_y > max_y:
                vel_y *= -1
            draw_movable_cube()

            if abs(maid_x-cube_x) < 9 and abs(maid_z-cube_y) < 9:
                sonidoOn("sonidos/dbd_check_start.mp3")
            
            if (abs(maid_x-min_x) < 5 or abs(maid_z-min_y) < 5 or abs(maid_x-max_x) < 5 or abs(maid_z-max_y) < 5) and not(hit):
                sonidoOn("sonidos/dbd-generator-explosion.wav")
                hit = True
            elif abs(maid_x-min_x) > 5 and abs(maid_z-min_y) > 5 and abs(maid_x-max_x) > 5 and abs(maid_z-max_y) > 5:
                hit = False
            
            text_tex_id, tex_w, tex_h = create_text_texture("Si tocas las paredes o los cubos se activa un sonido", font)
            draw_textured_quad_3d(text_tex_id, pos=(20, 35, -45), size=(60, 4), rotation=180)
            # text_tex_id, tex_w, tex_h = create_text_texture("B", font)
            # draw_textured_quad_3d(text_tex_id, pos=(0, 20, -20), size=(2, 2), rotation=0)
            # text_tex_id, tex_w, tex_h = create_text_texture("C", font)
            # draw_textured_quad_3d(text_tex_id, pos=(-20, 20, -20), size=(2, 2), rotation=0)
        
        if state == 1:#correr
            drawEscenario("images/cityRuins.jpg")
            drawCielo("images/whiteSky.jpg")
            drawPiso("images/phpiso.jpg")

            centerLeg = [1.5+maid_x, 7+maid_y, -0.75+maid_z]
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.vestido1,translation_vector),chucho.carasVestido1,0,0,0,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLArm,translation_vector),chucho.carasLArm,0,0,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRArm,translation_vector),chucho.carasRArm,0,1,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesRLeg,translation_vector),'x',angle,centerLeg),chucho.carasRLeg,0,1,1,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.rotate_matrix(chucho.translate_matrix(chucho.verticesLLeg,translation_vector),'x',angle*-1,centerLeg),chucho.carasLLeg,0,0,1,0,0,red,green,blue)
            objects.draw_line(chucho.translate_matrix(chucho.triste,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo1b,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo2b,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ceja1,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ceja2,translation_vector),x,y)
            objects.pintar_esfera(maid_x, maid_y+14.5,maid_z,1.5,0,0,0,0)

        if state == 2:#brazo L
            drawEscenario("images/NierBunker.jpg")
            drawCielo("images/yorhalogo.jpg")
            drawPiso("images/yorha.jpg")

            centerLeg = [1.5+maid_x, 7+maid_y, -0.75+maid_z]
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.vestido1,translation_vector),chucho.carasVestido1,0,0,0,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLArm,translation_vector),chucho.carasLArm,angle,0,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRArm,translation_vector),chucho.carasRArm,0,1,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRLeg,translation_vector),chucho.carasRLeg,0,1,1,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLLeg,translation_vector),chucho.carasLLeg,0,0,1,0,0,red,green,blue)
            objects.draw_line(chucho.translate_matrix(chucho.sorpresa,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo1a,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo2a,translation_vector),x,y)
            objects.pintar_esfera(maid_x, maid_y+14.5,maid_z,1.5,0,0,0,0)

        if state == 3:#Brazo R
            drawEscenario("images/tfd.jpg")
            drawCielo("images/whiteSky.jpg")
            drawPiso("images/pisopiedra.jpg")

            centerLeg = [1.5+maid_x, 7+maid_y, -0.75+maid_z]
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.vestido1,translation_vector),chucho.carasVestido1,0,0,0,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLArm,translation_vector),chucho.carasLArm,0,0,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRArm,translation_vector),chucho.carasRArm,angle,1,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRLeg,translation_vector),chucho.carasRLeg,0,1,1,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLLeg,translation_vector),chucho.carasLLeg,0,0,1,0,0,red,green,blue)
            objects.draw_line(chucho.translate_matrix(chucho.triste,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo1b,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo2b,translation_vector),x,y)
            objects.pintar_esfera(maid_x, maid_y+14.5,maid_z,1.5,0,0,0,0)

        if state == 4:#Pierna L
            drawEscenario("images/NierLibreria.jpg")
            drawCielo("images/pisomadera.jpg")
            drawPiso("images/pisomadera.jpg")

            centerLeg = [1.5+maid_x, 7+maid_y, -0.75+maid_z]
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.vestido1,translation_vector),chucho.carasVestido1,0,0,0,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLArm,translation_vector),chucho.carasLArm,0,0,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRArm,translation_vector),chucho.carasRArm,0,1,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRLeg,translation_vector),chucho.carasRLeg,0,1,1,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLLeg,translation_vector),chucho.carasLLeg,angle,0,1,0,0,red,green,blue)
            objects.draw_line(chucho.translate_matrix(chucho.uwu,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo1b,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo2a,translation_vector),x,y)
            objects.pintar_esfera(maid_x, maid_y+14.5,maid_z,1.5,0,0,0,0)

        if state == 5:#Pierna R
            drawEscenario("images/terraria.jpg")
            drawCielo("images/blueSky.jpg")
            drawPiso("images/pisopiedra.jpg")

            centerLeg = [1.5+maid_x, 7+maid_y, -0.75+maid_z]
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.vestido1,translation_vector),chucho.carasVestido1,0,0,0,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLArm,translation_vector),chucho.carasLArm,0,0,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRArm,translation_vector),chucho.carasRArm,0,1,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRLeg,translation_vector),chucho.carasRLeg,angle,1,1,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLLeg,translation_vector),chucho.carasLLeg,0,0,1,0,0,red,green,blue)
            objects.draw_line(chucho.translate_matrix(chucho.mm,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo1a,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo2a,translation_vector),x,y)
            objects.pintar_esfera(maid_x, maid_y+14.5,maid_z,1.5,0,0,0,0)

        if state == 6:#correr
            drawEscenario("images/86sce.jpg")
            drawCielo("images/blueSky.jpg")
            drawPiso("images/trainT.jpg")

            centerLeg = [1.5+maid_x, 7+maid_y, -0.75+maid_z]
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.vestido1,translation_vector),chucho.carasVestido1,0,0,0,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLArm,translation_vector),chucho.carasLArm,angle,0,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRArm,translation_vector),chucho.carasRArm,angle,1,0,0,1,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRLeg,translation_vector),chucho.carasRLeg,angle,1,1,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLLeg,translation_vector),chucho.carasLLeg,angle,0,1,0,0,red,green,blue)
            objects.draw_line(chucho.translate_matrix(chucho.mm,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo1a,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo2b,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ceja1,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ceja2,translation_vector),x,y)
            objects.pintar_esfera(maid_x, maid_y+14.5,maid_z,1.5,0,0,0,0)

        if state == 7:#correrMas?
            drawEscenario("images/86sce2.jpg")
            drawCielo("images/blueSky.jpg")
            drawPiso("images/pisopiedra.jpg")

            centerLeg = [1.5+maid_x, 7+maid_y, -0.75+maid_z]
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.vestido1,translation_vector),chucho.carasVestido1,0,0,0,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLArm,translation_vector),chucho.carasLArm,angle,0,1,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRArm,translation_vector),chucho.carasRArm,angle,1,1,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesRLeg,translation_vector),chucho.carasRLeg,angle,1,1,0,0,red,green,blue)
            objects.pintar_cosa(x,y,chucho.translate_matrix(chucho.verticesLLeg,translation_vector),chucho.carasLLeg,angle,0,1,0,0,red,green,blue)
            objects.draw_line(chucho.translate_matrix(chucho.uwu,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo1b,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ojo2b,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ceja1,translation_vector),x,y)
            objects.draw_line(chucho.translate_matrix(chucho.ceja2,translation_vector),x,y)
            objects.pintar_esfera(maid_x, maid_y+14.5,maid_z,1.5,0,0,0,0)

        
        #draw_textured_floor(floor_texture)
        
        
        # text_tex_id, tex_w, tex_h = create_text_texture("A", font)
        # draw_textured_quad_3d(text_tex_id, pos=(20, 20, 20), size=(2, 2), rotation=180)
        # text_tex_id, tex_w, tex_h = create_text_texture("B", font)
        # draw_textured_quad_3d(text_tex_id, pos=(0, 20, 20), size=(2, 2), rotation=180)
        # text_tex_id, tex_w, tex_h = create_text_texture("C", font)
        # draw_textured_quad_3d(text_tex_id, pos=(-20, 20, 20), size=(2, 2), rotation=180)
        draw_text("Controles: 'F1'", 30, 30, font)
        if controls:
            draw_text("Numeros 1-6: Cambiar escenario, animacion, expresion, sonido", 30, 60, font)
            draw_text("Nomero 0: Original", 30, 90, font)
            draw_text("'P': Reproducir cancion", 30, 120, font)
            draw_text("'O': Detener cancion", 30, 150, font)
            draw_text("Flechas del teclado: Mover al personaje", 30, 180, font)
            draw_text("'W,A,S,D': Mover la camara", 30, 210, font)
            draw_text("Movimiento del raton: Rotar la camara", 30, 240, font)
            draw_text("'F2': Creditos", 30, 270, font)
            draw_text("'ESC': Salir", 30, 300, font)
        if creditos:
            draw_text("Creado por: Jesus Antonio Garcia Cruz", 200, 360, font)
            draw_text("22280706", 200, 390, font)
        pygame.display.flip()
        clock.tick(60)

    return "menu"