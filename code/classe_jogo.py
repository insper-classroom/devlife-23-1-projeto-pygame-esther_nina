import pygame
from classe_plataforma import *
from classe_coins import *
from extra import *
from classe_pedras import *

class Jogo:
    def __init__(self):
        pygame.init()
        # Set tamanhos e cores
        self.tamanho_tela = [500, 700]
        self.clicou =  False
        self.pos_inicial_linha = [0, 0]
        self.pos_final_linha = [0, 0]
        self.window = pygame.display.set_mode(self.tamanho_tela)
        # Calcular a posição do jogador após pingar
        self.bolinha_pos = [240, 150]
        self.bolinha_vel = [75, 0]
        self.bolinha_tempo = 0
        self.pedra_tempo = 0
        # Loading de imagens e sons
        self.bloco_img =  pygame.transform.scale(pygame.image.load('assets/PEDRA.png'), (50, 50))
        self.pedrinha = pygame.transform.scale(pygame.image.load('assets/pedrinha.png'),(100, 200))    
        self.caverna = pygame.transform.scale(pygame.image.load('assets/caverna.jpeg'),(1000 , 1000))    
        self.fonte = pygame.font.Font('assets/Emulogic-zrEw.ttf', 13)
        self.som_moeda =  pygame.mixer.Sound('assets/som moeda.mp3')


        self.explosao1 = pygame.transform.scale(pygame.image.load('assets/ex1.png'),(100, 200)) 
        self.explosao2 = pygame.transform.scale(pygame.image.load('assets/ex2.png'),(100, 200)) 
        self.explosao3 = pygame.transform.scale(pygame.image.load('assets/ex3.png'),(100, 200)) 
        self.explosao4 = pygame.transform.scale(pygame.image.load('assets/ex4.png'),(100, 200)) 
        self.explosao5 = pygame.transform.scale(pygame.image.load('assets/ex5.png'),(100, 200)) 
        self.explosao6 = pygame.transform.scale(pygame.image.load('assets/ex6.png'),(100, 200)) 
        self.explosao7 = pygame.transform.scale(pygame.image.load('assets/ex7.png'),(100, 200)) 
        self.explosao8 = pygame.transform.scale(pygame.image.load('assets/ex8.png'),(100, 200)) 

        self.explosao = [self.explosao1, self.explosao2,self.explosao3,self.explosao4,self.explosao5,self.explosao6,self.explosao7,self.explosao8]
        self.indice_explosao = 0
       
        # Variáveis de monitoração do início do jogo 
        self.pontuacao = 0
        self.comecou = False
        self.primeiro = 0
        self.primeiro_coins = 0
        self.intervalo = 100
    
        # Variáveis de movimentação do background
        self.caverna1_y = - 300 
        self.caverna2_y = - 1300
        self.bloco_horizontal_y = 650
        self.bloco_vertical_y = - 300

        # Criação de pedras
        self.pedrinhas = []

        # Criação das moedas
        self.all_coins = pygame.sprite.Group()
        for _ in range(40):
            moeda =  Coins()
            self.all_coins.add(moeda)

    # Atualiza o arquivo highest score
    def atualiza_hscore(self):
        with open('highestscore.txt', 'r') as hscore:
            maior_score = hscore.read()
            if self.pontuacao > int(maior_score):
                with open('highestscore.txt', 'w') as hscore:
                    hscore.write(f'{self.pontuacao}')

    def cria_pedras(self):
        pedra = Pedras()
        self.pedrinhas.append(pedra)

    def bola_quica(self):
        # Intervalo de tempo
        hm = pygame.time.get_ticks()
        delta = (hm - self.bolinha_tempo) / 1000
        self.bolinha_tempo = hm

        # Calcula a velocidade alterada pela aceleração (gravidade) e o tempo
        self.bolinha_vel[1] += 175 * delta
        
        # Verifica se a bolinha colide com alguma platafroma
        colidiu = Plataformas.colidiu(self.bolinha_pos)
        verifica =  Plataformas.verifica_angulo(self.bolinha_vel)
        if colidiu and verifica == 'flip':
            self.bolinha_vel[1] *= - 1
            self.bolinha_vel[0] *= - 1
        elif colidiu and verifica == 'continua':
            self.bolinha_vel[1] *= - 1

        # Com isso, calcula as novas posições
        self.bolinha_pos[0] += self.bolinha_vel[0] * delta
        self.bolinha_pos[1] += self.bolinha_vel[1] * delta

       # Coloca limites nas paredes
        if self.bolinha_pos[0] - 10 < 50 or self.bolinha_pos[0] + 10 >= 450:
            self.bolinha_vel[0] *= - 1
    

    def alpha_fab(self):
        self.relogio = pygame.time.get_ticks() #em milissegundos
        subtracao = self.relogio - self.primeiro
        if subtracao >= 100:
            self.primeiro = self.relogio
            self.pontuacao += 1
            return True
        else:
            return False
    
    def tempo_coins(self):
        self.relogio_coins = pygame.time.get_ticks() #em milissegundos
        subtracao_coins = self.relogio_coins - self.primeiro_coins
        if subtracao_coins >= 100:
            self.primeiro_coins = self.relogio_coins
            return True
        return False

    def atualiza_estado(self):
        # Muda animação da moeda e verifica colisão
        if self.comecou:
            tempo = Jogo.tempo_coins(self)
            for c in self.all_coins:
                colidiu = c.colide(self.bolinha_pos)
                if colidiu:
                    self.all_coins.remove(c)
                    self.som_moeda.play()
            if tempo:
                self.all_coins.update()
            if self.pontuacao >= 100:
                for pedra in self.pedrinhas:
                    pedra.pedra_cai()
                    if pedra.colisao_bola(self.bolinha_pos):
                        self.pedrinhas.remove(pedra)
                        while self.indice_explosao < len(self.explosao):
                            pedra.desenha_explosao(self.window, self.explosao, self.indice_explosao)
                            self.indice_explosao += 1


                        self.atualiza_hscore()
                        del Plataformas.plataformas_anteriores[0]
                        fim = TelaFim(self.pontuacao)
                        fim.fim_loop()
                        return False

        # Verifica eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    self.comecou = True 
                    self.bolinha_tempo = pygame.time.get_ticks()     
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if self.comecou == True:
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
                    if self.comecou == True:
                        # Apenas após o mouse é solto que a linha pode ser desenhada
                        self.clicou =  True

                        self.coordenadas_final = pygame.mouse.get_pos()
                        self.pos_final_linha = [self.coordenadas_final[0], self.coordenadas_final[1]]
                        # Impedir (novamente) que a bolinha entre dentro da parede 
                        if self.pos_final_linha[0] < 50:
                            self.pos_final_linha[0] = 50
                        elif self.pos_final_linha[0] > 450:
                            self.pos_final_linha[0] = 450
                        elif self.pos_final_linha[1] > 650:
                            self.pos_final_linha[1] =  650
        if self.comecou:
            self.bola_quica()

        if self.bolinha_pos[1] - 10 > 700:
            self.atualiza_hscore()
            del Plataformas.plataformas_anteriores[0]
            fim = TelaFim(self.pontuacao)
            fim.fim_loop()
            return False
        return True
        
    def desenha(self):
        self.window.fill(AZUL_FUNDO)
        if self.caverna1_y >= - 300:
            self.window.blit(self.caverna, (- 500, self.caverna1_y))
            self.window.blit(self.caverna, (0, self.caverna2_y))

        elif self.caverna2_y >= - 300:
           self.window.blit(self.caverna, (0, self.caverna2_y))
           self.window.blit(self.caverna, (- 500, self.caverna1_y))
        
        if self.caverna1_y >= 700:
            self.caverna1_y = - 1300
        if self.caverna2_y >= 700:
            self.caverna2_y = - 1300
        
        if self.bloco_vertical_y == 0:
            self.bloco_vertical_y = - 300
        # Desenha pedras paredes
        x = 0
        y = self.bloco_vertical_y

        while x <= self.tamanho_tela[0]:
            # BOTTOM
            self.window.blit(self.bloco_img, (x, self.bloco_horizontal_y)) 
            x += 50
        while y <= 700:
            # WALLS
            self.window.blit(self.bloco_img, (0, y))
            self.window.blit(self.bloco_img, (450, y))
            y += 50
        # A bola permanece parada até o jogador dar início
        # Desenha plataformas
        if self.clicou == True:
            Plataformas(self.pos_inicial_linha, self.pos_final_linha)
        Plataformas.verifica_linhas()
        Plataformas.desenha_plataforma(self.window)

        # A bola permanece parada até o jogador dar início
        if self.comecou:
            # Blita o score
            pontuacao = self.fonte.render(f'Score: {self.pontuacao}', self.fonte, AZUL_CLARINHO)
            self.window.blit(pontuacao, (60, 10))
            # Blita o cofrinho
            with open('moedas.txt', 'r') as moedas:
                money = moedas.read()
                cofrinho = self.fonte.render(f' {int(money)}', self.fonte, AZUL_CLARINHO)
            self.window.blit(cofrinho, (390, 10))
            moedinha = pygame.transform.scale(pygame.image.load('assets/coin1.png'), (150, 60))
            self.window.blit(moedinha, (380, 11))
            # Move os objetos na tela
            if self.alpha_fab():
                self.caverna1_y += 5
                self.caverna2_y += 5
                self.bloco_horizontal_y += 5
                self.bloco_vertical_y += 5
                self.pos_inicial_linha[1] += 5
                self.pos_final_linha[1] += 5
        else:
            inicio = self.fonte.render('Aperte espaco para comecar', self.fonte, AZUL_CLARINHO)
            self.window.blit(inicio, (78, 30))
        
        if self.pontuacao >= 100:
            if self.pontuacao >= self.intervalo:
                self.cria_pedras()
                self.intervalo += 30
            for pedra in self.pedrinhas:
                self.window.blit(self.pedrinha, (pedra.coordenadas[0], pedra.coordenadas[1]))
 
        pygame.draw.circle(self.window, AZUL_BOLA, self.bolinha_pos, 10)
        # Desenha coins
        self.all_coins.draw(self.window)

        pygame.display.update()

    def game_loop(self):
        game = True
        while game:
            game = self.atualiza_estado()
            if game:
                self.desenha()



class TelaFim:
    def __init__(self, pontuacao):
        pygame.init()
        #pygame.mixer.init()
        self.tamanho_tela = [500, 700]
        self.window = pygame.display.set_mode(self.tamanho_tela)
        self.imagem_inicio = pygame.image.load('assets/casa_caiu.jpeg')
        self.imagem_inicio = pygame.transform.scale(self.imagem_inicio, (700, 700))
        
        self.fonte = pygame.font.Font('assets/Emulogic-zrEw.ttf', 20)
        self.fontemenor = pygame.font.Font('assets/Emulogic-zrEw.ttf', 11)
        self.fontemedia = pygame.font.Font('assets/Emulogic-zrEw.ttf', 15)
        self.inicio = TelaInicio()

        self.score = pontuacao
    

    def atualiza_fim(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r :
                    self.inicio.inicio_loop()
                    return False
        return True

    def desenha_tela_fim(self):
        self.window.blit(self.imagem_inicio, (- 87, 0))
        pygame.draw.rect(self.window, BEGE, (140, 100, 220, 100))

        
        game_over = self.fonte.render('A alma se perdeu...', self.fonte, BEGE)
        self.window.blit(game_over, (50, 500))

        restart = self.fontemedia.render('Pressione R para recomecar', self.fontemedia, LARANJA)
        self.window.blit(restart, (50, 660))

        score =  self.fonte.render(f'Score:{self.score}', self.fontemedia, MARROM_AVERMELHADO)
        self.window.blit(score, (150, 120))

        with open('highestscore.txt', 'r') as hscore:
                highest_score = hscore.read()
                maior_score = self.fontemenor.render(f'Highest Score:{int(highest_score)}', self.fontemenor, MARROM_AVERMELHADO)
        self.window.blit(maior_score, (155, 170))
        pygame.display.update()

    def fim_loop(self): # O loop para a tela de fim
       fim = True
       while fim:
            fim = self.atualiza_fim()
            if fim:
                self.desenha_tela_fim()



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

        self.musica = pygame.mixer.music.load('assets/cave music.mp3')
        pygame.mixer.music.play()

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
         