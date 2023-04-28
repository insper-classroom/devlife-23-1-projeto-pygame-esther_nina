import pygame
import random 

class Pedras:
    pedras_anteriores = []
    def __init__(self):
        self.img = pygame.image.load('assets/pedrinha.png')
        x = random.randint(50, 450)
        y = random.randint(- 1300, 0)
        self.coordenadas = [x, y]
        self.velocidade = [10, 100]
        Pedras.pedras_anteriores.append(self)

    def pedra_cai(self):
        hm = pygame.time.get_ticks()
        delta = (hm - self.bolinha_tempo) / 1000
        self.bolinha_tempo = hm

        self.velocidade[1] += delta * 1000
        
        self.coordenadas[0] += self.velocidade[0] * delta
        self.coordenadas[1] += self.velocidade[1] * delta

    def desenha_pedra(window):
        for pedra in Pedras.pedras_anteriores:
            window.blit(pedra.img, [pedra.coordenadas[0], pedra.coordenadas[1]])
            

