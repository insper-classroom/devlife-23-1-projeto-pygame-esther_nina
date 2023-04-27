import pygame
import random

class Coins(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        coin1 =  pygame.transform.scale(pygame.image.load('assets/coin1.png'), (150,60))
        coin2 =  pygame.transform.scale(pygame.image.load('assets/coin2.png'), (150,60))
        coin3 =  pygame.transform.scale(pygame.image.load('assets/coin3.png'), (150,60))
        coin4 =  pygame.transform.scale(pygame.image.load('assets/coin4.png'), (150,60))
        coin5 =  pygame.transform.scale(pygame.image.load('assets/coin5.png'), (150,60))
        coin6 =  pygame.transform.scale(pygame.image.load('assets/coin6.png'), (150,60))
        coin7 =  pygame.transform.scale(pygame.image.load('assets/coin7.png'), (150,60))
        coin8 =  pygame.transform.scale(pygame.image.load('assets/coin8.png'), (150,60))
        self.animation = [coin1 , coin2, coin3, coin4, coin5, 	coin6, coin7, coin8]

        self.frame = 0
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 350)
        self.rect.y = random.randint(-4000, 450)


    def colide(self, bola_pos):
        if bola_pos[0] >= self.rect.x and bola_pos[0] <= self.rect.x + 40 and bola_pos[1] >= self.rect.y and bola_pos[1] <= self.rect.y + 20:
            with open('moedas.txt', 'r') as moedas:
                qntd_moedas = int(moedas.read())
                qntd_moedas += 1
            with open('moedas.txt', 'w') as moedas:
                moedas.write(f'{qntd_moedas}')
            return True
        return False



    def update(self):
        self.frame += 1
        if self.frame >= len(self.animation):
            self.frame = 0
        self.image = self.animation[self.frame]
        self.rect.y += 5
    def draw(self, window):
        window.blit(self.image, self.rect)