import pygame
import random
from classe_plataforma import *
from classe_tela_fim import *
from classe_coins import *

ROXO_ESCURO = (29, 0, 33)
AZUL_CLARINHO = (200, 245, 247)
AZUL_BOLA = (115, 209, 208)
ROSA = (228, 97, 128)
AZUL_FUNDO = (23, 28, 48)

class Jogo:
    def __init__(self):
        pygame.init()
        # Set tamanhos e cores
        self.tamanho_tela = [500, 700]
        self.clicou =  False
        self.pos_inicial_linha = (0, 0)
        self.pos_final_linha = (0, 0)
        # Calcular a posição do jogador após pingar
        self.bolinha_pos = [240, 150]
        self.bolinha_vel = [75, 0]
        self.bolinha_tempo = 0
        # Loading de imagens e sons
        self.bloco_img =  pygame.transform.scale(pygame.image.load('assets/PEDRA.png'), (50, 50))
        self.pedrinha_img = pygame.transform.scale(pygame.image.load('assets/pedrinha.png'),(40, 40))    
        self.caverna = pygame.transform.scale(pygame.image.load('assets/caverna.jpeg'),(1000 , 1000))    
        self.fonte = pygame.font.Font('assets/Emulogic-zrEw.ttf', 13)
        self.window = pygame.display.set_mode(self.tamanho_tela)
        
        self.comecou = False
        self.qntd_linhas = 0
        self.primeiro = 0
        self.primeiro_coins = 0
        
        self.caverna1_y = - 300
        self.caverna2_y = - 1300
        self.caverna3_y = - 2300

        self.bloco_horizontal_y = 650
        self.bloco_vertical_y = 0
        self.plataformas_anteriores = []

        # Define score
        self.score = 0
        self.maior_score = 0

        # Criação das moedas
        self.all_coins = pygame.sprite.Group()
        for i in range(10):
            moeda =  Coins()
            self.all_coins.add(moeda)

    def cria_pedras(self):
        pos_pedras = [1, 51, 101, 151, 201, 251, 301, 351, 401, 451, 500]
        self.pedras = pygame.sprite.Group()
        x = random.choice(pos_pedras)
        self.pedras.add((x,1))

    def bola_quica(self):
        # Intervalo de tempo
        hm = pygame.time.get_ticks()
        delta = (hm - self.bolinha_tempo) / 1000
        self.bolinha_tempo = hm

        # Calcula a velocidade alterada pela aceleração (gravidade) e o tempo
        self.bolinha_vel[1] += 175 * delta

        if Plataformas.colidiu(self.bolinha_pos):
            if Plataformas.verifica_angulo == 'flip':
                self.bolinha_vel[1] *= - 1
                self.bolinha_vel[0] *= - 1
            else:
                self.bolinha_vel[1] *= - 1
        # Com isso, calcula as novas posições
        self.bolinha_pos[0] += self.bolinha_vel[0] * delta
        self.bolinha_pos[1] += self.bolinha_vel[1] * delta

       # Coloca limites nas paredes
        if self.bolinha_pos[0] - 10 < 50 or self.bolinha_pos[0] + 10 >= 450:
            self.bolinha_vel[0] *= - 1
        if self.bolinha_pos[1] - 10 > self.bloco_horizontal_y:
            fim = TelaFim()
            TelaFim.fim_loop(fim)

    def alpha_fab(self):
        self.relogio = pygame.time.get_ticks() #em milissegundos
        subtracao = self.relogio - self.primeiro
        if subtracao >= 100:
            self.primeiro = self.relogio
            return True
        return False
    
    def tempo_coins(self):
        self.relogio_coins = pygame.time.get_ticks() #em milissegundos
        subtracao_coins = self.relogio_coins - self.primeiro_coins
        if subtracao_coins >= 100:
            self.primeiro_coins = self.relogio_coins
            return True
        return False

    def atualiza_estado(self):
        # Muda animação da moeda
        tempo = Jogo.tempo_coins(self)
        if tempo:
            self.all_coins.update()
                

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    self.coordenadas_comeco = pygame.mouse.get_pos()
                    self.pos_inicial_linha = [self.coordenadas_comeco[0], self.coordenadas_comeco[1]]
                    # Recomeça o "clicou" para que as linhas sejam criadas separadamente
                    self.clicou = False
                    # Impedir que a bolinha entre dentro da parede 
                    if self.pos_inicial_linha[0] < 50:
                        self.pos_inicial_linha[0] = 50
                    elif self.pos_inicial_linha[0] > 450:
                        self.pos_inicial_linha[0] = 450
                    elif self.pos_inicial_linha[1] > 650:
                        self.pos_inicial_linha[1] =  650

            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    # Apenas após o mouse é solto que a linha pode ser desenhada
                    self.clicou =  True
                    # Não permitir que ele desenhe a primeira linha após clicar no 'Inicio'
                    self.qntd_linhas += 1

                    self.coordenadas_final = pygame.mouse.get_pos()
                    self.pos_final_linha = [self.coordenadas_final[0], self.coordenadas_final[1]]
                    # Impedir (novamente) que a bolinha entre dentro da parede 
                    if self.pos_final_linha[0] < 50:

                        self.pos_final_linha[0] = 50
                    elif self.pos_final_linha[0] > 450:
                        self.pos_final_linha[0] = 450
                    elif self.pos_final_linha[1] > 650:
                        self.pos_final_linha[1] =  650
            
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    self.comecou = True 
                    self.bolinha_tempo = pygame.time.get_ticks()     
        return True

    def desenha(self):
        self.window.fill(AZUL_FUNDO)
        if self.caverna1_y >= - 300:
            self.window.blit(self.caverna, (- 500, self.caverna1_y))
            self.window.blit(self.caverna, (0, self.caverna2_y))
            self.window.blit(self.caverna, (- 500, self.caverna3_y))
        elif self.caverna2_y >= - 300:
           self.window.blit(self.caverna, (0, self.caverna2_y))
           self.window.blit(self.caverna, (- 500, self.caverna1_y))
           self.window.blit(self.caverna, (0, self.caverna3_y))
        else:
            self.window.blit(self.caverna, (- 500, self.caverna1_y))
            self.window.blit(self.caverna, (0, self.caverna2_y))
        # Desenha pedras paredes
        x = 0
        y = self.bloco_vertical_y
        while x <= self.tamanho_tela[0]:
            # BOTTOM
            self.window.blit(self.bloco_img, (x, self.bloco_horizontal_y)) 
            x += 50
        while y <= self.tamanho_tela[1]:
            # WALLS
            self.window.blit(self.bloco_img, (0, y))
            self.window.blit(self.bloco_img, (450, y))
            y += 50
        # A bola permanece parada até o jogador dar início
        if self.comecou:
            self.bola_quica()
            if self.alpha_fab():
                self.caverna1_y += 10
                self.caverna2_y += 10
                self.caverna3_y += 10
                self.bloco_horizontal_y += 10
                self.bloco_vertical_y += 10
        else:
            inicio = self.fonte.render('Aperte espaco para comecar', self.fonte, AZUL_CLARINHO)
            self.window.blit(inicio, (78, 30))

        pygame.draw.circle(self.window, AZUL_BOLA, self.bolinha_pos, 10)

        # Desenha plataformas
        if self.clicou == True:
            if self.qntd_linhas > 1:
                Plataformas(self.pos_inicial_linha, self.pos_final_linha)
        Plataformas.verifica_linhas()
        Plataformas.desenha_plataforma(self.window)

        # Desenha coins
        self.all_coins.draw(self.window)
        pygame.display.update()

    def game_loop(self):
        game = True
        while game:
            game = self.atualiza_estado()
            if game:
                self.desenha()
            