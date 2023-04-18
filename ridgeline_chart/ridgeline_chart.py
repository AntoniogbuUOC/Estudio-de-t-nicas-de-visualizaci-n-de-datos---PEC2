import pandas as pd
import matplotlib.pyplot as plt
from joypy import joyplot

df = pd.read_csv('city_temperature.csv')

df = df[df['Year']== 2019].reset_index(drop=True)

df = df.drop(columns=['Region','State','City','Month','Day','Year'])
lista_country = ['Egypt','China','Spain','France','New Zealand','Nigeria','Russia','Hungary']

df = df[df['Country'].isin(lista_country)].reset_index(drop=True)
  
plt.figure()

joyplot(
    data=df[['Country', 'AvgTemperature']], 
    by='Country',
    figsize=(12,8)
)
plt.title('Ridgeline Chart de las Temperaturas (ºF) en varios países en 2019', fontsize=20)
plt.xlabel('Temperaturas en ºF')
plt.ylabel('Country')
plt.show()
