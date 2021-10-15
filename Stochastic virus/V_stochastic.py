from population_class import Population

model = Population(N=500,
                   I0=1,
                   box=1,
                   infection_time=100,
                   step_size=0.01,
                   r_infec=0.04,
                   p_infec=0.3,
                   incubation_time=15,
                   walk_type='bounce_walk',
                   p_market=0.002,
                   tmax_market=2,
                   rnd_starting_infection_time=False)


model.scatter_animation(interval=20)

#model.run(run_time=1000)

#model.final_state()

model.infection_timeline()

model.infection_status()
