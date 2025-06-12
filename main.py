import pygame
import sys

# Inicializar pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 600, 450
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego con Dos Personajes")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (200, 200, 200)

# Fuentes
fuente = pygame.font.SysFont(None, 30)
fuente_grande = pygame.font.SysFont(None, 50)

# Cargar fondo y personajes
fondo = pygame.image.load("fondo.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

imagen_personaje1 = pygame.image.load("personaje1.png")
imagen_personaje1 = pygame.transform.scale(imagen_personaje1, (50, 50))

imagen_personaje2 = pygame.image.load("personaje2.png")
imagen_personaje2 = pygame.transform.scale(imagen_personaje2, (50, 50))

# Clase Jugador
class Jugador:
    def __init__(self, x, y, imagen, controles):
        self.inicial_x = x
        self.inicial_y = y
        self.x = x
        self.y = y
        self.velocidad = 5
        self.imagen = imagen
        self.controles = controles
        self.puntos = 0
        self.activo = True
        self.ancho = 50
        self.alto = 50
        self.tiempo_inactivo = 0

    def mover(self, teclas):
        if not self.activo:
            return
        if teclas[self.controles["izquierda"]] and self.x > 0:
            self.x -= self.velocidad
        if teclas[self.controles["derecha"]] and self.x < ANCHO - self.ancho:
            self.x += self.velocidad
        if teclas[self.controles["arriba"]] and self.y > 0:
            self.y -= self.velocidad
        if teclas[self.controles["abajo"]] and self.y < ALTO - self.alto:
            self.y += self.velocidad

    def dibujar(self, pantalla):
        if self.activo:
            pantalla.blit(self.imagen, (self.x, self.y))

    def reaparecer(self):
        self.x = self.inicial_x
        self.y = self.inicial_y
        self.activo = True
        self.tiempo_inactivo = 0

# Función para colisión
def detectar_colision(j1, j2):
    rect1 = pygame.Rect(j1.x, j1.y, j1.ancho, j1.alto)
    rect2 = pygame.Rect(j2.x, j2.y, j2.ancho, j2.alto)
    return rect1.colliderect(rect2)

# Botón rectangular
def dibujar_boton(texto, x, y, ancho, alto, color, hover_color, fuente):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, ancho, alto)

    if rect.collidepoint(mouse):
        pygame.draw.rect(pantalla, hover_color, rect)
        if click[0]:
            return True
    else:
        pygame.draw.rect(pantalla, color, rect)

    texto_render = fuente.render(texto, True, NEGRO)
    pantalla.blit(texto_render, (x + (ancho - texto_render.get_width()) // 2,
                                  y + (alto - texto_render.get_height()) // 2))
    return False

# Función de juego principal
def jugar():
    jugador1 = Jugador(100, 200, imagen_personaje1, {
        "izquierda": pygame.K_LEFT,
        "derecha": pygame.K_RIGHT,
        "arriba": pygame.K_UP,
        "abajo": pygame.K_DOWN
    })

    jugador2 = Jugador(400, 200, imagen_personaje2, {
        "izquierda": pygame.K_a,
        "derecha": pygame.K_d,
        "arriba": pygame.K_w,
        "abajo": pygame.K_s
    })

    reloj = pygame.time.Clock()
    ganador = None
    ejecutando = True

    while ejecutando:
        reloj.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        jugador1.mover(teclas)
        jugador2.mover(teclas)

        # Lógica de colisión
        if jugador1.activo and jugador2.activo and detectar_colision(jugador1, jugador2):
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_LEFT] or teclas[pygame.K_UP] or teclas[pygame.K_DOWN]:
                jugador1.puntos += 1
                jugador2.activo = False
                jugador2.tiempo_inactivo = pygame.time.get_ticks()
            elif teclas[pygame.K_a] or teclas[pygame.K_d] or teclas[pygame.K_w] or teclas[pygame.K_s]:
                jugador2.puntos += 1
                jugador1.activo = False
                jugador1.tiempo_inactivo = pygame.time.get_ticks()

        # Reapariciones
        tiempo_actual = pygame.time.get_ticks()
        for jugador in [jugador1, jugador2]:
            if not jugador.activo and tiempo_actual - jugador.tiempo_inactivo >= 500:
                jugador.reaparecer()

        pantalla.blit(fondo, (0, 0))
        jugador1.dibujar(pantalla)
        jugador2.dibujar(pantalla)

        # Mostrar puntos
        texto_p1 = fuente.render(f"Puntos J1: {jugador1.puntos}", True, NEGRO)
        texto_p2 = fuente.render(f"Puntos J2: {jugador2.puntos}", True, NEGRO)
        pantalla.blit(texto_p1, (10, 10))
        pantalla.blit(texto_p2, (10, 40))

        # Verificar ganador
        if jugador1.puntos >= 5:
            ganador = "Jugador 1"
        elif jugador2.puntos >= 5:
            ganador = "Jugador 2"

        if ganador:
            mensaje = fuente_grande.render(f"¡{ganador} gana!", True, ROJO)
            pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO//2 - mensaje.get_height()//2))

            if dibujar_boton("Reiniciar", ANCHO//2 - 60, ALTO//2 + 50, 120, 40, GRIS, AZUL, fuente):
                jugar()  # reiniciar el juego
                return

        pygame.display.update()

# Pantalla de inicio
def pantalla_inicio():
    while True:
        pantalla.blit(fondo, (0, 0))
        titulo = fuente_grande.render("¡Juego de Dos Jugadores!", True, AZUL)
        instrucciones1 = fuente.render("Jugador 1: Flechas ← ↑ ↓ →", True, NEGRO)
        instrucciones2 = fuente.render("Jugador 2: Teclas A W S D", True, NEGRO)
        instrucciones3 = fuente.render("¡Tóquense para ganar puntos! El primero en llegar a 5 gana.", True, NEGRO)

        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))
        pantalla.blit(instrucciones1, (ANCHO//2 - instrucciones1.get_width()//2, 120))
        pantalla.blit(instrucciones2, (ANCHO//2 - instrucciones2.get_width()//2, 150))
        pantalla.blit(instrucciones3, (ANCHO//2 - instrucciones3.get_width()//2, 180))

        if dibujar_boton("Iniciar", ANCHO//2 - 60, 250, 120, 50, GRIS, AZUL, fuente):
            return

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Ejecutar
pantalla_inicio()
jugar()
