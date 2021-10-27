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


