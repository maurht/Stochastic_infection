import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from population_class import Population


def color_f(state):
    if state == 'S':
        return 0
    elif state == 'I':
        return 10
    else:
        return 5


model = Population(N=900,
                   I0=2,
                   box=2,
                   tmax_infec=150,
                   step_size=0.01,
                   r_infec=0.07,
                   p_infec=0.3,
                   market=False,
                   tmax_market=2)

fig = plt.figure(figsize=(7, 7))
ax = plt.axes(xlim=(-model.box, model.box), ylim=(-model.box, model.box))
scat = ax.scatter([], [])


def update(i):
    P = np.array([[person.x, person.y] for person in model.pop])
    C = np.array([color_f(person.est) for person in model.pop])
    scat.set_offsets(P)
    scat.set_array(C)
    model.be()


amin = FuncAnimation(fig, func=update, interval=60)
plt.show()
