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
        # Calcular a posição do jogador após pingar
        self.bolinha_pos = [240, 50]
        self.bolinha_vel = [100, 150]
        self.bolinha_tempo = 0
        # Loading de imagens e sons
        self.bloco_img =  pygame.transform.scale(pygame.image.load('bloquinho.png'), (50,50))
        self.pedrinha_img = pygame.transform.scale(pygame.image.load('pedrinha.png'),(40,40))    
        self.window = pygame.display.set_mode(self.tamanho_tela)

        # jog = Jogador()
        # g.add(jog)
        # g.update()

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
        self.bolinha_vel[1] += 400 * delta

        # Com isso, calcula as novas posições
        self.bolinha_pos[0] += self.bolinha_vel[0] * delta
        self.bolinha_pos[1] += self.bolinha_vel[1] * delta

       # Coloca limites nas paredes
        if self.bolinha_pos[0] - 10 < 50 or self.bolinha_pos[0] + 10 >= 450:
            self.bolinha_vel[0] *= - 1
        if self.bolinha_pos[1] - 10 > 650:
            self.bolinha_vel[1] *= - 1 

    def atualiza_estado(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
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
        pygame.draw.circle(self.window, (255, 255, 255), self.bolinha_pos, 10)
        pygame.display.update()

    def game_loop(self):
        game = True
        while game:
            game = self.atualiza_estado()
            if game:
                self.desenha()
            

        return
    
        
