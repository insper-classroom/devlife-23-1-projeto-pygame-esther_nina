import pygame
import math

class Plataformas:
    plataformas_anteriores = []

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
                if vel_bola > 0:
                    return 'flip'
                else:
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