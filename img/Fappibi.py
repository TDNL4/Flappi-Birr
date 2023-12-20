import pygame, sys, random 

def dibujar_suelo():
	screen.blit(superficie_suelo, (pos_x_suelo, 900))
	screen.blit(superficie_suelo, (pos_x_suelo + 576, 900))

def crear_tubo():
	posicion_tubo = random.choice(altura_tubo)
	tubo_inferior = superficie_tubo.get_rect(midtop=(700, posicion_tubo))
	tubo_superior = superficie_tubo.get_rect(midbottom=(700, posicion_tubo - 300))
	return tubo_inferior, tubo_superior

def mover_tubos(tubos):
	for tubo in tubos:
		tubo.centerx -= 5
	return tubos

def dibujar_tubos(tubos):
	for tubo in tubos:
		if tubo.bottom >= 1024:
			screen.blit(superficie_tubo, tubo)
		else:
			tubo_invertido = pygame.transform.flip(superficie_tubo, False, True)
			screen.blit(tubo_invertido, tubo)

def quitar_tubos(tubos):
	for tubo in tubos:
		if tubo.centerx == -600:
			tubos.remove(tubo)
	return tubos

def verificar_colision(tubos):
	for tubo in tubos:
		if rectangulo_pajaro.colliderect(tubo):
			sonido_muerte.play()
			return False

	if rectangulo_pajaro.top <= -100 or rectangulo_pajaro.bottom >= 900:
		return False

	return True

def rotar_pajaro(pajaro):
	nuevo_pajaro = pygame.transform.rotozoom(pajaro, -movimiento_pajaro * 3, 1)
	return nuevo_pajaro

def animacion_pajaro():
	nuevo_pajaro = frames_pajaro[indice_pajaro]
	nuevo_rectangulo_pajaro = nuevo_pajaro.get_rect(center=(100, rectangulo_pajaro.centery))
	return nuevo_pajaro, nuevo_rectangulo_pajaro

def mostrar_puntaje(estado_juego):
	if estado_juego == 'main_game':
		superficie_puntaje = fuente_juego.render(str(int(puntaje)), True, (255, 255, 255))
		rectangulo_puntaje = superficie_puntaje.get_rect(center=(288, 100))
		screen.blit(superficie_puntaje, rectangulo_puntaje)
	if estado_juego == 'game_over':
		superficie_puntaje = fuente_juego.render(f'Puntaje: {int(puntaje)}', True, (255, 255, 255))
		rectangulo_puntaje = superficie_puntaje.get_rect(center=(288, 100))
		screen.blit(superficie_puntaje, rectangulo_puntaje)

		superficie_puntaje_alto = fuente_juego.render(f'Mejor puntaje: {int(mejor_puntaje)}', True, (255, 255, 255))
		rectangulo_puntaje_alto = superficie_puntaje_alto.get_rect(center=(288, 850))
		screen.blit(superficie_puntaje_alto, rectangulo_puntaje_alto)

def actualizar_puntaje(puntaje, mejor_puntaje):
	if puntaje > mejor_puntaje:
		mejor_puntaje = puntaje
	return mejor_puntaje

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
fuente_juego = pygame.font.Font('04B_19.ttf', 40)

# Variables del juego
gravedad = 0.30
movimiento_pajaro = 0
juego_activo = True
puntaje = 0
mejor_puntaje = 0

superficie_fondo = pygame.image.load('Images/background-day.png').convert()
superficie_fondo = pygame.transform.scale2x(superficie_fondo)

superficie_suelo = pygame.image.load('Images/base.png').convert()
superficie_suelo = pygame.transform.scale2x(superficie_suelo)
pos_x_suelo = 0

pajaro_abajo = pygame.transform.scale2x(pygame.image.load('Images/bluebird-downflap.png').convert_alpha())
pajaro_medio = pygame.transform.scale2x(pygame.image.load('Images/bluebird-midflap.png').convert_alpha())
pajaro_arriba = pygame.transform.scale2x(pygame.image.load('Images/bluebird-upflap.png').convert_alpha())
frames_pajaro = [pajaro_abajo, pajaro_medio, pajaro_arriba]
indice_pajaro = 0
superficie_pajaro = frames_pajaro[indice_pajaro]
rectangulo_pajaro = superficie_pajaro.get_rect(center=(100, 512))

PAJARO_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(PAJARO_FLAP, 200)

superficie_tubo = pygame.image.load('Images/pipe-green.png')
superficie_tubo = pygame.transform.scale2x(superficie_tubo)
tubo_lista = []
SPAWNTUBO = pygame.USEREVENT
pygame.time.set_timer(SPAWNTUBO, 1200)
altura_tubo = [400, 600, 800]

superficie_fin_juego = pygame.transform.scale2x(pygame.image.load('Images/message.png').convert_alpha())
rectangulo_fin_juego = superficie_fin_juego.get_rect(center=(288, 512))

sonido_aleta = pygame.mixer.Sound('sfx/wing.wav')
sonido_muerte = pygame.mixer.Sound('sfx/hit.wav')
sonido_puntaje = pygame.mixer.Sound('sfx/point.wav')
cuenta_regresiva_sonido_puntaje = 100

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and juego_activo:
				movimiento_pajaro = 0
				movimiento_pajaro -= 12
				sonido_aleta.play()
			if event.key == pygame.K_SPACE and not juego_activo:
				juego_activo = True
				tubo_lista.clear()
				rectangulo_pajaro.center = (100, 512)
				movimiento_pajaro = 0
				puntaje = 0

		if event.type == SPAWNTUBO:
			tubo_lista.extend(crear_tubo())

		if event.type == PAJARO_FLAP:
			if indice_pajaro < 2:
				indice_pajaro += 1
			else:
				indice_pajaro = 0

			superficie_pajaro, rectangulo_pajaro = animacion_pajaro()

	screen.blit(superficie_fondo, (0, 0))

	if juego_activo:
		# Pájaro
		movimiento_pajaro += gravedad
		pajaro_rotado = rotar_pajaro(superficie_pajaro)
		rectangulo_pajaro.centery += movimiento_pajaro
		screen.blit(pajaro_rotado, rectangulo_pajaro)
		juego_activo = verificar_colision(tubo_lista)

		# Tubos
		tubo_lista = mover_tubos(tubo_lista)
		tubo_lista = quitar_tubos(tubo_lista)
		dibujar_tubos(tubo_lista)
		
		puntaje += 0.01
		mostrar_puntaje('main_game')
		cuenta_regresiva_sonido_puntaje -= 1
		if cuenta_regresiva_sonido_puntaje <= 0:
			sonido_puntaje.play()
			cuenta_regresiva_sonido_puntaje = 100
	else:
		screen.blit(superficie_fin_juego, rectangulo_fin_juego)
		mejor_puntaje = actualizar_puntaje(puntaje, mejor_puntaje)
		mostrar_puntaje('game_over')

	# Suelo
	pos_x_suelo -= 1
	dibujar_suelo()
	if pos_x_suelo <= -576:
		pos_x_suelo = 0

	pygame.display.update()
	clock.tick(120) 