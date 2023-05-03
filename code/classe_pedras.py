import pygame
import random 

class Pedras():
    def __init__(self):
        x = random.randint(50, 390)
        self.coordenadas = [x, - 100]
        self.velocidade = [10, 130]
        self.pedra_tempo = - 1
        self.rect = pygame.rect.Rect(x,-100,100,200)
        self.pedras = []

    def pedra_cai(self):
        hm = pygame.time.get_ticks()
        if self.pedra_tempo != - 1:
            delta = (hm - self.pedra_tempo) / 1000

            self.velocidade[1] += delta * 60

            self.coordenadas[0] += self.velocidade[0] * delta
            self.coordenadas[1] += self.velocidade[1] * delta
            self.rect[1]+= self.velocidade[1] * delta
        self.pedra_tempo = hm

    def colisao_bola(self, posicao_bola):
        if (posicao_bola[0] >= self.rect[0] and posicao_bola[0] <= self.rect[0] + 100) and posicao_bola[1] >= self.rect[1] and posicao_bola[1] <= self.rect[1] + 200:
            return True
        else:
            return False

    def desenha_explosao(self, window, lista, indice):
        window.blit(lista[indice], (self.coordenadas[0], self.coordenadas[1]))
        print('boom')
