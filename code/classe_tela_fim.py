import pygame
from classe_jogo import *

ROXO_ESCURO = (29, 0, 33)
AZUL_CLARINHO = (200, 245, 247)
AZUL_BOLA = (115, 209, 208)
ROSA = (228, 97, 128)
AZUL_FUNDO = (23, 28, 48)
BRANCO = (255, 255, 255)

class TelaFim:
    def __init__(self):
        pygame.init()
        
        self.tamanho_tela = [500, 700]
        self.window = pygame.display.set_mode(self.tamanho_tela)
        self.imagem_inicio = pygame.image.load('assets/minerando.jpeg')
        self.imagem_inicio = pygame.transform.scale(self.imagem_inicio, (700, 700))
        
        self.fonte = pygame.font.Font('assets/Emulogic-zrEw.ttf', 20)
        self.jogo = Jogo()


    def atualiza_tela(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.K_r:
                    self.jogo.game_loop()
                    return False
        return True

    def desenha_tela_inicio(self):
        self.window.blit(self.imagem_inicio, (- 87, 0))
        pygame.draw.rect(self.window, AZUL_CLARINHO, (150, 500, 200, 100))
        
        game_over = self.fonte_titulo.render('A alma se perdeu...', self.fonte_titulo, ROXO_ESCURO)
        self.window.blit(game_over, (46, 300))

        restart = self.fonte.render('Pressione 'R' para recomeçar', self.fonte, ROXO_ESCURO)
        self.window.blit(restart, (100, 650))

        score =  self.fonte.render(f'Score: {self.score}', self.fonte, ROXO_ESCURO)
        self.window.blit(score, (100, 540))

        maior_score = self.fonte.render(f'Highest Score:: {self.maior_score}', self.fonte, ROXO_ESCURO)
        self.window.blit(maior_score, (100, 600))
        pygame.display.update()

    def fim_loop(self): # O loop para a tela de fim
        fim = True
        while fim:
            fim = self.atualiza_tela()
            if fim:
                self.desenha_tela_inicio()
