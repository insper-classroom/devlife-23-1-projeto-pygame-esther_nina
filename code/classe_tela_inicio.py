import pygame
from classe_jogo import *

ROXO_ESCURO = (29, 0, 33)
AZUL_CLARINHO = (200, 245, 247)
AZUL_BOLA = (115, 209, 208)
ROSA = (228, 97, 128)
AZUL_FUNDO = (23, 28, 48)


class TelaInicio:
    def __init__(self):
        pygame.init()
        
        self.tamanho_tela = [500, 700]
        self.window = pygame.display.set_mode(self.tamanho_tela)
        self.imagem_inicio = pygame.image.load('assets/minerando.jpeg')
        self.imagem_inicio = pygame.transform.scale(self.imagem_inicio, (700, 700))
        
        self.fonte_inicio = pygame.font.Font('assets/Emulogic-zrEw.ttf', 20)
        self.fonte_titulo = pygame.font.Font('assets/PlaymegamesReguler-2OOee.ttf', 45)
        self.fonte_footer = pygame.font.Font('assets/PlaymegamesReguler-2OOee.ttf', 20)
        self.jogo = Jogo()
    
    def colisao_ponto_retangulo(self, pontox, pontoy, rectx, recty, rectw, recth):
        if rectx <= pontox <= (rectx + rectw) and recty <= pontoy <= (recty + recth):
            return True
        else:
            return False

    def atualiza_tela(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                self.coordenadas_clique = pygame.mouse.get_pos() 
                # Se o jogador clicou no retângulo 'inicio', o jogo se inicia
                if self.colisao_ponto_retangulo(self.coordenadas_clique[0], self.coordenadas_clique[1], 150, 500, 200, 100): 
                    self.jogo.game_loop()
                    return False
        return True

    def desenha_tela_inicio(self):
        self.window.blit(self.imagem_inicio, (- 87, 0))
        pygame.draw.rect(self.window, AZUL_CLARINHO, (150, 500, 200, 100))
        # Desenhando o botão e as suas limitações
        pygame.draw.rect(self.window, ROSA, (150, 500, 200, 10))
        pygame.draw.rect(self.window, ROSA, (150, 500, 10, 100))
        pygame.draw.rect(self.window, ROSA, (150, 600, 200, 10))
        pygame.draw.rect(self.window, ROSA, (350, 500, 10, 110))
        
        inicio = self.fonte_inicio.render('Inicio', self.fonte_inicio, ROXO_ESCURO)
        self.window.blit(inicio, (190, 540))

        titulo = self.fonte_titulo.render('Platforms of Salvation', self.fonte_titulo, ROXO_ESCURO)
        self.window.blit(titulo, (46, 50))

        footer = self.fonte_footer.render('Desenvolvido por Esther Caroline e Nina Savoy', self.fonte_footer, AZUL_CLARINHO)
        self.window.blit(footer, (63, 670)) 

        pygame.display.update()

    def inicio_loop(self): # O loop para a tela início
        inicio = True
        while inicio:
            inicio = self.atualiza_tela()
            if inicio:
                self.desenha_tela_inicio()
