import pygame
from sympy import Symbol, And, Or, Not

pygame.init()

ANCHO_VENTANA, ALTO_VENTANA = 1200, 650
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Juego de Misterio")

mapa = pygame.image.load("mapa.png")
mapa = pygame.transform.scale(mapa, (600, 500))

juan = Symbol("juan")
maria = Symbol("maria")
carlos = Symbol("carlos")
martillo = Symbol("martillo")
veneno = Symbol("veneno")
pistola = Symbol("pistola")
patio = Symbol("patio")
cocina = Symbol("cocina")
sala = Symbol("sala")

conocimiento = And(
    Or(juan, maria, carlos),
    Or(cocina, patio, sala),
    Or(pistola, veneno, martillo),
    Not(cocina),
    Not(pistola),
    Or(juan, maria),
    Not(martillo),
    Not(maria),
    And(patio)
)

cuadros = {
    "Sospechosos": [juan, maria, carlos],
    "Armas": [veneno, pistola, martillo],
    "Lugares": [patio, cocina, sala]
}

estado_cuadros = {
    "Sospechosos": [None] * len(cuadros["Sospechosos"]),
    "Armas": [None] * len(cuadros["Armas"]),
    "Lugares": [None] * len(cuadros["Lugares"])
}

def verificar_marcado_y_comparar():
    for categoria, items in cuadros.items():
        for i, item in enumerate(items):
            if estado_cuadros[categoria][i] == 'marcado':
                if not verificar_todo(conocimiento, item, simbolos):
                    return False
    return True

def verificar_todo(conocimiento, consulta, simbolos, modelo={}):
    if not simbolos:
        if conocimiento.subs(modelo) == True:
            return consulta.subs(modelo)
        return True
    else:
        restantes = simbolos.copy()
        p = restantes.pop()
        modelo_verdadero = modelo.copy()
        modelo_verdadero[p] = True
        modelo_falso = modelo.copy()
        modelo_falso[p] = False
        return (verificar_todo(conocimiento, consulta, restantes, modelo_verdadero) and
                verificar_todo(conocimiento, consulta, restantes, modelo_falso))

simbolos = [juan, maria, carlos, veneno, pistola, martillo, patio, cocina, sala]

culpable_encontrado = False
resultado_culpable = None
mensaje_error = None

pistas = [
    "No fue en la cocina.",
    "No fue con la pistola.",
    "El culpable es Juan o María.",
    "No fue con el martillo.",
    "No fue María.",
    "Fue en el patio."
]

indice_pista = 0

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, (categoria, items) in enumerate(cuadros.items()):
                for j, item in enumerate(items):
                    cuadro_x = 10 + (j * 200)
                    cuadro_y = 510 + (i * 50)
                    if cuadro_x < pos[0] < cuadro_x + 180 and cuadro_y < pos[1] < cuadro_y + 40:
                        if estado_cuadros[categoria][j] is None:
                            estado_cuadros[categoria][j] = 'marcado'
                        elif estado_cuadros[categoria][j] == 'marcado':
                            estado_cuadros[categoria][j] = 'descartado'
                        else:
                            estado_cuadros[categoria][j] = None

            if 620 < pos[0] < 720 and 270 < pos[1] < 300:
                if indice_pista < len(pistas):
                    indice_pista += 1

            if 730 < pos[0] < 830 and 270 < pos[1] < 300:
                culpable_encontrado = True
                for sospechoso in [juan, maria, carlos]:
                    for arma in [veneno, pistola, martillo]:
                        for lugar in [patio, cocina, sala]:
                            modelo = {
                                sospechoso: True,
                                arma: True,
                                lugar: True
                            }
                            resultado = verificar_todo(conocimiento, sospechoso, simbolos, modelo)
                            if resultado:
                                resultado_culpable = f"El culpable es {sospechoso}, el arma es {arma} y el lugar es {lugar}."
                                break
                        if culpable_encontrado:
                            break
                    if culpable_encontrado:
                        break

            if 840 < pos[0] < 940 and 270 < pos[1] < 300:
                if verificar_marcado_y_comparar():
                    mensaje_error = "¡Correcto! Has encontrado al culpable."
                else:
                    mensaje_error = "Fallaste. El culpable no coincide con tus sospechas."

    ventana.fill((255, 255, 255))
    ventana.blit(mapa, (0, 0))

    for i, (categoria, items) in enumerate(cuadros.items()):
        for j, item in enumerate(items):
            cuadro_x = 10 + (j * 200)
            cuadro_y = 510 + (i * 50)
            pygame.draw.rect(ventana, (200, 200, 200), (cuadro_x, cuadro_y, 180, 40), 0)
            fuente = pygame.font.Font(None, 24)
            texto = fuente.render(item.name, True, (0, 0, 0))
            ventana.blit(texto, (cuadro_x + 5, cuadro_y + 10))

            if estado_cuadros[categoria][j] == 'marcado':
                estado_texto = fuente.render('X', True, (0, 255, 0))
                ventana.blit(estado_texto, (cuadro_x + 150, cuadro_y + 10))
            elif estado_cuadros[categoria][j] == 'descartado':
                estado_texto = fuente.render('X', True, (255, 0, 0))
                ventana.blit(estado_texto, (cuadro_x + 150, cuadro_y + 10))

    pygame.draw.rect(ventana, (200, 0, 0), (620, 270, 100, 30), 0)
    pygame.draw.rect(ventana, (0, 200, 0), (730, 270, 100, 30), 0)
    pygame.draw.rect(ventana, (0, 0, 200), (840, 270, 100, 30), 0)

    fuente_botones = pygame.font.Font(None, 24)
    texto_pista = fuente_botones.render("Pista", True, (255, 255, 255))
    ventana.blit(texto_pista, (640, 275))
    texto_resolver = fuente_botones.render("Resolver", True, (255, 255, 255))
    ventana.blit(texto_resolver, (740, 275))
    texto_acusar = fuente_botones.render("Acusar", True, (255, 255, 255))
    ventana.blit(texto_acusar, (850, 275))

    if indice_pista > 0:
        pista_actual = pistas[indice_pista - 1]
        fuente_pista = pygame.font.Font(None, 24)
        texto_pista_actual = fuente_pista.render(pista_actual, True, (0, 0, 0))
        ventana.blit(texto_pista_actual, (620, 320))

    if culpable_encontrado and resultado_culpable:
        fuente_solucion = pygame.font.Font(None, 28)
        texto_solucion = fuente_solucion.render(resultado_culpable, True, (0, 0, 0))
        ventana.blit(texto_solucion, (620, 400))

    if mensaje_error:
        fuente_error = pygame.font.Font(None, 28)
        texto_error = fuente_error.render(mensaje_error, True, (255, 0, 0))
        ventana.blit(texto_error, (620, 430))

    pygame.display.flip()

pygame.quit()
