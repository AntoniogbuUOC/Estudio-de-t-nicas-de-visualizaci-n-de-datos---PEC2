import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('covid-data.csv')

lista_country = ['Algeria','China','Spain','Belgium','United Kingdom','Australia','Germany','France']

df = df[df['location'].isin(lista_country)].reset_index(drop=True)
df = df.drop(columns=['new_cases','total_deaths','new_deaths'])

df_group = df.groupby(by=['date','location']).sum().reset_index(drop=False)
  
fig = plt.figure(figsize = (16, 8))
plt.bar(df_group['location'], df_group['total_cases'], color ='maroon',
        width = 0.4)
 
plt.xlabel("Número de casos de COVID-19 en diferentes países en el primer semestre de 2020")
plt.ylabel("Número de casos de COVID-19")
plt.title("Países")
plt.show()
