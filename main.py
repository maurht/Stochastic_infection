import numpy as np
import random as rnd
from math import pi
from math import cos
from math import sin
from math import sqrt
import time
import matplotlib.pyplot as plt

start = time.time() #contador de tiempo de ejecucion
N = 1000        # Tamaño de poblacion
box = 2         # Tamapo de la region box x box
I0 = 1          # Infectados iniciales
tmax = 500      # Tiempo limite
Su = np.zeros(tmax, dtype=int)  # Desarrollo de poblacion suceptible a lo largo del tiempo
In = np.zeros(tmax, dtype=int)  # Desarrollo de poblacion infectada a lo largo del tiempo
Re = np.zeros(tmax, dtype=int)  # Desarrollo de poblacion removida a lo largo del tiempo
t = np.linspace(0, tmax, tmax)  # Tiempo
tmax_infec = 100      #Tiempo de duracion de la infeccion
tmax_market = 4       #Tiempo en el mercado(?)


class Indv:         # Definicion de un individuo
    est = 'S'       # Estado S-> suceptible, I-> infectado, R-> removido
    x, y = 0, 0     # Coordenadas iniciales
    xcp, ycp = 0, 0      # Coordenadas auxiliares 
    t = 0    
    v = 0
    stepsize = 0.05    #Tamaño del paso
    r_infec = 0.05     #Radio de infeccion
    p_infec = 0.1      #Probabilidad de infeccion
    p_market = 0.002   #Probabilidad de ir al mercado
    t_market = 0       #Tiempo en el mercado

    def rand_walk(self):       #Caminata aleatoria
        if self.est == 'I':    
            self.t += 1        #Contador de tiempo infectado
        if self.t == tmax_infec:
            self.est = 'R'     #El individuo se cura
        theta = 2 * pi * rnd.random()    #Caminata dentro de un radio stepsize
        self.x += self.stepsize * cos(theta)
        self.y += self.stepsize * sin(theta)
        if abs(self.x) >= box:
            self.x += -2 * self.stepsize * cos(theta)
        if abs(self.y) >= box:
            self.y += -2 * self.stepsize * sin(theta)

    def virus(self):       #Definicion del virus
        if self.est == 'S':
            for iv in range(N):
                if self.est != 'S':
                    break
                elif pop[iv].est == 'I' and rnd.random() <= self.p_infec and sqrt(
                        (self.x - pop[iv].x) ** 2 + (self.y - pop[iv].y) ** 2) <= self.r_infec:
                    self.est = 'I'

    def walk_market(self):        #Caminata aleatoria pero existe la probabilidad de que el individuo visite un "mercado", que es un foco de infeccion
        if rnd.random() <= self.p_market and self.t_market == 0:
            self.xcp, self.ycp = self.x, self.y
            self.x, self.y = 0, 0
            self.t_market += 1
        elif self.t_market < tmax_market and self.t_market != 0:
            self.t_market += 1
        elif self.t_market == tmax_market:
            self.x, self.y = self.xcp, self.ycp
            self.t_market = 0
        else:
            if self.est == 'I':
                self.t += 1
            if self.t == tmax_infec:
                self.est = 'R'
            theta = 2 * pi * rnd.random()
            self.x += self.stepsize * cos(theta)
            self.y += self.stepsize * sin(theta)
            if abs(self.x) >= box:
                self.x += -2 * self.stepsize * cos(theta)
            if abs(self.y) >= box:
                self.y += -2 * self.stepsize * sin(theta)


pop = [Indv() for i in range(N)]   #Creacion de la poblacion

for i in range(N):              #Asignacion de las coordenadas de cada individuo
    pop[i].x, pop[i].y = box * (2 * rnd.random() - 1), box * (2 * rnd.random() - 1)
    if i < I0:                  #Asignacion de estatus I a I_O personas
        #       pop[i].t = rnd.randint(0, tmax_infec)
        pop[i].est = 'I'

for j1 in range(tmax):
    print(100 * j1 / tmax)
    for j2 in range(N):
        pop[j2].virus()
        pop[j2].rand_walk()
#        pop[j2].walk_market()
        if pop[j2].est == 'S':
            Su[j1] += 1
        elif pop[j2].est == 'I':
            In[j1] += 1
    Re = N - Su - In

end = time.time()    #fin de tiempo de ejecucion
print(end - start)

plt.figure(1)
for j3 in range(N):
    if pop[j3].est == 'S':  # Suceptibles
        plt.scatter(pop[j3].x, pop[j3].y, c='r', s=5)
    elif pop[j3].est == 'I':  # Infectados
        plt.scatter(pop[j3].x, pop[j3].y, c='g', s=5)
    else:  # Removidos
        plt.scatter(pop[j3].x, pop[j3].y, c='b', s=5)
plt.xlim([-box, box])
plt.ylim([-box, box])
plt.grid()

plt.figure(2)
plt.plot(t, Su, label='Susceptible', c='r')
plt.plot(t, In, label='Infected', c='g')
plt.plot(t, Re, label='Removed', c='b')
plt.grid()
plt.legend()

plt.show()
