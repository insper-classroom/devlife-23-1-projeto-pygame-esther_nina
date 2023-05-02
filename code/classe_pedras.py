import pygame
import random 

class Pedras():
    def __init__(self):
        x = random.randint(50, 450)
        self.coordenadas = [x, - 100]
        self.velocidade = [10, 100]
        self.pedra_tempo = - 1
        self.pedras = []

    def pedra_cai(self, posicao, velocidade):
        hm = pygame.time.get_ticks()
        if self.pedra_tempo != - 1:
            delta = (hm - self.pedra_tempo) / 1000

            velocidade[1] += delta * 10

            posicao[0] += velocidade[0] * delta
            posicao[1] += velocidade[1] * delta
        self.pedra_tempo = hm
