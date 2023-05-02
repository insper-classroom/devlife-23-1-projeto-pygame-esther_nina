import pygame
import math

class Plataformas:
    plataformas_anteriores = []

    def __init__(self, coordenada_inicio, coordenada_final):
        self.cor = (255, 255, 255)
        # Criador das nossas linhas, nas quais a bolinha pulará em
        self.coordenadas_comeco = coordenada_inicio
        self.coordenadas_final = coordenada_final
        self.vertices =  (coordenada_inicio, coordenada_final, (coordenada_final[0], coordenada_final[1] - 5), (coordenada_inicio[0], coordenada_inicio[1] - 5))
        Plataformas.plataformas_anteriores.append(self)

    def desenha_plataforma(window):
        for plataforma in Plataformas.plataformas_anteriores:
            pygame.draw.polygon(window, plataforma.cor, (plataforma.coordenadas_comeco, plataforma.coordenadas_final, (plataforma.coordenadas_final[0], plataforma.coordenadas_final[1] - 5), (plataforma.coordenadas_comeco[0], plataforma.coordenadas_comeco[1] - 5)))

    def colidiu(bola_pos):
        for p in Plataformas.plataformas_anteriores:
            # Coordenadas dos vértices da plataforma
                vertices = p.vertices
                
                # Verifica colisão com cada lado da plataforma
                for i in range(len(vertices)):
                    p1 = vertices[i]
                    p2 = vertices[(i+1) % len(vertices)]
                    
                    # Verifica se a bola está dentro dos limites do segmento de reta
                    if (p1[0] <= bola_pos[0] <= p2[0] or p2[0] <= bola_pos[0] <= p1[0]) and \
                    (p1[1] <= bola_pos[1] <= p2[1] or p2[1] <= bola_pos[1] <= p1[1]):
                        
                        # Cálculo da equação da reta que contém o segmento de reta
                        a = p1[1] - p2[1]
                        b = p2[0] - p1[0]
                        c = p1[0]*p2[1] - p2[0]*p1[1]
                        
                        # Distância da bola até a reta que contém o segmento de reta
                        dist = abs(a * bola_pos[0] + b * bola_pos[1] + c) / math.sqrt(a ** 2 + b ** 2)
                        
                        # Se a bola está dentro do raio da plataforma, houve colisão
                        if dist <= 5:
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
            if cateto_adjacente == 0:
                cateto_adjacente = 0.0000000000000001
            tangente = cateto_oposto / cateto_adjacente
            angulo_rad = math.atan(tangente)
            angulo_grau = math.degrees(angulo_rad)
            angulo_linha = 180 - (angulo_grau + 90)

            if angulo_linha > 70:
                return 'flip'
            
            elif angulo_linha > 45 and angulo_linha < 70:
                if vel_bola[0] > 0:
                    return 'flip'
                else:
                    return 'continua'
            elif angulo_linha < 45 and angulo_linha > 20:
                if vel_bola[0] > 0:
                    return 'continua'
                else:
                    return 'flip'
            else:
                return 'continua'
               