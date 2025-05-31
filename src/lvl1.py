import pygame
from pygame import sprite
import sys
import random

# --- Colores ---
gris = (127, 127, 127)
negro = (0, 0, 0)
blanco = (255, 255, 255)
azul = (0, 0, 255)
rojo = (255, 0, 0)

# --- Mensajes de Evolución ---
MENSAJES_EVOLUCION = [
    "SABÍAS QUE... La primera forma de vida en la Tierra fue procariota, como bacterias y arqueas.",
    "SABÍAS QUE... Los estromatolitos son las estructuras biológicas más antiguas conocidas, formadas por cianobacterias.",
    "SABÍAS QUE... La Gran Oxidación fue un evento donde el oxígeno se acumuló en la atmósfera, cambiando drásticamente la vida.",
    "SABÍAS QUE... La explosión Cámbrica fue un período de rápida diversificación de la vida hace unos 540 millones de años.",
    "SABÍAS QUE... Los primeros animales terrestres evolucionaron de peces hace unos 375 millones de años.",
    "SABÍAS QUE... La aparición de la fotosíntesis cambió la composición de la atmósfera terrestre para siempre.",
    "SABÍAS QUE... Las plantas colonizaron la tierra firme antes que los animales, creando nuevos hábitats.",
    "SABÍAS QUE... Los dinosaurios dominaron la Tierra durante más de 160 millones de años.",
    "SABÍAS QUE... La extinción del Cretácico-Paleógeno, hace 66 millones de años, acabó con los dinosaurios no aviares.",
    "SABÍAS QUE... Los mamíferos se diversificaron rápidamente después de la extinción de los dinosaurios.",
    "SABÍAS QUE... Los primeros homínidos aparecieron en África hace unos 6 millones de años.",
    "SABÍAS QUE... Homo sapiens, nuestra especie, surgió hace aproximadamente 300,000 años.",
    "SABÍAS QUE... La domesticación del fuego fue un paso crucial en la evolución humana.",
    "SABÍAS QUE... La invención de la agricultura llevó a la formación de asentamientos permanentes y civilizaciones.",
    "SABÍAS QUE... La teoría de la evolución por selección natural fue propuesta por Charles Darwin.",
    "SABÍAS QUE... El ADN es la molécula que contiene las instrucciones genéticas para el desarrollo y funcionamiento de los seres vivos.",
    "SABÍAS QUE... Las mutaciones genéticas son la fuente principal de la variación sobre la cual actúa la selección natural.",
    "SABÍAS QUE... La coevolución ocurre cuando dos o más especies influyen mutuamente en su evolución.",
    "SABÍAS QUE... La deriva genética es un cambio aleatorio en la frecuencia de alelos en una población."
]

# --- Clases de Sprites ---
class pared(pygame.sprite.Sprite):
    def __init__(self, x, y, largo, alto, color=negro):
        super().__init__()
        self.image = pygame.Surface((largo, alto))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class protagonista(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carga todas las imágenes: normal, golpeado y evolucionado
        self.image_normal = pygame.image.load("images/agrio.png").convert_alpha()
        self.image_normal = pygame.transform.scale(self.image_normal, (60, 60))
        
        try:
            self.image_hit = pygame.image.load("images/agrio2.png").convert_alpha()
            self.image_hit = pygame.transform.scale(self.image_hit, (60, 60))
        except pygame.error:
            print("Advertencia: 'images/agrio2.png' no encontrada. Usando imagen normal para golpeado.")
            self.image_hit = self.image_normal

        try:
            self.image_evolve = pygame.image.load("images/agrio3.png").convert_alpha()
            self.image_evolve = pygame.transform.scale(self.image_evolve, (60, 60))
        except pygame.error:
            print("Advertencia: 'images/agrio3.png' no encontrada. Usando imagen normal para evolucionado.")
            self.image_evolve = self.image_normal

        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.cambio_x = 0
        self.cambio_y = 0
        self.velocidad = 5

        self.hit_timer = 0    
        self.evolve_timer = 0 

        self.golpeado_por_enemigo = False
        self.tiempo_ultimo_golpe = 0
        self.tiempo_invulnerabilidad = 1500

    def cambioVelocidad(self, x, y):
        self.cambio_x = x
        self.cambio_y = y

    def mover(self, paredes):
        self.rect.x += self.cambio_x
        for bloque in pygame.sprite.spritecollide(self, paredes, False):
            if self.cambio_x > 0:
                self.rect.right = bloque.rect.left
            else:
                self.rect.left = bloque.rect.right

        self.rect.y += self.cambio_y
        for bloque in pygame.sprite.spritecollide(self, paredes, False):
            if self.cambio_y > 0:
                self.rect.bottom = bloque.rect.top
            else:
                self.rect.top = bloque.rect.bottom
    
    def got_hit(self):
        self.image = self.image_hit
        self.hit_timer = 30 # Duración en frames para la imagen de golpeado

    def evolved(self):
        self.image = self.image_evolve
        self.evolve_timer = 30 # Duración en frames para la imagen de evolucionado

    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        # Manejar el timer de "golpeado"
        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer == 0:
                # Si ya no está golpeado, y no está evolucionado, vuelve a la imagen normal
                if self.evolve_timer == 0:
                    self.image = self.image_normal
                else: # Si estaba golpeado y evolucionado, vuelve a la imagen evolucionada
                    self.image = self.image_evolve
        # Manejar el timer de "evolucionado" (solo si no está actualmente en el estado "golpeado")
        elif self.evolve_timer > 0:
            self.evolve_timer -= 1
            if self.evolve_timer == 0:
                self.image = self.image_normal

        # Manejar la invulnerabilidad después de ser golpeado
        if self.golpeado_por_enemigo:
            if tiempo_actual - self.tiempo_ultimo_golpe > self.tiempo_invulnerabilidad:
                self.golpeado_por_enemigo = False


class PuntoEvolucion(pygame.sprite.Sprite):
    def __init__(self, x, y, mensaje_index):
        super().__init__()
        self.image = pygame.image.load("images/mone.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mensaje_index = mensaje_index

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, dx=0, dy=0, limite_x=None, limite_y=None):
        super().__init__()
        self.image = pygame.image.load("images/enemigo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dx = dx
        self.dy = dy
        self.limite_x = limite_x
        self.limite_y = limite_y

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.limite_x:
            if self.rect.left < self.limite_x[0] or self.rect.right > self.limite_x[1]:
                self.dx *= -1

        if self.limite_y:
            if self.rect.top < self.limite_y[0] or self.rect.bottom > self.limite_y[1]:
                self.dy *= -1


class cuarto():
    def __init__(self):
        self.pared_lisa = pygame.sprite.Group()
        self.spri_enemigos = pygame.sprite.Group()
        self.puntos = pygame.sprite.Group()

class cuarto1(cuarto):
    def __init__(self):
        super().__init__()
        # Paredes externas
        paredes_externas = [[0, 0, 20, 250, negro], [0, 350, 20, 440, negro], [1480, 0, 20, 400, negro],
                            [1480, 550, 20, 300, negro], [20, 0, 1460, 20, negro], [20, 765, 1460, 20, negro]]
        for item in paredes_externas:
            self.pared_lisa.add(pared(*item))

        # Paredes internas
        self.pared_lisa.add(pared(80, 30, 10, 460, negro))
        self.pared_lisa.add(pared(80, 580, 10, 170, negro))
        self.pared_lisa.add(pared(80, 30, 1330, 10, negro))
        self.pared_lisa.add(pared(80, 750, 1330, 10, negro))
        self.pared_lisa.add(pared(1400, 450, 10, 300, negro))
        self.pared_lisa.add(pared(1400, 30, 10, 330, negro))
        self.pared_lisa.add(pared(80, 340, 220, 10, negro))
        self.pared_lisa.add(pared(80, 570, 220, 10, negro))
        self.pared_lisa.add(pared(300, 480, 10, 100, negro))
        self.pared_lisa.add(pared(300, 130, 10, 220, negro))
        self.pared_lisa.add(pared(300, 130, 200, 10, negro))
        self.pared_lisa.add(pared(310, 480, 200, 10, negro))
        self.pared_lisa.add(pared(310, 650, 200, 10, negro))
        self.pared_lisa.add(pared(500, 250, 10, 410, negro))
        self.pared_lisa.add(pared(500, 250, 210, 10, negro))
        self.pared_lisa.add(pared(700, 150, 10, 100, negro))
        self.pared_lisa.add(pared(860, 30, 10, 330, negro))
        self.pared_lisa.add(pared(860, 110, 200, 10, negro))
        self.pared_lisa.add(pared(660, 360, 400, 10, negro))
        self.pared_lisa.add(pared(660, 360, 10, 300, negro))
        self.pared_lisa.add(pared(660, 650, 200, 10, negro))
        self.pared_lisa.add(pared(860, 540, 10, 120, negro))
        self.pared_lisa.add(pared(860, 540, 370, 10, negro))
        self.pared_lisa.add(pared(860, 440, 550, 10, negro))
        self.pared_lisa.add(pared(1200, 110, 10, 330, negro))
        self.pared_lisa.add(pared(1220, 550, 10, 110, negro))
        self.pared_lisa.add(pared(1045, 650, 10, 110, negro))
        self.pared_lisa.add(pared(1045, 230, 160, 10, negro))

        # Enemigos con distintos patrones
        self.spri_enemigos.add(Enemigo(300, 300, dx=3, limite_x=(200, 700)))
        self.spri_enemigos.add(Enemigo(500, 100, dy=2, limite_y=(100, 500)))
        self.spri_enemigos.add(Enemigo(1000, 500, dx=2, dy=2, limite_x=(900, 1200), limite_y=(400, 650)))
        self.spri_enemigos.add(Enemigo(700, 300, dx=5, limite_x=(600, 1400)))
        
        # Puntos de evolución
        mensajes_disponibles_indices = list(range(len(MENSAJES_EVOLUCION)))
        random.shuffle(mensajes_disponibles_indices)

        self.puntos.add(PuntoEvolucion(150, 100, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(400, 200, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(1300, 150, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(200, 680, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(550, 500, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(800, 180, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(1100, 600, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(950, 300, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(1350, 700, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(150, 450, mensajes_disponibles_indices.pop(0)))


class cuarto2(cuarto):
    def __init__(self):
        super().__init__()
        
        paredes_externas = [[0, 0, 20, 270, negro], [0, 600, 20, 200, negro], [1480, 0, 20, 400, negro],
                            [1480, 550, 20, 300, negro], [20, 0, 1460, 20, negro], [20, 765, 1460, 20, negro]]
        for item in paredes_externas:
            self.pared_lisa.add(pared(*item))

        self.pared_lisa.add(pared(80, 30, 10, 460, negro))
        self.pared_lisa.add(pared(80, 580, 10, 170, negro))
        self.pared_lisa.add(pared(80, 30, 1330, 10, negro))
        self.pared_lisa.add(pared(80, 750, 1330, 10, negro))
        self.pared_lisa.add(pared(1400, 450, 10, 300, negro))
        self.pared_lisa.add(pared(1400, 30, 10, 330, negro))
        self.pared_lisa.add(pared(80, 340, 220, 10, negro))
        self.pared_lisa.add(pared(80, 570, 220, 10, negro))
        self.pared_lisa.add(pared(300, 480, 10, 100, negro))
        self.pared_lisa.add(pared(300, 130, 10, 220, negro))
        self.pared_lisa.add(pared(300, 130, 200, 10, negro))
        self.pared_lisa.add(pared(310, 480, 200, 10, negro))
        self.pared_lisa.add(pared(310, 650, 200, 10, negro))
        self.pared_lisa.add(pared(500, 250, 10, 410, negro))
        self.pared_lisa.add(pared(500, 250, 210, 10, negro))
        self.pared_lisa.add(pared(700, 150, 10, 100, negro))
        self.pared_lisa.add(pared(860, 30, 10, 330, negro))
        self.pared_lisa.add(pared(860, 110, 200, 10, negro))
        self.pared_lisa.add(pared(660, 360, 400, 10, negro))
        self.pared_lisa.add(pared(660, 360, 10, 300, negro))
        self.pared_lisa.add(pared(660, 650, 200, 10, negro))
        self.pared_lisa.add(pared(860, 540, 10, 120, negro))
        self.pared_lisa.add(pared(860, 540, 370, 10, negro))
        self.pared_lisa.add(pared(860, 440, 550, 10, negro))
        self.pared_lisa.add(pared(1200, 110, 10, 330, negro))
        self.pared_lisa.add(pared(1220, 550, 10, 110, negro))
        self.pared_lisa.add(pared(1045, 650, 10, 110, negro))
        self.pared_lisa.add(pared(1045, 230, 160, 10, negro))

        self.spri_enemigos.add(Enemigo(750, 680, dx=3, limite_x=(0, 1000)))
        self.spri_enemigos.add(Enemigo(400, 600, dy=4, limite_y=(10, 700)))
        self.spri_enemigos.add(Enemigo(1300, 100, dx=-3, limite_x=(1100, 1450)))
        self.spri_enemigos.add(Enemigo(650, 400, dx=2, dy=-2, limite_x=(80, 1450),limite_y=(400,550)))
        self.spri_enemigos.add(Enemigo(950, 200, dy=3, limite_y=(100, 350)))

        mensajes_disponibles_indices = list(range(len(MENSAJES_EVOLUCION)))
        random.shuffle(mensajes_disponibles_indices)
        
        self.puntos.add(PuntoEvolucion(350, 180, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(700, 80, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(1300, 400, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(150, 650, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(550, 300, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(800, 580, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(1150, 150, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(1250, 700, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(450, 450, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(1000, 400, mensajes_disponibles_indices.pop(0)))
        self.puntos.add(PuntoEvolucion(700, 480, mensajes_disponibles_indices.pop(0)))


def mostrar_texto(pantalla, texto, color=negro, fondo=azul, x=350, y=350, ancho_cuadro=700, alto_cuadro=200, delay=3000, centrar_texto=True, font_size=24):
    fuente = pygame.font.SysFont('arial', font_size)
    cuadro = pygame.Surface((ancho_cuadro, alto_cuadro))
    cuadro.fill(fondo)

    
    parrafos_o_secciones = texto.split('\n')
    lineas_finales = []

    for seccion_texto in parrafos_o_secciones:
        palabras = seccion_texto.split(' ')
        linea_actual = ""
        for palabra in palabras:
            test_linea = linea_actual + palabra + " "
            temp_render = fuente.render(test_linea, True, color)
            
            if temp_render.get_width() < (ancho_cuadro - 40): # Margen de 20 a cada lado
                linea_actual = test_linea
            else:
                lineas_finales.append(linea_actual.strip())
                linea_actual = palabra + " "
        lineas_finales.append(linea_actual.strip())
 
    
    total_texto_height = sum([fuente.render(linea, True, color).get_height() for linea in lineas_finales]) + (len(lineas_finales) - 1) * 5
    y_offset_start = (alto_cuadro - total_texto_height) // 2 if centrar_texto else 10

    current_y_offset = y_offset_start
    for linea in lineas_finales:
        texto_render = fuente.render(linea, True, color)
        if centrar_texto:
            texto_rect = texto_render.get_rect(center=(cuadro.get_width() // 2, current_y_offset + texto_render.get_height() // 2))
        else:
            texto_rect = texto_render.get_rect(topleft=(20, current_y_offset)) # 20 es un margen izquierdo
        cuadro.blit(texto_render, texto_rect)
        current_y_offset += texto_render.get_height() + 5

    pantalla.blit(cuadro, (x, y))
    pygame.display.flip()
    if delay > 0:
        pygame.time.delay(delay)

def mostrar_vidas(pantalla, vidas):
    fuente = pygame.font.SysFont('arial', 30, True)
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, blanco)
    pantalla.blit(texto_vidas, (10, 10))

def mostrar_puntuacion(pantalla, puntuacion):
    fuente = pygame.font.SysFont('arial', 30, True)
    texto_puntuacion = fuente.render(f"Puntos: {puntuacion}", True, blanco)
    pantalla.blit(texto_puntuacion, (10, 45))

def game_over_screen(pantalla, puntuacion, sound_manager):
    sound_manager.stop_music()
    sound_manager.play_game_over_sound()
    
    pantalla.fill(negro)
    fuente_titulo = pygame.font.SysFont('arial', 60, True)
    fuente_info = pygame.font.SysFont('arial', 30)

    titulo_render = fuente_titulo.render("GAME OVER", True, rojo)
    punt_render = fuente_info.render(f"Puntuación final: {puntuacion}", True, blanco)
    instrucciones_render = fuente_info.render("Presiona R para Reiniciar, M para ir al Menú", True, blanco) 

    pantalla.blit(titulo_render, titulo_render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 - 50)))
    pantalla.blit(punt_render, punt_render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 + 20)))
    pantalla.blit(instrucciones_render, instrucciones_render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 + 80)))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit" 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit" 
                if event.key == pygame.K_r:
                    return "restart" 
                if event.key == pygame.K_m: 
                    return "menu" 
        pygame.time.Clock().tick(30)

def victory_screen(pantalla, puntuacion, sound_manager):
    sound_manager.stop_music()
    sound_manager.play_victory_sound()
    
    pantalla.fill(azul)
    fuente_titulo = pygame.font.SysFont('arial', 60, True)
    fuente_info = pygame.font.SysFont('arial', 30)

    titulo_render = fuente_titulo.render("¡NIVEL COMPLETADO!", True, blanco)
    punt_render = fuente_info.render(f"Puntuación final: {puntuacion}", True, blanco)
    instrucciones_render = fuente_info.render("Presiona R para Reiniciar, M para ir al Menú", True, blanco) 

    pantalla.blit(titulo_render, titulo_render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 - 50)))
    pantalla.blit(punt_render, punt_render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 + 20)))
    pantalla.blit(instrucciones_render, instrucciones_render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 + 80)))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit" 
            if event.type == pygame.KEYDOWN: # Este chequeo debe estar dentro de KEYDOWN
                if event.key == pygame.K_ESCAPE:
                    return "quit" 
                if event.key == pygame.K_r:
                    return "restart" 
                if event.key == pygame.K_m: # CORREGIDO: Asegura que detecta K_m
                    return "menu" 
        pygame.time.Clock().tick(30)

def instructions_screen(pantalla):
    s = pygame.Surface((pantalla.get_width(), pantalla.get_height()), pygame.SRCALPHA)
    s.fill((0,0,0,180)) # Negro con 180 de opacidad (de 255)
    pantalla.blit(s, (0,0))

    texto_instrucciones = """INSTRUCCIONES
        Usa las teclas de flecha (ARRIBA, ABAJO, IZQUIERDA, DERECHA) para moverte.
        Recoge los puntos de evolución para aumentar tu puntuación.
        Evita a los enemigos. Si te atrapan 3 veces, ¡es GAME OVER!
        Atraviesa los laberintos para completar el nivel.
        Presiona S para salir del juego.
        Presiona I para cerrar las instrucciones.""" 
    

    ancho_cuadro = 500
    alto_cuadro = 400
    x_cuadro = (pantalla.get_width() - ancho_cuadro) // 2
    y_cuadro = (pantalla.get_height() - alto_cuadro) // 2

    mostrar_texto(pantalla, texto_instrucciones, color=blanco, fondo=gris,
                  x=x_cuadro, y=y_cuadro,
                  ancho_cuadro=ancho_cuadro, alto_cuadro=alto_cuadro,
                  delay=0, centrar_texto=True, font_size=20)

def countdown_screen(pantalla):
    fuente_contador = pygame.font.SysFont('arial', 150, True)
    fuente_instrucciones = pygame.font.SysFont('arial', 30, True)
    background_image = pygame.image.load("images/fono.png").convert()
    background_image = pygame.transform.scale(background_image, (1500, 800))

    inst_texto = "Presiona 'I' para ver las instrucciones en cualquier momento."

    for i in range(3, 0, -1):
        pantalla.blit(background_image, (0, 0))

        contador_render = fuente_contador.render(str(i), True, blanco)
        contador_rect = contador_render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 - 50))
        pantalla.blit(contador_render, contador_rect)

        inst_render = fuente_instrucciones.render(inst_texto, True, blanco)
        inst_rect = inst_render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 + 50))
        pantalla.blit(inst_render, inst_rect)

        pygame.display.flip()
        pygame.time.delay(1000)

    pantalla.blit(background_image, (0, 0))
    go_render = fuente_contador.render("¡GO!", True, azul)
    go_rect = go_render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 - 50))
    pantalla.blit(go_render, go_rect)

    inst_render = fuente_instrucciones.render(inst_texto, True, blanco)
    inst_rect = inst_render.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2 + 50))
    pantalla.blit(inst_render, inst_rect)

    pygame.display.flip()
    pygame.time.delay(1000)

def confirm_exit_screen(pantalla):
    s = pygame.Surface((pantalla.get_width(), pantalla.get_height()), pygame.SRCALPHA)
    s.fill((0,0,0,180)) 
    pantalla.blit(s, (0,0))

    fuente = pygame.font.SysFont('arial', 40, True)
    
    texto = "¿Quieres ir al Menú (M) o seguir jugando (N)?" 
    render = fuente.render(texto, True, blanco)
    
    
    text_width, text_height = render.get_size()
    box_width = text_width + 80 
    box_height = text_height + 80
    box_x = (pantalla.get_width() - box_width) // 2
    box_y = (pantalla.get_height() - box_height) // 2

   
    pygame.draw.rect(pantalla, gris, (box_x, box_y, box_width, box_height))

    
    text_rect = render.get_rect(center=(box_x + box_width // 2, box_y + box_height // 2))
    pantalla.blit(render, text_rect)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_s:
                #     return "quit" 
                if event.key == pygame.K_n:
                    return "continue"
                if event.key == pygame.K_m: 
                    return "menu" 
            if event.type == pygame.QUIT:
                return "quit" 
        pygame.time.Clock().tick(30)


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = self._load_sound("sonidos/cancion.wav")
        self.hit_sound = self._load_sound("sonidos/enemigos.wav")
        self.point_sound = self._load_sound("sonidos/coin.wav")
        self.game_over_sound = self._load_sound("sonidos/gameover.wav")
        self.victory_sound = self._load_sound("sonidos/nlTerminado.wav")
        
        if self.background_music:
            self.background_music.set_volume(0.3)
        if self.hit_sound:
            self.hit_sound.set_volume(0.7)
        if self.point_sound:
            self.point_sound.set_volume(0.8)
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

    def play_game_over_sound(self):
        if self.game_over_sound:
            self.game_over_sound.play()

    def play_victory_sound(self):
        if self.victory_sound:
            self.victory_sound.play()


def run():
    pygame.init()
    
    pantalla = pygame.display.set_mode([1500, 800])
    pygame.display.set_caption('LABERINTO')
    reloj = pygame.time.Clock()

    sound_manager = SoundManager()

    Protagonista = protagonista(50, 500)
    desplazarsprites = pygame.sprite.Group(Protagonista)

    cuartos = [cuarto1(), cuarto2()] 
    cuarto_actual_no = 0
    cuarto_actual = cuartos[cuarto_actual_no]

    puntuacion = 0
    vidas = 3
    mensajes_mostrados_indices = [] 
    hecho = False 
    game_over = False
    game_won = False
    show_instructions = False
    game_started = False
    transitioned_to_cuarto2 = False 

    while not hecho:
        if not game_started:
            countdown_screen(pantalla)
            game_started = True
            sound_manager.play_music() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound_manager.stop_music() 
                action_on_exit = confirm_exit_screen(pantalla)
                if action_on_exit == "quit":
                    return "quit" 
                elif action_on_exit == "menu":
                    return "menu" 
                else: 
                    sound_manager.play_music() 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i: 
                    show_instructions = not show_instructions 
                elif event.key == pygame.K_s:
                    sound_manager.stop_music()
                    action_on_exit = confirm_exit_screen(pantalla)
                    if action_on_exit == "quit":
                        return "quit" 
                    elif action_on_exit == "menu":
                        return "menu" 
                    else: 
                        sound_manager.play_music()
                elif not show_instructions and not game_over and not game_won and game_started:
                    if event.key == pygame.K_LEFT: Protagonista.cambioVelocidad(-Protagonista.velocidad, 0)
                    if event.key == pygame.K_RIGHT: Protagonista.cambioVelocidad(Protagonista.velocidad, 0)
                    if event.key == pygame.K_UP: Protagonista.cambioVelocidad(0, -Protagonista.velocidad)
                    if event.key == pygame.K_DOWN: Protagonista.cambioVelocidad(0, Protagonista.velocidad)
            if event.type == pygame.KEYUP:
                if not show_instructions and not game_over and not game_won and game_started:
                    if event.key == pygame.K_LEFT and Protagonista.cambio_x < 0: Protagonista.cambioVelocidad(0, Protagonista.cambio_y)
                    if event.key == pygame.K_RIGHT and Protagonista.cambio_x > 0: Protagonista.cambioVelocidad(0, Protagonista.cambio_y)
                    if event.key == pygame.K_UP and Protagonista.cambio_y < 0: Protagonista.cambioVelocidad(Protagonista.cambio_x, 0)
                    if event.key == pygame.K_DOWN and Protagonista.cambio_y > 0: Protagonista.cambioVelocidad(Protagonista.cambio_x, 0)

       
        if not game_over and not game_won and not show_instructions and game_started:
            Protagonista.update()
            Protagonista.mover(cuarto_actual.pared_lisa)

            for punto in pygame.sprite.spritecollide(Protagonista, cuarto_actual.puntos, True):
                sound_manager.play_point_sound() 
                mensaje_a_mostrar = MENSAJES_EVOLUCION[punto.mensaje_index]
                if punto.mensaje_index not in mensajes_mostrados_indices:
                    mostrar_texto(pantalla, mensaje_a_mostrar, color=blanco, fondo=azul,
                                  x=(pantalla.get_width() - 700) // 2, y=(pantalla.get_height() - 200) // 2)
                    mensajes_mostrados_indices.append(punto.mensaje_index)
                    puntuacion += 1
                    Protagonista.evolved() 

            cuarto_actual.spri_enemigos.update()
            
            if pygame.sprite.spritecollideany(Protagonista, cuarto_actual.spri_enemigos) and not Protagonista.golpeado_por_enemigo:
                vidas -= 1
                sound_manager.play_hit_sound() 
                
                Protagonista.got_hit() 
                Protagonista.golpeado_por_enemigo = True 
                Protagonista.tiempo_ultimo_golpe = pygame.time.get_ticks() 

                mostrar_texto(pantalla, f"¡Fuiste atrapado por un enemigo! Te quedan {vidas} vidas.",
                                         color=blanco, fondo=rojo,
                                         x=(pantalla.get_width() - 700) // 2, y=(pantalla.get_height() - 200) // 2)

                if vidas <= 0:
                    game_over = True 
                else:
                    Protagonista.rect.x = 50
                    Protagonista.rect.y = 500
                    Protagonista.cambioVelocidad(0,0) 

            if Protagonista.rect.x < -15: 
                if cuarto_actual_no == 0:
                    Protagonista.rect.x = -10 
                else:
                    cuarto_actual_no -= 1
                    cuarto_actual = cuartos[cuarto_actual_no]
                    Protagonista.rect.x = 1490 
                    transitioned_to_cuarto2 = False 

            if Protagonista.rect.x > 1500: 
                if cuarto_actual_no == len(cuartos) - 1:
                    game_won = True 
                else:
                    cuarto_actual_no += 1
                    cuarto_actual = cuartos[cuarto_actual_no]
                    Protagonista.rect.x = 0 
                    
                    if cuarto_actual_no == 1 and not transitioned_to_cuarto2:
                        mostrar_texto(pantalla, "¡ETAPA 2!", color=blanco, fondo=azul,
                                      x=(pantalla.get_width() - 700) // 2, y=(pantalla.get_height() - 200) // 2, delay=2000)
                        transitioned_to_cuarto2 = True 

        
        background_image = pygame.image.load("images/fono.png").convert()
        background_image = pygame.transform.scale(background_image, (1500, 800))
        pantalla.blit(background_image, (0, 0))

        if game_over:
            action = game_over_screen(pantalla, puntuacion, sound_manager)
            if action == "restart":
                return "restart" 
            elif action == "menu":
                return "menu" 
            elif action == "quit":
                return "quit" 
        elif game_won:
            action = victory_screen(pantalla, puntuacion, sound_manager)
            if action == "restart":
                return "restart" 
            elif action == "menu":
                return "menu" 
            elif action == "quit":
                return "quit" 
        else:
            cuarto_actual.pared_lisa.draw(pantalla)
            cuarto_actual.puntos.draw(pantalla)
            cuarto_actual.spri_enemigos.draw(pantalla)
            desplazarsprites.draw(pantalla)
            mostrar_vidas(pantalla, vidas)
            mostrar_puntuacion(pantalla, puntuacion)

            if show_instructions:
                instructions_screen(pantalla)

        pygame.display.flip() 
        reloj.tick(60) 

    return "menu"

if __name__ == "__main__":
    pygame.init()
    result = run()
    if result == "quit":
        pygame.quit()
        sys.exit()
    elif result == "menu":
        print("Regresando al menú (simulado).")
        pygame.quit()
        sys.exit()
    elif result == "restart":
        print("Reiniciando el nivel (simulado).")
        pygame.quit()
        sys.exit()