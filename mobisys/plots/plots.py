#!/home/msj/miniconda3/bin/python3



import matplotlib as mpl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
import matplotlib.lines as mlines


from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#print('Setting MPL defaults')
#https://matplotlib.org/users/customizing.html
colors = ['#3778bf','#7bb274','#825f87',
          '#feb308','#59656d','#984447',
          '#e17701','#add9f4','#1b264f',
          '#4b296b','#380835','#607c8e',
          '#ca6641']
# colors = ['#3778bf','#7bb274',,'#feb308',
#               '#59656d']

mpl.rcParams['axes.prop_cycle'] = mpl.cycler('color',colors)
bg_color = '#ffffff'
fg_color = colors[1]
fg_color2 = colors[0]
fg_color3 = colors[3]
fg_color4 = colors[2]
ax_color = colors[4]

mpl.rcParams['font.family'] = 'sans-serif'
#mpl.rcParams['font.sans-serif'] = ['Helvetica']
plt.rc('text', color=ax_color)
#plt.rc('axes',titleweight='bold')

mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.edgecolor'] = ax_color
mpl.rcParams['ytick.color'] = ax_color
mpl.rcParams['xtick.color'] = ax_color
mpl.rcParams['axes.labelcolor'] = ax_color
mpl.rcParams['axes.labelsize'] = 13
mpl.rcParams["figure.figsize"] = (7,5)




    
