from population_class import Population
# import matplotlib.pyplot as plt


model = Population(N=1000,
                   I0=1,
                   box=2,
                   market_size=0.07,
                   infection_time=100,
                   step_size=0.015,
                   r_infec=0.07,
                   p_infec=0.3,
                   incubation_time=0,
                   walk_type='linear_bounce_walk',
                   p_market=0.002,
                   tmax_market=10,
                   rnd_starting_infection_time=False)



model.run(run_time=300)

#model.scatter_animation(interval=5, alpha=0.6, gradient=True)

model.final_state(gradient=True)

#model.infection_timeline()

#model.infection_status()
