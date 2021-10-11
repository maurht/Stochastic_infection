import numpy as np
import random as rnd
from indv_class import Indv
from tqdm import tqdm
from math import sqrt
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from pandas import DataFrame
import plotly.express as px



def color_f(state):
    if state == 'S':
        return 0
    elif state == 'I':
        return 10
    else:
        return 5


class Population:

    def __init__(self, N, I0, box, step_size=0.05, r_infec=0.05, p_infec=0.1, infection_time=100, p_market=0.002
                 , tmax_market=4, incubation_time=25, rnd_starting_infection_time=False, market=False):

        # Simulation parameters

        self.N = N  # Tamaño de poblacion
        self.I0 = I0  # Infectados iniciales

        # Variables for Indv class
        self.box = box
        self.step_size = step_size  # Tamaño del paso
        self.r_infec = r_infec  # Radio de infeccion
        self.p_infec = p_infec  # Probabilidad de infeccion
        self.p_market = p_market  # Probabilidad de ir al mercado

        self.incubation_time = incubation_time
        self.infection_time = infection_time  # Tiempo de duracion de la infeccion
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

        pop = [Indv(step_size=self.step_size,
                    r_infec=self.r_infec,
                    p_infec=self.r_infec,
                    p_market=self.p_market,
                    box=self.box,
                    infection_time=self.infection_time,
                    tmax_market=self.tmax_market,
                    incubation_time=self.incubation_time) for i in range(self.N)]  # Creacion de la poblacion

        # Asignacion de estatus I a I_O personas
        count = 0
        for person in pop:
            if self.rnd_starting_infection_time:
                if count < self.I0:
                    person.t = rnd.randint(0, self.i)
                    person.est = 'I'
                    person.t = self.incubation_time
                    count += 1
            else:
                if count < self.I0:
                    person.est = 'I'
                    person.t = self.incubation_time
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
                    elif other_person.est == 'I' and other_person.t > self.incubation_time and rnd.random() <= self.p_infec and sqrt(
                            (person.x - other_person.x) ** 2 + (person.y - other_person.y) ** 2) <= self.r_infec:
                        person.est = 'I'
            if person.est == 'S':
                self.Su[-1] += 1
            elif person.est == 'I':
                self.In[-1] += 1
        self.Re = np.append(self.Re, self.N - self.Su[-1] - self.In[-1])

    def run(self, run_time):
        for _ in tqdm(range(run_time)):
            self.be()
            if self.In[-1] == 0:
                print('Early stopping. The number of infected dropped to 0.')
                break

    def infection_status(self):
        infection_count = sum([1 for person in self.pop if person.est == 'I'])
        print('Porcentaje de infeccion: ' + str((infection_count / self.N) * 100))

    def scatter_animation(self, interval):
        fig = plt.figure()
        ax = plt.axes(xlim=(-self.box, self.box), ylim=(-self.box, self.box))
        ax.legend(['S','I','R'], bbox_to_anchor=(1.1, 1.05))
        scat = ax.scatter([], [])

        def update(i):
            scat.set_offsets(np.array([[person.x, person.y] for person in self.pop]))
            scat.set_array(np.array([color_f(person.est) for person in self.pop]))
            self.be()

        amin = FuncAnimation(fig, func=update, interval=interval)
        plt.show()

    def final_state(self):
        from seaborn import scatterplot
        P = DataFrame()
        P[['X', 'Y', 'State']] = [[person.x, person.y, person.est] for person in self.pop]

        scatterplot(data=P, x='X', y='Y', hue='State', palette='magma')
        plt.legend(bbox_to_anchor=(1.05, 0.5))
        plt.xlim([-self.box, self.box])
        plt.ylim([-self.box, self.box])
        plt.tight_layout()
        plt.show()

    def infection_timeline(self):
        lines = DataFrame()
        lines['Susceptible'] = self.Su
        lines['Infected'] = self.In
        lines['Removed'] = self.Re

        fig = px.line(lines)
        fig.show()
