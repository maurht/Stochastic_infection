import numpy as np
import random as rnd
from indv_class import Indv
from math import sqrt


class Population:

    def __init__(self, N, I0, box, step_size = 0.05, r_infec = 0.05, p_infec = 0.1, p_market = 0.002, tmax_infec = 100
                 ,tmax_market = 4, rnd_starting_infection_time = False, market = False):

        # Simulation parameters

        self.N = N           # Tamaño de poblacion
        self.I0 = I0            # Infectados iniciales

        # Variables for Indv class
        self.box = box
        self.step_size = step_size  # Tamaño del paso
        self.r_infec = r_infec  # Radio de infeccion
        self.p_infec = p_infec  # Probabilidad de infeccion
        self.p_market = p_market  # Probabilidad de ir al mercado

        self.tmax_infec = tmax_infec  # Tiempo de duracion de la infeccion
        self.tmax_market = tmax_market

        # Data record
        self.Su = np.zeros(0, dtype=int)  # Desarrollo de poblacion suceptible a lo largo del tiempo
        self.In = np.zeros(0, dtype=int)  # Desarrollo de poblacion infectada a lo largo del tiempo
        self.Re = np.zeros(0, dtype=int)

        # Special features
        self.rnd_starting_infection_time = rnd_starting_infection_time
        self.market = market

        # setup
        self.pop = self.populate()

    def populate(self):

        pop = [Indv(step_size = self.step_size,
                    r_infec = self.r_infec,
                    p_infec = self.r_infec,
                    p_market = self.p_market,
                    box = self.box,
                    tmax_infec = self.tmax_infec,
                    tmax_market = self.tmax_market) for i in range(self.N)]  # Creacion de la poblacion

        # Asignacion de estatus I a I_O personas
        count = 0
        for person in pop:
            if self.rnd_starting_infection_time:
                if count < self.I0:
                    person.t = rnd.randint(0, self.tmax_infec)
                    person.est = 'I'
                    count += 1
            else:
                if count < self.I0:
                    person.est = 'I'
                    count += 1

        return pop

    # one instance of time

    def be(self):
        self.Su = np.append(self.Su, 0)
        self.In = np.append(self.In, 0)

        for person in self.pop:
            if self.market:
                person.walk_market()
            else:
                person.rand_walk()
            if person.est == 'S':
                for other_person in self.pop:
                    if person.est != 'S':
                        break
                    elif other_person.est == 'I' and rnd.random() <= self.p_infec and sqrt(
                            (person.x - other_person.x) ** 2 + (person.y - other_person.y) ** 2) <= self.r_infec:
                        person.est = 'I'
            if person.est == 'S':
                self.Su[-1] += 1
            elif person.est == 'I':
                self.In[-1] += 1
        self.Re = np.append(self.Re, self.N - self.Su[-1] - self.In[-1])
