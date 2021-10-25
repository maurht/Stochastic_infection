import numpy as np
import random as rnd
from indv_class import Indv
from tqdm import tqdm
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from pandas import DataFrame


def color_f(state):
    if state == 'S':
        return 0
    elif state == 'I':
        return 1
    else:
        return 0.5


class Population:

    def __init__(self, N: int, I0: int, box: float, market_size: float, step_size=0.05, r_infec=0.05, p_infec=0.1,
                 infection_time=100,
                 p_market=0.002, tmax_market=4, incubation_time=25, walk_type='rand_bounce_walk',
                 rnd_starting_infection_time=False):

        # Simulation parameters

        self.N = N  # Tamaño de poblacion
        self.I0 = I0  # Infectados iniciales

        # Variables for Indv class
        self.box = box  # Tamaño del dominio
        self.step_size = step_size  # Tamaño del paso
        self.r_infec = r_infec  # Radio de infeccion
        self.p_infec = p_infec  # Probabilidad de infeccion
        self.p_market = p_market  # Probabilidad de ir al mercado
        self.market_size = market_size

        self.incubation_time = incubation_time  # tiempo de incubacion
        self.infection_time = infection_time  # Tiempo de duracion de la infeccion
        self.tmax_market = tmax_market  # tiempo en el mercado

        # Status SIR
        self.Su = np.zeros(0, dtype=int)  # Desarrollo de poblacion suceptible a lo largo del tiempo
        self.In = np.zeros(0, dtype=int)  # Desarrollo de poblacion infectada a lo largo del tiempo
        self.Re = np.zeros(0, dtype=int)

        # Opciones especiales
        self.rnd_starting_infection_time = rnd_starting_infection_time
        self.walk_type = walk_type

        # setup
        self.pop = self.populate

    @property
    def populate(self):
        # Creacion de la poblacion
        pop = [Indv(step_size=self.step_size,
                    p_market=self.p_market,
                    box=self.box,
                    infection_time=self.infection_time,
                    tmax_market=self.tmax_market,
                    incubation_time=self.incubation_time,
                    walk_type=self.walk_type,
                    market_size=self.market_size) for i in range(self.N)]

        # Asignacion de estatus I a I_O personas
        count = 0
        for person in pop:
            if self.rnd_starting_infection_time:
                if count < self.I0:
                    person.t = rnd.randint(0, self.infection_time)
                    person.est = 'I'
                    person.t = self.incubation_time
                    count += 1
            else:
                if count < self.I0:
                    person.est = 'I'
                    person.t = self.incubation_time
                    count += 1

        return pop

    # una instancia de tiempo

    def be(self):
        # Añdimos un espacio a los arrays del timeline SIR. No necesitamos calcular Re por ahora, ya que Si+Re+Su=N
        self.Su = np.append(self.Su, 0)
        self.In = np.append(self.In, 0)

        # tipo de caminata elegido
        for person in self.pop:
            person.walk()
            ''' Proceso de infeccion. Por pasos: checamos si la persona es suceptible, luego tomamos a todos los
            infectados que se mantienen al principio de self.pop por el .sort() que se usa cada vez que hay un
            infectado, checamos si esa persona esta infectada (esto se hace en el caso de que el numero de infectados
            baje a cero. Si esta condicion no se usa un individuo en estado Re puede infectar individuos), checamos
            si el tiempo de incubacion se ha cumplido, si el caso entra en la probabilidad de infeccion y si la
            persona esta dentro del radio de infeccion. Si las condiciones se cumplen, el estatus del individuo se
            cambia, se ordena pop y se corta el ciclo'''
            if person.est == 'S':
                for infected in self.pop[:self.In[-1] + 1]:
                    if infected.est == 'I' and infected.t > self.incubation_time and rnd.random() <= self.p_infec and (
                            (person.x - infected.x) ** 2 + (person.y - infected.y) ** 2) <= self.r_infec ** 2:
                        person.est = 'I'
                        self.pop.sort(key=lambda x: x.est)
                        break

            if person.est == 'S':
                self.Su[-1] += 1
            elif person.est == 'I':
                self.In[-1] += 1
        self.Re = np.append(self.Re, self.N - self.Su[-1] - self.In[-1])

    def run(self, run_time: int):
        for _ in tqdm(range(run_time)):
            self.be()
            if self.In[-1] == 0:
                print('Early stopping. The number of infected dropped to 0.')
                break

    def infection_status(self):
        infection_count = sum([1 for person in self.pop if person.est == 'I' or person.est == 'R'])
        print('Porcentaje de infeccion: ' + str((infection_count / self.N) * 100))

    def scatter_animation(self, interval: int, alpha: float, gradient=False):
        fig = plt.figure()
        ax = plt.axes(xlim=(-self.box, self.box), ylim=(-self.box, self.box))
        if gradient:
            scat = ax.scatter([self.box * 2, self.box * 3], [self.box * 2, self.box * 3], c=[0, self.infection_time],
                              alpha=0.5)
        else:
            scat = ax.scatter([], [], alpha=alpha)

        def update(_):
            scat.set_offsets(np.array([[person.x, person.y] for person in self.pop]))
            scat.set_array(np.array([person.t if gradient else color_f(person.est) for person in self.pop]))
            self.be()

        anim = FuncAnimation(fig, func=update, interval=interval)
        plt.tight_layout()
        plt.show()

    def final_state(self, gradient=False, palette='Spectral'):
        from seaborn import scatterplot
        p = DataFrame()
        if gradient:
            p[['X', 'Y', 'Infection time']] = [[person.x, person.y, person.t] for person in self.pop]
            scatterplot(data=p, x='X', y='Y', hue='Infection time', palette=palette)
        else:
            p[['X', 'Y', 'State']] = [[person.x, person.y, person.est] for person in self.pop]
            scatterplot(data=p, x='X', y='Y', hue='State', palette='magma')


        plt.legend(bbox_to_anchor=(1.05, 0.5))
        plt.xlim([-self.box, self.box])
        plt.ylim([-self.box, self.box])
        plt.tight_layout()
        plt.show()

    def infection_timeline(self):
        import plotly.express as px

        lines = DataFrame()
        lines['Susceptible'] = self.Su
        lines['Infected'] = self.In
        lines['Removed'] = self.Re

        fig = px.line(lines)
        fig.show()
