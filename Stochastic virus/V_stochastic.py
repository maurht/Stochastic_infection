import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import plotly.express as px
from population_class import Population

sns.set_theme(style='white')

model = Population(N=500,
                   I0=10,
                   box=1.5,
                   tmax_infec=100)

tmax = 1000
for step in tqdm(range(tmax)):
    model.be()
    if model.In[-1] == 0:
        print('Early stopping. The number of infected dropped to 0.')
        break

P = pd.DataFrame()
P['X'] = [person.x for person in model.pop]
P['Y'] = [person.y for person in model.pop]
P['State'] = [person.est for person in model.pop]

plt.figure(figsize=(12, 8))
sns.scatterplot(data=P, x='X', y='Y', hue='State', palette='magma')
plt.legend(bbox_to_anchor=(1.05, 0.5))
plt.xlim([-model.box, model.box])
plt.ylim([-model.box, model.box])
plt.show()

lines = pd.DataFrame()
lines['Suceptible'] = model.Su
lines['Infected'] = model.In
lines['Removed'] = model.Re

fig = px.line(lines)
fig.show()

print('Porcentaje de infeccion: ' + str((P.groupby('State').count()['X']['R'] / model.N) * 100))
