from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import math
from pygame.locals import *
from PIL import Image

#personaje

def pintar_cabeza(posx,posy,posz,r,g,b,ilu=True):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)    
    if ilu:setColor(r,g,b)
    else: setColor2(r,g,b)
    draw_cube(2,-2,-1.5,1.5,3.5,7.5)
    glPopMatrix()

def pintar_frente(posx,posy,posz,r,g,b,ilu=True):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    if ilu:setColor(r,g,b)
    else: setColor2(r,g,b)
    draw_cube(2,-2,-1.5,1.5,7.5,10.5)
    glPopMatrix()

def pintar_marca_frente(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    setColor(r,g,b)
    draw_line(0,0,0.5,0,1,7)
    draw_line(0.25,0.25,0.25,-0.25,1,4)
    glPopMatrix()

def pintar_torso(posx,posy,posz,r,g,b,ilu=True):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    if ilu:setColor(r,g,b)
    else: setColor2(r,g,b)
    draw_cube(-1.5,1.5,-0.5,0.5,1,3.5)
    glPopMatrix()

def pintar_marca_torso(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    setColor(r,g,b)
    draw_line(0,0,-0.2,-0.4,1,7)
    draw_line(-0.2,-0.4,0.1,-0.4,1,4)
    draw_line(0.1,-0.4,-0.3,-0.8,1,7)
    glPopMatrix()

def pintar_extremidad(posx,posy,posz,r,g,b,ilu=True):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    if ilu:setColor(r,g,b)
    else: setColor2(r,g,b)
    draw_cylinder(0.5,1.5,50)
    glPopMatrix()

def pintar_esfera(posx,posy,posz,r,g,b,ilu=True):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    if ilu:setColor(r,g,b)
    else: setColor2(r,g,b)
    draw_sphere(0.5,50,50)
    glPopMatrix()

#extremidad a 45 grados
def pintar_extremidad_der_arriba(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    setColor(r,g,b)
    draw_cylinder2(0.5,2,50,(posx,posy,posz), (1,-0.5,0))
    glPopMatrix()

#exremidad a 135 grados
def pintar_extremidad_izq_arriba(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    setColor(r,g,b)
    draw_cylinder2(0.5,2,50,(posx,posy,posz), (1,0.5,0))
    glPopMatrix()

marca_frente_v = [
    [0, 16, 1.5],
    [0, 16.5, 1.5]
]
marca_frente_h = [
    [-0.25, 16.25, 1.5],
    [0.25, 16.25, 1.5]
]
marca_torso = [
    [0, 0, 1.5],
    [-0.2,-0.4, 1.5],
    [0.1,-0.4, 1.5],
    [-0.3,-0.8, 1.5],
]



# funciones

def setColor(r,g,b):
    glColor3f(r,g,b)
def setColor2(r,g,b):
    glColor3f(r/5,g/5,b/5)

def draw_cube(x_min, x_max, y_min, y_max, z_min, z_max):
    # Definir los 8 vértices del cubo
    A = (x_min, y_min, z_min)
    B = (x_max, y_min, z_min)
    C = (x_max, y_max, z_min)
    D = (x_min, y_max, z_min)
    E = (x_min, y_min, z_max)
    F = (x_max, y_min, z_max)
    G = (x_max, y_max, z_max)
    H = (x_min, y_max, z_max)
    
    # Definir las caras con un orden consistente (contrario a las agujas del reloj visto desde el exterior)
    faces = [
        # Cara frontal (cara en z_max)
        [E, F, G, H],
        # Cara trasera (cara en z_min)
        [D, C, B, A],
        # Cara derecha (x_max)
        [B, C, G, F],
        # Cara izquierda (x_min)
        [A, D, H, E],
        # Cara superior (y_max)
        [D, H, G, C],
        # Cara inferior (y_min)
        [A, B, F, E]
    ]
    
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            # Se intercambian y y z: (x, y, z) => (x, z, y)
            glVertex3f(vertex[0], vertex[2], vertex[1])
    glEnd()

def draw_line(x1, y1, x2, y2, segments, thickness=1.0):
    glLineWidth(thickness)
    glBegin(GL_LINE_STRIP)
    for i in range(segments + 1):
        t = i / segments
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        glVertex2f(x, y)
    glEnd()

def draw_cylinder(radius, height, segments):
    glBegin(GL_QUAD_STRIP)
    for i in range(segments+1):
        theta = i*(2*math.pi/segments)
        x = radius*math.cos(theta)
        y = radius*math.sin(theta)
        glVertex3f(x, height/2, y)
        glVertex3f(x, -height/2, y)
    glEnd()

def draw_sphere(radius, slices, segments):
    for i in range(slices+1):
        lat0 = math.pi*(-0.5*(i-1)/slices)
        lat1 = math.pi*(-0.5*i/slices)
        z0 = radius*math.sin(lat0)
        zr0 = radius*math.cos(lat0)
        z1 = radius*math.sin(lat1)
        zr1 = radius*math.cos(lat1)
        glBegin(GL_QUAD_STRIP)
        for j in range(segments+1):
            lng = 2*math.pi*j/segments
            x = zr0*math.cos(lng)
            y = zr0*math.sin(lng)
            glNormal3f(x,y,z0)
            glVertex3f(x,y,z0)
            x = zr1*math.cos(lng)
            y = zr1*math.sin(lng)
            glNormal3f(x,y,z1)
            glVertex3f(x,y,z1)
        glEnd()

def pintar_ojo_normal(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    setColor(r,g,b)
    draw_line(0,0,0.5,0,1,7)
    draw_line(0.25,0.25,0.25,-0.25,1,7)
    glPopMatrix()

def pintar_boca_normal(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    setColor(r,g,b)
    draw_line(0,0,0.5,0,1,7)
    glPopMatrix()

def text(texto,posx,posy,posz,sizefont,r,g,b,rb,gb,bb):
    font = pygame.font.Font(None, sizefont)
    text_surface = font.render(texto, True, (r,g,b), (rb,gb,bb))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos3d(posx,posy,posz)
    glDrawPixels(
                text_surface.get_width(),
                text_surface.get_height(),
                GL_RGBA, GL_UNSIGNED_BYTE,
                text_data)

def draw_cylinder2(radius, height, segments, start=(0.0, 0.0, 0.0), direction=(0.0, 1.0, 0.0)):
    # Normaliza el vector de dirección
    dx, dy, dz = direction
    mag = math.sqrt(dx*dx + dy*dy + dz*dz)
    ndir = (dx/mag, dy/mag, dz/mag)
    
    # Guarda la matriz actual y traslada al punto de inicio
    glPushMatrix()
    glTranslatef(start[0], start[1], start[2])
    
    # Rota el cilindro si la dirección no es la vertical (0,1,0)
    # Se calcula el ángulo entre (0,1,0) y la dirección normalizada y el eje de rotación
    dot = ndir[1]  # producto escalar con (0,1,0) es simplemente el componente Y
    angle = math.degrees(math.acos(dot))
    
    # Calcula el eje de rotación usando el producto vectorial:
    # (0,1,0) x (nx, ny, nz) = (nz, 0, -nx)
    rx = ndir[2]
    ry = 0.0
    rz = -ndir[0]
    if math.sqrt(rx*rx + ry*ry + rz*rz) > 0.0001 and abs(angle) > 0.0001:
        glRotatef(angle, rx, ry, rz)
    
    # Dibuja el cilindro a lo largo del eje Y
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        theta = i * (2 * math.pi / segments)
        x = radius * math.cos(theta)
        z = radius * math.sin(theta)
        glVertex3f(x, height / 2, z)
        glVertex3f(x, -height / 2, z)
    glEnd()
    
    glPopMatrix()

# sonido

pygame.init()
pygame.mixer.init()

def sonidoOn(fileName):
    audio_file = fileName
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

def sonidoOff():
    pygame.mixer.music.stop()
    
# escenario

pygame.init()
pygame.mixer.init()

def load_texture(fileName):
    im = Image.open(fileName)
    ix, iy, image = im.size[0], im.size[1], im.tobytes("raw","RGBX",0,-1)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,ix,iy,0,GL_RGBA,GL_UNSIGNED_BYTE,image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT) 
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT) 
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) 
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) 
    return texture_id

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

#objeto

def draw_sphere(radius, slices, segments):
    for i in range(slices+1):
        lat0 = math.pi*(-0.5*(i-1)/slices)
        lat1 = math.pi*(-0.5*i/slices)
        z0 = radius*math.sin(lat0)
        zr0 = radius*math.cos(lat0)
        z1 = radius*math.sin(lat1)
        zr1 = radius*math.cos(lat1)
        glBegin(GL_QUAD_STRIP)
        for j in range(segments+1):
            lng = 2*math.pi*j/segments
            x = zr0*math.cos(lng)
            y = zr0*math.sin(lng)
            glNormal3f(x,y,z0)
            glVertex3f(x,y,z0)
            x = zr1*math.cos(lng)
            y = zr1*math.sin(lng)
            glNormal3f(x,y,z1)
            glVertex3f(x,y,z1)
        glEnd()

def draw_cone(radius, height, segments):
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0,0,height)
    for i in range(segments+1):
        theta = 2*math.pi*i/segments
        x = radius*math.cos(theta)
        y = radius*math.sin(theta)
        glVertex3f(x,y,0)
    glEnd()
    
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0,0,height)
    for i in range(segments+1):
        theta = 2*math.pi*i/segments
        x = radius*math.cos(theta)
        y = radius*math.sin(theta)
        glVertex3f(x,y,0)
    glEnd()
    
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0,0,height)
    for i in range(segments+1):
        theta = 2*math.pi*i/segments
        x = radius*math.cos(theta)
        y = radius*math.sin(theta)
        glVertex3f(x,y,0)
    glEnd()

def draw_arch(radius, start, end, segments):
    glBegin(GL_LINE_STRIP)
    for i in range(segments+1):
        angle = start+(end-start)*(i/segments)
        x = radius*math.cos(angle)
        y = radius*math.sin(angle)
        glVertex2f(x,y)
    glEnd()

def draw_line(x1, y1, x2, y2, segments, thickness=1.0):
    glLineWidth(thickness)
    glBegin(GL_LINE_STRIP)
    for i in range(segments + 1):
        t = i / segments
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        glVertex2f(x, y)
    glEnd()


def draw_cylinder(radius, height, segments):
    glBegin(GL_QUAD_STRIP)
    for i in range(segments+1):
        theta = i*(2*math.pi/segments)
        x = radius*math.cos(theta)
        y = radius*math.sin(theta)
        glVertex3f(x, height/2, y)
        glVertex3f(x, -height/2, y)
    glEnd()

def draw_cylinder2(radius, height, segments, start=(0.0, 0.0, 0.0), direction=(0.0, 1.0, 0.0)):
    # Normaliza el vector de dirección
    dx, dy, dz = direction
    mag = math.sqrt(dx*dx + dy*dy + dz*dz)
    ndir = (dx/mag, dy/mag, dz/mag)
    
    # Guarda la matriz actual y traslada al punto de inicio
    glPushMatrix()
    glTranslatef(start[0], start[1], start[2])
    
    # Rota el cilindro si la dirección no es la vertical (0,1,0)
    # Se calcula el ángulo entre (0,1,0) y la dirección normalizada y el eje de rotación
    dot = ndir[1]  # producto escalar con (0,1,0) es simplemente el componente Y
    angle = math.degrees(math.acos(dot))
    
    # Calcula el eje de rotación usando el producto vectorial:
    # (0,1,0) x (nx, ny, nz) = (nz, 0, -nx)
    rx = ndir[2]
    ry = 0.0
    rz = -ndir[0]
    if math.sqrt(rx*rx + ry*ry + rz*rz) > 0.0001 and abs(angle) > 0.0001:
        glRotatef(angle, rx, ry, rz)
    
    # Dibuja el cilindro a lo largo del eje Y
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        theta = i * (2 * math.pi / segments)
        x = radius * math.cos(theta)
        z = radius * math.sin(theta)
        glVertex3f(x, height / 2, z)
        glVertex3f(x, -height / 2, z)
    glEnd()
    
    glPopMatrix()

def draw_cube(x_min, x_max, y_min, y_max, z_min, z_max):
    # Definir los 8 vértices del cubo
    A = (x_min, y_min, z_min)
    B = (x_max, y_min, z_min)
    C = (x_max, y_max, z_min)
    D = (x_min, y_max, z_min)
    E = (x_min, y_min, z_max)
    F = (x_max, y_min, z_max)
    G = (x_max, y_max, z_max)
    H = (x_min, y_max, z_max)
    
    # Definir las caras con un orden consistente (contrario a las agujas del reloj visto desde el exterior)
    faces = [
        # Cara frontal (cara en z_max)
        [E, F, G, H],
        # Cara trasera (cara en z_min)
        [D, C, B, A],
        # Cara derecha (x_max)
        [B, C, G, F],
        # Cara izquierda (x_min)
        [A, D, H, E],
        # Cara superior (y_max)
        [D, H, G, C],
        # Cara inferior (y_min)
        [A, B, F, E]
    ]
    
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            # Se intercambian y y z: (x, y, z) => (x, z, y)
            glVertex3f(vertex[0], vertex[2], vertex[1])
    glEnd()

def draw_cube2(pos, size=1.0):
    x, y, z = pos
    hs = size / 2.0  # mitad del tamaño
    # Definir los 8 vértices del cubo
    vertices = [
        (x - hs, y - hs, z - hs),
        (x + hs, y - hs, z - hs),
        (x + hs, y + hs, z - hs),
        (x - hs, y + hs, z - hs),
        (x - hs, y - hs, z + hs),
        (x + hs, y - hs, z + hs),
        (x + hs, y + hs, z + hs),
        (x - hs, y + hs, z + hs)
    ]
    # Definir las caras (cada cara es un conjunto de 4 vértices)
    caras = [
        (0, 1, 2, 3),  # cara trasera
        (4, 5, 6, 7),  # cara delantera
        (0, 1, 5, 4),  # cara inferior
        (2, 3, 7, 6),  # cara superior
        (1, 2, 6, 5),  # cara derecha
        (0, 3, 7, 4)   # cara izquierda
    ]
    glColor3f(0.0, 1.0, 0.0)  # color verde para el cubo
    glBegin(GL_QUADS)
    for cara in caras:
        for vert in cara:
            glVertex3fv(vertices[vert])
    glEnd()
