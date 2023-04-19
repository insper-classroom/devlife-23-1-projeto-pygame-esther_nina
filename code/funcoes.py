import pygame
import random

class Jogo:
    def __init__(self):
        pygame.init()
        # Set tamanhos e cores
        self.tamanho_tela = [500, 700]
        self.cor_fundo =  (22, 47, 109)
        self.bolinha = (150, 490, 5)
        self.cor_bolinha = (120, 148, 204)
        self.cor_plat = (7, 15, 33)
        self.clicou =  False
        # Calcular a posição do jogador após pingar
        self.bolinha_pos = [240, 50]
        self.bolinha_vel = [100, 150]
        self.bolinha_tempo = 0
        # Loading de imagens e sons
        self.bloco_img =  pygame.transform.scale(pygame.image.load('bloquinho.png'), (50,50))
        self.pedrinha_img = pygame.transform.scale(pygame.image.load('pedrinha.png'),(40,40))    
        self.window = pygame.display.set_mode(self.tamanho_tela)
        self.plataformas_anteriores = []


    def cria_pedras(self):
        pos_pedras = [1,51,101,151,201,251,301,351,401,451,500]
        self.pedras = pygame.sprite.Group()
        x = random.choice(pos_pedras)
        self.pedras.add((x,1))
        print(self.pedras())
        
    def bola_quica(self):
        # Intervalo de tempo
        hm = pygame.time.get_ticks()
        delta = (hm - self.bolinha_tempo) / 1000
        self.bolinha_tempo = hm

        # Calcula a velocidade alterada pela aceleração (gravidade) e o tempo
        self.bolinha_vel[1] += 350 * delta

        # Com isso, calcula as novas posições
        self.bolinha_pos[0] += self.bolinha_vel[0] * delta
        self.bolinha_pos[1] += self.bolinha_vel[1] * delta

       # Coloca limites nas paredes
        if self.bolinha_pos[0] - 10 < 50 or self.bolinha_pos[0] + 10 >= 450:
            self.bolinha_vel[0] *= - 1
        if self.bolinha_pos[1] - 10 > 650:
            self.bolinha_vel[1] *= - 1 

    def atualiza_estado(self):
        # self.plataformas =  Plataformas().atualiza_estado
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

            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    # Apenas após o mouse é solto que a linha pode ser desenhada
                    self.clicou =  True
                    self.coordenadas_final = pygame.mouse.get_pos()
                    self.pos_final_linha = [self.coordenadas_final[0], self.coordenadas_final[1]]
                    # Impedir (novamente) que a bolinha entre dentro da parede 
                    if self.pos_final_linha[0] < 50:
                        self.pos_final_linha[0] = 50
                    elif self.pos_final_linha[0] > 450:
                        self.pos_final_linha[0] = 450
                        
        return True

    def desenha(self):
        self.window.fill(self.cor_fundo)

        # Desenha pedras paredes
        x = 0
        y = 0
        while x <= self.tamanho_tela[0]:
            # BOTTOM
            self.window.blit(self.bloco_img, (x, 660)) 
            x += 50
        while y <= self.tamanho_tela[1] - 50:
            # WALLS
            self.window.blit(self.bloco_img, (0, y))
            self.window.blit(self.bloco_img, (450, y))
            y += 50
        self.bola_quica()
        pygame.draw.circle(self.window, (115, 209, 208), self.bolinha_pos, 10)

    #    Desenha plataformas
        if self.clicou == True:
            Plataformas(self.pos_inicial_linha, self.pos_final_linha)
        Plataformas.desenha_plataforma(self.window)
        pygame.display.update()

    def game_loop(self):
        game = True
        while game:
            game = self.atualiza_estado()
            if game:
                self.desenha()
            


class Plataformas:
    plataformas_anteriores = []
    rect_plataformas = []

    def __init__(self, coordenada_inicio, coordenada_final):
        self.cor = (255, 255, 255)
        self.coordenadas_comeco = coordenada_inicio
        self.coordenadas_final = coordenada_final
        Plataformas.plataformas_anteriores.append(self)

    def cria_rect(self):
        width =  self.c

    def colisao(self, largura, altura, cx, cy, raio): #esther comecei a mexer numa funcao de colisao da nossa bolinha e retangulo, to indo embora agora entao vou comitar soh pra c ter uma ideia (nao acabei ainda)
        self.coordenadas_comeco[0] #x
        self.coordenadas_comeco[1] #y
        largura = abs(self.coordenadas_final[0] -  self.coordenadas_comeco[0])
        altura = abs(self.coordenadas_final[1] -  self.coordenadas_comeco[1])
        if r1(0) < r2(0) + r2(2) and r1(0) + r1(2) > r2(0) and r1(1) < r2(1) + r2(3) and r1(3) + r1(0) > r2(1):
            return True
        else:
            return False
        
    def desenha_plataforma( window):
        # pygame.draw.polygon(self.window, self.cor, (self.coordenadas_comeco, self.coordenadas_final, (self.coordenadas_final[0], self.coordenadas_final[1] - 5), (self.coordenadas_comeco[0], self.coordenadas_comeco[1] - 5)))
        for plataforma in Plataformas.plataformas_anteriores:
            pygame.draw.polygon(window, plataforma.cor, (plataforma.coordenadas_comeco, plataforma.coordenadas_final, (plataforma.coordenadas_final[0], plataforma.coordenadas_final[1] - 3), (plataforma.coordenadas_comeco[0], plataforma.coordenadas_comeco[1] -3)))
