from population_class import Population

model = Population(N=500,
                   I0=3,
                   box=1,
                   infection_time=100,
                   step_size=0.012,
                   r_infec=0.07,
                   p_infec=0.3,
                   incubation_time=25,
                   market=False,
                   p_market=0.002,
                   tmax_market=2,
                   rnd_starting_infection_time=False)


model.scatter_animation(interval=30)

#model.run(run_time=200)

#model.final_state()

#model.infection_timeline()

#model.infection_status()
