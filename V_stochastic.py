from population_class import Population
# import matplotlib.pyplot as plt


model = Population(N=30,
                   I0=1,
                   box=1,
                   market_size=0.08,
                   infection_time=200,
                   step_size=0.005,
                   r_infec=0.04,
                   p_infec=0.3,
                   incubation_time=25,
                   walk_type='linear_toroid',
                   market=True,
                   p_market=0.002,
                   tmax_market=200,
                   rnd_starting_infection_time=False)



#model.run(run_time=300)

model.scatter_animation(interval=5, alpha=1, gradient=True)

#model.final_state(gradient=True)

#model.infection_timeline()

#model.infection_status()


"""
from math import sin, cos

P_size = 1
time = 3000


def color_func(x):
    return (0.25 * (sin(x * 6.2831 / time) + 3), 0.7, 0.2)


model = Population(N=P_size,
                   I0=1,
                   box=1,
                   infection_time=100,
                   step_size=0.02,
                   r_infec=0.05,
                   p_infec=0.3,
                   incubation_time=15,
                   walk_type='rand_walk',
                   p_market=0.002,
                   tmax_market=2,
                   rnd_starting_infection_time=False)

cc = 1
for t in range(time):
    for person in model.pop:
        xn = person.x
        yn = person.y
        person.walk()
        plt.plot([xn, person.x], [yn, person.y], c=color_func(cc))
        cc += 1

plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.show()

"""