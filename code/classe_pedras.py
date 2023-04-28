import pygame
import random 

class Pedras(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('assets/pedrinha.png')
        x = random.randint(50, 450)
        y = random.randint(- 1300, 0)
        self.coordenadas = [x, y]
        self.velocidade = [10, 100]
        

    def pedra_cai(self, bolinha_tempo):
        hm = pygame.time.get_ticks()
        delta = (hm - bolinha_tempo) / 1000
        bolinha_tempo = hm

        self.velocidade[1] += delta * 1000
        
        self.coordenadas[0] += self.velocidade[0] * delta
        self.coordenadas[1] += self.velocidade[1] * delta
        return bolinha_tempo, hm

    def desenha_pedra(self,window):
        window.blit(self.img, [self.coordenadas[0], self.coordenadas[1]])
            

