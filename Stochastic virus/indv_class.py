import random as rnd
from math import sin, cos, pi
from numpy import sign


# Definicion de un individuo

class Indv:

    def __init__(self, step_size: float, p_market: float, box: float,
                 infection_time: float, tmax_market: int, incubation_time: int, market_size: float):
        self.box = box  # Tamaño de la region box x box

        # Coordenadas iniciales
        self.x = self.box * (2 * rnd.random() - 1)
        self.y = self.box * (2 * rnd.random() - 1)
        self.theta = 2 * pi * rnd.random()

        self.step_size = step_size  # Tamaño del paso
        self.p_market = p_market  # Probabilidad de ir al mercado
        self.tmax_market = tmax_market  # Tiempo en el mercado(?)
        self.market_size = market_size

        self.infection_incubation_time = incubation_time + infection_time

        self.est = 'S'  # Estado S-> suceptible, I-> infectado, R-> removido
        self.xcp, self.ycp = 0, 0  # Coordenadas auxiliares
        self.box_save = box  # Valor de la caja auxiliar
        self.t = 0
        self.t_market = 0  # Tiempo en el mercado

    def rand_bounce(self):  # Caminata aleatoria
        if self.est == 'I':
            self.t += 1  # Contador de tiempo infectado
        if self.t == self.infection_incubation_time:
            self.est = 'R'  # El individuo se cura
        random_theta = rnd.random() * pi * 2
        self.x += self.step_size * cos(random_theta)
        self.y += self.step_size * sin(random_theta)
        if abs(self.x) >= self.box:
            self.x += -2 * self.step_size * cos(random_theta)
        if abs(self.y) >= self.box:
            self.y += -2 * self.step_size * sin(random_theta)

    def go_to_market(self):

        if self.t_market == 0 and rnd.random() <= self.p_market:
            self.xcp = self.x
            self.ycp = self.y
            self.box = self.market_size

            self.x = self.market_size * (2 * rnd.random() - 1)
            self.y = self.market_size * (2 * rnd.random() - 1)

            self.t_market += 1
        elif self.t_market < self.tmax_market and self.t_market != 0:
            self.t_market += 1
        elif self.t_market == self.tmax_market:
            self.x = self.xcp
            self.y = self.ycp
            self.box = self.box_save
            self.t_market = 0

    def linear_bounce(self):
        if self.est == 'I':
            self.t += 1  # Contador de tiempo infectado
        if self.t == self.infection_incubation_time:
            self.est = 'R'  # El individuo se cura
        self.x += self.step_size * cos(self.theta)
        self.y += self.step_size * sin(self.theta)
        if abs(self.x) >= self.box:
            self.theta = pi - self.theta
            self.x += self.step_size * cos(self.theta)
            self.y += self.step_size * sin(self.theta)
        if abs(self.y) >= self.box:
            self.theta = - self.theta
            self.x += self.step_size * cos(self.theta)
            self.y += self.step_size * sin(self.theta)

    def rand_toroid(self):
        if self.est == 'I':
            self.t += 1  # Contador de tiempo infectado
        if self.t == self.infection_incubation_time:
            self.est = 'R'  # El individuo se cura
        random_theta = rnd.random() * pi * 2
        self.x += self.step_size * cos(random_theta)
        self.y += self.step_size * sin(random_theta)
        if abs(self.x) >= self.box:
            self.x += - 2 * sign(self.x) * self.box
        if abs(self.y) >= self.box:
            self.y += - 2 * sign(self.y) * self.box

    def linear_toroid(self):
        if self.est == 'I':
            self.t += 1  # Contador de tiempo infectado
        if self.t == self.infection_incubation_time:
            self.est = 'R'  # El individuo se cura
        self.x += self.step_size * cos(self.theta)
        self.y += self.step_size * sin(self.theta)
        if abs(self.x) >= self.box:
            self.x += - 2 * sign(self.x) * self.box
        if abs(self.y) >= self.box:
            self.y += - 2 * sign(self.y) * self.box

    def none(self):
        if self.est == 'I':
            self.t += 1  # Contador de tiempo infectado
        if self.t == self.infection_incubation_time:
            self.est = 'R'  # El individuo se cura
