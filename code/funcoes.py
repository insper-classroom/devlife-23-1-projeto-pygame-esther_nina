import pygame
import random
import math

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
        self.caverna_y = - 250
        self.bloco_y = 650
        
        self.plataformas_anteriores = []

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
        if self.bolinha_pos[1] - 10 > 650:
            self.bolinha_vel[1] *= - 1 

    def alpha_fab(self):
        self.relogio = pygame.time.get_ticks() #em milissegundos
        subtracao = self.relogio - self.primeiro
        if subtracao >= 100:
            self.primeiro = self.relogio
            return True
        return False

    def atualiza_estado(self):
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
                    
        return True

    def desenha(self):
        self.window.fill(AZUL_FUNDO)
        self.window.blit(self.caverna, (- 500, self.caverna_y))
        # Desenha pedras paredes
        x = 0
        y = 0
        while x <= self.tamanho_tela[0]:
            # BOTTOM
            self.window.blit(self.bloco_img, (x, self.bloco_y)) 
            x += 50
        while y <= self.tamanho_tela[1] - 50:
            # WALLS
            self.window.blit(self.bloco_img, (0, y))
            self.window.blit(self.bloco_img, (450, y))
            y += 50
        
        # A bola permanece parada até o jogador dar início
        if self.comecou:
            self.bola_quica()
            if self.alpha_fab():
                self.caverna_y += 1
                self.bloco_y += 1
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
        # Criador das nossas linhas, nas quais a bolinha pulará em
        self.coordenadas_comeco = coordenada_inicio
        self.coordenadas_final = coordenada_final
        Plataformas.plataformas_anteriores.append(self)

    def desenha_plataforma(window):
        for plataforma in Plataformas.plataformas_anteriores:
                pygame.draw.polygon(window, plataforma.cor, (plataforma.coordenadas_comeco, plataforma.coordenadas_final, (plataforma.coordenadas_final[0], plataforma.coordenadas_final[1] - 5), (plataforma.coordenadas_comeco[0], plataforma.coordenadas_comeco[1] - 5)))

    def colidiu(bola_pos): # Cálculo de interssecção ponto e reta, porém limitada, para as colisões com plataformas
        for p in Plataformas.plataformas_anteriores:
            raio = 10
            a = - ((p.coordenadas_comeco[1] - p.coordenadas_final[1])/(p.coordenadas_comeco[0] - p.coordenadas_final[0]))
            b = 1
            c = - (a * p.coordenadas_comeco[0] + p.coordenadas_comeco[1])
            dist = abs(a * bola_pos[0] + b * bola_pos[1] + c) / math.sqrt(a ** 2 + b ** 2)
            if dist <= raio and bola_pos[0] < p.coordenadas_final[0] and bola_pos[0] > p.coordenadas_comeco[0] :
                return True
        return False

    def verifica_linhas(): # Deletar plataformas anteriores
        linhas = len(Plataformas.plataformas_anteriores)
        if linhas >= 2:
            del Plataformas.plataformas_anteriores[0]

    def verifica_angulo(vel_bola): # Interlúdio de física e matemática, para que a colisão seja mais realista
        for plataforma in Plataformas.plataformas_anteriores:
            cateto_oposto = abs(plataforma.coordenadas_final[0] - plataforma.coordenadas_comeco[0])
            cateto_adjacente = abs (plataforma.coordenadas_final[1] - plataforma.coordenadas_comeco[1])
            # Cálculos trigonométricos
            tangente = cateto_oposto / cateto_adjacente
            angulo_rad = math.atan(tangente)
            angulo_grau = math.degrees(angulo_rad)
            
            angulo_linha = 180 - (angulo_grau + 90)
            if angulo_linha > 70:
                return 'continua'
            elif angulo_linha > 45 and angulo_linha < 70:
                if vel_bola > 0:
                    return 'flip'
                else:
                    return 'continua'
            elif angulo_linha < 45 and angulo_linha > 20:
                if vel_bola > 0:
                    return 'continua'
                else:
                    return 'flip'
            else:
                if vel_bola > 0:
                    return 'continua'
                else:
                    return 'flip'
               
             
        
class TelaInicio:
    def __init__(self):
        pygame.init()
        
        self.tamanho_tela = [500, 700]
        self.window = pygame.display.set_mode(self.tamanho_tela)
        self.imagem_inicio = pygame.image.load('assets/minerando.jpeg')
        self.imagem_inicio = pygame.transform.scale(self.imagem_inicio, (700, 700))
        
        self.fonte_inicio = pygame.font.Font('assets/Emulogic-zrEw.ttf', 20)
        self.fonte_titulo = pygame.font.Font('assets/PlaymegamesReguler-2OOee.ttf', 45)
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

        pygame.display.update()

    def inicio_loop(self): # O loop para a tela início
        inicio = True
        while inicio:
            inicio = self.atualiza_tela()
            if inicio:
                self.desenha_tela_inicio()


class Coins(pygame.sprite.Sprite):
    def __init__(self):
        self.animation = [pygame.image.load('assets/coin1.png') , pygame.image.load('assets/coin2.png'), 
                    pygame.image.load('assets/coin3.png'), pygame.image.load('assets/coin4.png'), 
                    pygame.image.load('assets/coin5.png'), 	pygame.image.load('assets/coin6.png'), 
                    pygame.image.load('assets/coin7.png'), pygame.image.load('assets/coin8.png')]
        self.frame = 0
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50,650)
        self.rect.y = random.randint(0,450)
        self.posicoes = []

    def update(self):
        self.frame += 1
        if self.frame >= len(self.animation):
            self.frame_index = 0
        self.image = self.animation[self.frame]

    # def desenha_coin(self, window):
    #     for i in range(10):
    #         self.posicoes.append((x,y))
            
    #     grupo = pygame.sprite.Group()
    #     grupo.add(sprite)

    #         # Update sprites
    #     # grupo.update()
    #     for moeda in self.posicoes:
    #         window.blit(self.image, moeda)
    # pygame.display.flip()
    