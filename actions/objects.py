from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
from pygame.locals import *
import pygame
from actions import luces as lc

def resetear_opengl():
        # Limpia estados OpenGL para no afectar otros módulos
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_DEPTH_TEST)
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Cierra ventana y libera pygame y OpenGL
        pygame.display.quit()
        pygame.quit()

def pintar_cosa(x,y,vertices,faces,angle,s,rx,ry,rz,red,green,blue):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glPushMatrix()
    if angle!=0:
        if s==1:
            angle=angle*-1
        glTranslate(vertices[0][0],vertices[0][1],vertices[0][2])
        glRotatef(angle, rx, ry, rz)
        glTranslatef(-vertices[0][0],-vertices[0][1],-vertices[0][2])
    lc.iluminacion(1,1,1)
    #cl.set_naranja()
    glColor3f(red, green, blue)
    draw_custom_object(vertices,faces)
    glPopMatrix()

def pintar_esfera(x,y,z,r,angle,rx,ry,rz):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glPushMatrix()
    glTranslatef(x, y, z)
    if angle!=0:
        glTranslate(0,0,0)
        glRotatef(angle, rx, ry, rz)
        glTranslatef(x, y, z)
    lc.iluminacion(1,1,1)
    #cl.set_naranja()
    glColor3f(1.0, 0.5, 0.0)
    draw_sphere(r,40,40)
    glPopMatrix()

def draw_custom_object(vertices,faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        num_vertices = len(face)
        if num_vertices == 3:
            # Si es un triangulo se dibujoa directamente
            for vertex in face:
                glVertex3fv(vertices[vertex])
        elif num_vertices == 4:
            # Si es un cuadrado se divide en 2 triangulos
            glVertex3fv(vertices[face[0]])
            glVertex3fv(vertices[face[1]])
            glVertex3fv(vertices[face[2]])

            glVertex3fv(vertices[face[0]])
            glVertex3fv(vertices[face[2]])
            glVertex3fv(vertices[face[3]])

        elif num_vertices > 4:
            # si tiene mas de 4 vertices se divide en varios triangulos
            for i in range(1, num_vertices - 1):
                glVertex3fv(vertices[face[0]])
                glVertex3fv(vertices[face[i]])
                glVertex3fv(vertices[face[i + 1]])

    glEnd()

    # dibujar las aristas
    glLineWidth(2.0)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    for face in faces:
        for i in range(len(face)):
            start_vertex = face[i]
            end_vertex = face[(i + 1) % len(face)]
            glVertex3fv(vertices[start_vertex])
            glVertex3fv(vertices[end_vertex])
    glEnd()


def draw_character_placeholder(index):
    colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    glColor3fv(colors[index])
    glutSolidCube(1.5)  # Or use your model drawing here

def draw_sphere(radius, slices, segments):
    for i in range(slices):
        lat0 = math.pi * (-0.5 + float(i) / slices)
        lat1 = math.pi * (-0.5 + float(i + 1) / slices)
        z0 = radius * math.sin(lat0)
        zr0 = radius * math.cos(lat0)
        z1 = radius * math.sin(lat1)
        zr1 = radius * math.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(segments + 1):
            lng = 2 * math.pi * float(j) / segments
            x = math.cos(lng)
            y = math.sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0, y * zr0, z0)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()


def draw_cylinder(radius, height, segments):
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        theta = i * (2 * math.pi / segments)
        x = height / 2  
        y = radius * math.cos(theta)  
        z = radius * math.sin(theta)  
        glVertex3f(x, y, z)  
        glVertex3f(-x, y, z)  
    glEnd()


def draw_cylinderM(radius, height, segments):
    glBegin(GL_QUAD_STRIP)
    for i in range(segments+1):
        theta = i*(2*math.pi/segments)
        x = radius*math.cos(theta)
        y = radius*math.sin(theta)
        glVertex3f(x, height/2, y)
        glVertex3f(x, -height/2, y)
    glEnd()

def draw_line(vertices,x,y,color=(0.0,0.0,0.0,1.0),thickness=3.0):
    glPushMatrix()
    glColor4f(*color)  # Set line color (RGBA)
    glLineWidth(thickness)
    glBegin(GL_LINE_STRIP)  # Connect consecutive points
    for vertex in vertices:
        glVertex3fv(vertex)  # Use the 3D vertex
    glEnd()
    glPopMatrix()



