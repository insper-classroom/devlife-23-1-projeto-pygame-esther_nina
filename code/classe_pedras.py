import pygame
import random 

class Pedras():
    def __init__(self):
        x = random.randint(50, 390)
        self.coordenadas = [x, - 100]
        self.velocidade = [10, 100]
        self.pedra_tempo = - 1
        self.pedras = []

    def pedra_cai(self):
        hm = pygame.time.get_ticks()
        if self.pedra_tempo != - 1:
            delta = (hm - self.pedra_tempo) / 1000

            self.velocidade[1] += delta * 60

            self.coordenadas[0] += self.velocidade[0] * delta
            self.coordenadas[1] += self.velocidade[1] * delta
        self.pedra_tempo = hm

    def colisao_bola(self, posicao_bola):
        if self.coordenadas[0] <= posicao_bola[0] + 10 <= (self.coordenadas[0] + 40) and self.coordenadas[1] <= posicao_bola[1] <= (self.coordenadas[1] + 40):
            return True
        else:
            return False
