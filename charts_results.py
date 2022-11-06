import pandas as pd
import numpy as np
import geopandas as gpd
import os
import matplotlib.pyplot as plt
import warnings

from constants import states, states_short


def jitterplot(df=None, v='peratus_keluar'):

    v_suffix = {'peratus_keluar': 'turnout',
                'rosak_vs_keseluruhan': 'undirosak'}
    v_title = {'peratus_keluar': 'Voter Turnout',
               'rosak_vs_keseluruhan': 'Undi Rosak Prevalence'}

    path_output = 'charts-general'
    if not os.path.isdir(path_output):
        os.makedirs(path_output)

    plt.rcParams.update({'font.size': 12,
                        'font.family': 'sans-serif',
                         'grid.linestyle': 'dashed',
                         'axes.edgecolor': 'lightgrey',
                         'figure.autolayout': True,
                         'figure.figsize': [8, 5]})  # width, height
    fig, ax = plt.subplots(1, 16, sharex=True, sharey=True)
    axes = ax.ravel()
    for i in range(16):
        tf = df[df.state == states[i]].copy()[[v]]
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
        axes[i].tick_params(axis=u'both', which=u'both', length=0)
    plt.suptitle(f'GE14: {v_title[v]} by State (each point = 1 seat)')
    plt.savefig(f'{path_output}/jitterplot_{v_suffix[v]}.png', pad_inches=0.2, dpi=400)


def scatterplot_margin_v_turnout(df=None):

    path_output = 'charts-general'
    if not os.path.isdir(path_output):
        os.makedirs(path_output)

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
    plt.savefig(f'{path_output}/scatterplot_majority_v_turnout.png', pad_inches=0.2, dpi=400)


# TODO: Add manual correction for overlapping annotations
def choropleth_gradient(df=None, plot_for=['Malaysia'], v='peratus_keluar'):

    v_suffix = {'peratus_keluar': 'turnout',
                'majoriti_peratus': 'majority',
                'rosak_vs_keseluruhan': 'undirosak'}
    v_title = {'peratus_keluar': 'Voter Turnout',
               'majoriti_peratus': 'Majority (% of votes)',
               'rosak_vs_keseluruhan': 'Undi Rosak (% of votes)'}
    cmaps = {'peratus_keluar': 'Blues',
             'majoriti_peratus': 'Greens',
             'rosak_vs_keseluruhan': 'Reds'}

    path_output = f'charts-{v_suffix[v]}'
    if not os.path.isdir(path_output):
        os.makedirs(path_output)

    for s in plot_for:
        print(s)
        geo = df.copy()
        title = ''
        suffix = ''
        if s != 'Malaysia':
            geo = geo[geo.state == s]
            title = f' in {s}'
            suffix = '_' + s.lower().replace(' ', '').replace('.', '')

        geo_s = geo.copy().dissolve(by='state')

        plt.rcParams.update({'font.size': 13,
                            'font.family': 'sans-serif',
                             'grid.linestyle': 'dotted',
                             'figure.figsize': [8, 8],
                             'figure.autolayout': True})
        fig, ax = plt.subplots()
        ax.axis('off')

        cmap = cmaps[v]
        lw = 1 if s != 'Malaysia' else 0.7
        vmin, vmax = geo[v].min(), geo[v].max()  # colours relative to specific range being plotted

        geo.plot(column=v, cmap=cmap, vmin=vmin, vmax=vmax, linewidth=0.07, edgecolor='black', ax=ax)
        geo_s.plot(edgecolor='black', linewidth=lw, facecolor='none', ax=ax)
        if s != 'Malaysia':
            bbox_props = dict(boxstyle='round', fc="w", ec='0.5', alpha=0.5)
            geo.apply(lambda x: ax.annotate(text=x['seat'][6:],
                                            xy=x.geometry.centroid.coords[0],
                                            ha='center', va='center',
                                            size=9, bbox=bbox_props,
                                            wrap=True), axis=1)
        cbar_ax = fig.add_axes([0.1, 0.00, 0.8, 0.01])
        cbar = fig.colorbar(
            plt.cm.ScalarMappable(
                cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax)
            ), cax=cbar_ax, orientation="horizontal")
        plt.suptitle(f'GE14: {v_title[v]} by Parliament{title}')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            plt.savefig(f'{path_output}/choropleth_{v_suffix[v]}{suffix}.png',
                        bbox_inches='tight', pad_inches=0.2, dpi=400)
        plt.close()


def choropleth_binary(tf=None, plot_for=['Malaysia'], v='tidakhadir_vs_majoriti', threshold=100, positive=0):

    tf.loc[tf[v] < threshold, v] = 0
    tf.loc[tf[v] > 0, v] = 1

    for s in plot_for:
        print(s)
        geo = tf.copy()
        title = ''
        suffix = ''
        if s != 'Malaysia':
            geo = geo[geo.state == s]
            title = f' in {s}'
            suffix = '_' + s.lower().replace(' ', '').replace('.', '')

        v_suffix = {'tidakhadir_vs_majoriti': 'absentimpact',
                    'rosak_vs_majoriti': 'rosakimpact'}
        v_title = {'tidakhadir_vs_majoriti': f'Non-Voters vs Majority{title}\n\nRed Seats: Non-Voters > Majority (could have swung result)',
                   'rosak_vs_majoriti': f'Undi-Rosak vs Majority{title}\n\nRed Seats: Undi Rosak > Majority (could have swung result)'}

        path_output = f'charts-{v_suffix[v]}'
        if not os.path.isdir(path_output):
            os.makedirs(path_output)

        geo_s = geo.copy().dissolve(by='state')

        plt.rcParams.update({'font.size': 13,
                            'font.family': 'sans-serif',
                             'grid.linestyle': 'dotted',
                             'figure.figsize': [8, 8],
                             'figure.autolayout': True})
        fig, ax = plt.subplots()
        ax.axis('off')

        cmap = 'Reds' if positive == 0 else 'Greens'
        vmin, vmax = 0, 1.5
        lw = 1 if s != 'Malaysia' else 0.7

        geo.plot(column=v, cmap=cmap, vmin=vmin, vmax=vmax, linewidth=0.07, edgecolor='black', ax=ax)
        geo_s.plot(edgecolor='black', linewidth=lw, facecolor='none', ax=ax)
        if s != 'Malaysia':
            bbox_props = dict(boxstyle='round', fc="w", ec='0.5', alpha=0.5)
            geo.apply(lambda x: ax.annotate(text=x['seat'][6:],
                                            xy=x.geometry.centroid.coords[0],
                                            ha='center', va='top',
                                            size=9, bbox=bbox_props,
                                            wrap=True), axis=1)
        plt.suptitle(f'GE14: {v_title[v]}')
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            plt.savefig(f'{path_output}/choropleth_{v_suffix[v]}{suffix}.png',
                        bbox_inches='tight', pad_inches=0.2, dpi=400)
        plt.close()


# ---------- Chart functions defined above, call everything below ----------


# Load election results (once), then plot charts that depend only on the election results
df = pd.read_csv('data/results_parlimen_ge14.csv')
df['majoriti_peratus'] = df.majoriti/df.undi_keluar_peti * 100
scatterplot_margin_v_turnout(df=df)

for v in ['rosak_vs_keseluruhan', 'peratus_keluar']:
    jitterplot(df=df, v=v)

# Load basemaps(once only); relatively large (37MB) because high-res (necessary for clean parlimen --> state dissolve)
geo_o = gpd.read_file('maps/parlimen.geojson')
geo_o.loc[~geo_o.code_state.isin([12, 13, 15]), 'geometry'] = geo_o.geometry.translate(9, 4.5)  # More compact Msia map
geo_o = pd.merge(geo_o, df,
                 left_on=['state', 'parlimen'],
                 right_on=['state', 'seat'], how='left')  # Merge with election results

for v in ['peratus_keluar', 'majoriti_peratus', 'rosak_vs_keseluruhan']:
    choropleth_gradient(df=geo_o, plot_for=['Malaysia'] + states, v=v)

for v in ['tidakhadir_vs_majoriti', 'rosak_vs_majoriti']:
    choropleth_binary(tf=geo_o, plot_for=['Malaysia'] + states, v=v)
