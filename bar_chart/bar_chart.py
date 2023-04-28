import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator

df = pd.read_csv('covid-data.csv')

lista_country = ['Portugal','China','Spain','Belgium','United Kingdom','Australia','Germany','France','Brazil']

df = df[df['location'].isin(lista_country)].reset_index(drop=True)
df = df.drop(columns=['new_cases','total_deaths','new_deaths','date'])

df_group = df.groupby(by=['location']).sum().reset_index(drop=False)

# Figure
fig, ax = plt.subplots(figsize=(13.33,7.5), dpi = 96)
bar1 = ax.bar(df_group['location'], df_group['total_cases'], width=0.6)

# Grid
ax.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
ax.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)

# X-label
ax.set_xlabel('', fontsize=12, labelpad=10) # No need for an axis label
ax.xaxis.set_label_position("bottom")
ax.xaxis.set_major_formatter(lambda s, i : f'{s:,.0f}')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.xaxis.set_tick_params(pad=2, labelbottom=True, bottom=True, labelsize=12, labelrotation=0)
ax.set_xticks(df_group['location'], lista_country) # Map integers numbers from the series to labels list

# Reformat y-axis
ax.set_ylabel('Número de casos de COVID-19', fontsize=12, labelpad=10)
ax.yaxis.set_label_position("left")
ax.yaxis.set_major_formatter(lambda s, i : f'{s:,.0f}')
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_tick_params(pad=2, labeltop=False, labelbottom=True, bottom=False, labelsize=12)

# Add label on top of each bar
ax.bar_label(bar1, labels=[f'{e:,.1f}' for e in df_group['total_cases']], padding=3, color='black', fontsize=8) 

# Remove the spines
ax.spines[['top','left','bottom']].set_visible(False)

# Make the left spine thicker
ax.spines['right'].set_linewidth(1.1)

# Add in red line and rectangle on top
ax.plot([0.12, .9], [.98, .98], transform=fig.transFigure, clip_on=False, color='#E3120B', linewidth=.6)
ax.add_patch(plt.Rectangle((0.12,.98), 0.04, -0.02, facecolor='#E3120B', transform=fig.transFigure, clip_on=False, linewidth = 0))

# Add in title and subtitle
ax.text(x=0.12, y=.93, s="Número de casos de COVID-19 en el primer semestre de 2020", transform=fig.transFigure, ha='left', fontsize=14, weight='bold', alpha=.8)
ax.text(x=0.12, y=.90, s="Se representan el número de casos de COVID-19 que hubo en diferentes países en el primer semestre de 2020", transform=fig.transFigure, ha='left', fontsize=12, alpha=.8)

# Set source text
ax.text(x=0.1, y=0.12, s="Fuente: Kaggle - COVID19 cases by country - https://www.kaggle.com/datasets/aj7amigo/covid19-cases-by-country?resource=download", transform=fig.transFigure, ha='left', fontsize=10, alpha=.7)

# Adjust the margins around the plot area
plt.subplots_adjust(left=None, bottom=0.2, right=None, top=0.85, wspace=None, hspace=None)

# Set a white background
fig.patch.set_facecolor('white')

# Colours - Choose the extreme colours of the colour map
colours = ["#2196f3", "#bbdefb"]

# Colormap - Build the colour maps
cmap = mpl.colors.LinearSegmentedColormap.from_list("colour_map", colours, N=256)
norm = mpl.colors.Normalize(df_group['total_cases'].min(), df_group['total_cases'].max()) # linearly normalizes data into the [0.0, 1.0] interval

# Plot bars
bar1 = ax.bar(df_group['location'], df_group['total_cases'], color=cmap(norm(df_group['total_cases'])), width=0.6, zorder=2)

# Find the average data point and split the series in 2
average = df_group['total_cases'].mean()
below_average = df_group[df_group['total_cases']<average]
above_average = df_group[df_group['total_cases']>=average]

# Colours - Choose the extreme colours of the colour map
colors_high = ["#ff5a5f", "#c81d25"] # Extreme colours of the high scale
colors_low = ["#2196f3","#bbdefb"] # Extreme colours of the low scale

# Colormap - Build the colour maps
cmap_low = mpl.colors.LinearSegmentedColormap.from_list("low_map", colors_low, N=256)
cmap_high = mpl.colors.LinearSegmentedColormap.from_list("high_map", colors_high, N=256)
norm_low = mpl.colors.Normalize(below_average['total_cases'].min(), average) # linearly normalizes data into the [0.0, 1.0] interval
norm_high = mpl.colors.Normalize(average, above_average['total_cases'].max())

# Plot bars and average (horizontal) line
bar1 = ax.bar(below_average['location'], below_average['total_cases'], color=cmap_low(norm_low(below_average['total_cases'])), width=0.6, label='Por debajo de la Media', zorder=2)
bar2 = ax.bar(above_average['location'], above_average['total_cases'], color=cmap_high(norm_high(above_average['total_cases'])), width=0.6, label='Por encima de la Media', zorder=2)
plt.axhline(y=average, color = 'grey', linewidth=3)

# Determine the y-limits of the plot
ymin, ymax = ax.get_ylim()
# Calculate a suitable y position for the text label
y_pos = average/ymax + 0.03
# Annotate the average line
ax.text(0.88, y_pos, f'Average = {average:.1f}', ha='right', va='center', transform=ax.transAxes, size=8, zorder=3)

# Add legend
ax.legend(loc="best", ncol=2, bbox_to_anchor=[1, 1.07], borderaxespad=0, frameon=False, fontsize=8)

