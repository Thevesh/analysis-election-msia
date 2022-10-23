import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

from constants import states, states_short


def jitterplot_turnout(df):
    plt.rcParams.update({'font.size': 12,
                        'font.family': 'sans-serif',
                         'grid.linestyle': 'dashed',
                         'axes.edgecolor': 'lightgrey',
                         'figure.autolayout': True,
                         'figure.figsize': [8, 5]})  # width, height
    fig, ax = plt.subplots(1, 16, sharex=True, sharey=True)
    axes = ax.ravel()
    for i in range(16):
        tf = df[df.state == states[i]].copy()[['peratus_keluar']]
        tf.columns = ['y']
        tf['x'] = 0
        tf.plot(kind='scatter', x='x', y='y', s=25, c='red', ax=axes[i])
        axes[i].yaxis.grid(True)
        axes[i].set_xlabel('')
        axes[i].set_ylabel('')
        axes[i].yaxis.set_visible(True)
        axes[i].xaxis.set_visible(False)
        axes[i].set_facecolor('white')
        axes[i].set_title(states_short[i], fontsize=12, fontfamily='sans-serif')
    plt.suptitle('GE14: Voter Turnout by State (each point = 1 seat)')
    plt.savefig('charts/jitterplot_turnout.png', pad_inches=0.2, dpi=400)


def scatterplot_margin_v_turnout(df):
    plt.rcParams.update({'font.size': 13,
                         'font.family': 'sans-serif',
                         'grid.linestyle': 'dashed',
                         'figure.autolayout': True,
                         'figure.figsize': [7, 7]})  # width, height
    fig, ax = plt.subplots()

    df.plot(kind='scatter', x='peratus_keluar', y='majoriti_peratus', s=50, c='red', alpha=0.5, ax=ax)
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    ax.set_axisbelow(True)
    ax.set_facecolor('white')
    ax.set_ylabel('Winning Margin')
    ax.set_xlabel('\nVoter Turnout')
    plt.xticks(np.arange(60, 100.01, 4))
    plt.yticks(np.arange(0, 100.01, 10))
    plt.title('Winning Margin (% of Votes) vs Voter Turnout (%)\n')
    plt.savefig('charts/scatterplot_majority_v_turnout.png', pad_inches=0.2, dpi=400)


# ---------- Chart functions defined above, call everything below ----------


# Load election results, then plot charts that depend only on the election results
df = pd.read_csv('results-parlimen/ge14.csv')
df['majoriti_peratus'] = df.majoriti/df.undi_keluar_peti * 100
jitterplot_turnout(df)
scatterplot_margin_v_turnout(df)

# Load basemaps (again, load once only)
# It is relatively large (37MB) because it is high-res
# We need high-res so that we get clean boundaries when we group parliament --> state
# Without a high-res basemap, there will be 'holes'

# geo_o = gpd.read_file('maps/parlimen.geojson')
# geo_o.loc[~geo_o.code_state.isin([12, 13, 15]), 'geometry'] = geo_o.geometry.translate(9, 4.5)  # More compact Msia map
# geo_o = pd.merge(geo_o, df, left_on=['state', 'parlimen'], right_on=['state', 'seat'], how='left')
