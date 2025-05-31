from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import math

#personaje

def pintar_cabeza(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)    
    setColor(r,g,b)
    draw_cube(2,-2,-1.5,1.5,3.5,7.5)
    glPopMatrix()

def pintar_frente(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    setColor(r,g,b)
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

def pintar_torso(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    setColor(r,g,b)
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

def pintar_extremidad(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    setColor(r,g,b)
    draw_cylinder(0.5,1.5,50)
    glPopMatrix()

def pintar_esfera(posx,posy,posz,r,g,b):
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    glTranslate(posx,posy,posz)
    setColor(r,g,b)
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