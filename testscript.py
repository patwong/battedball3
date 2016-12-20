import numpy as np
from scipy import stats
import bbp2
import pickle
import os
import plotly.plotly as plply
import plotly.graph_objs as go

pdict = {}
statdict = {}

pickled_pdict = "pdict.pickle"
pickled_statdict = "statdict.pickle"
if os.path.isfile(pickled_pdict) and os.path.isfile(pickled_statdict):
    print('pickled pdict and statdict found')
    with open(pickled_pdict, 'rb') as pdhandle:
        # need to declare pdict and statdict as global to access the global variable
        # otherwise will access a variable in the local scope
        # global pdict
        pdict = pickle.load(pdhandle)
    with open(pickled_statdict, 'rb') as sdhandle:
        # global statdict
        statdict = pickle.load(sdhandle)
# end if
plist1 = []
for player_name in pdict:
    player = pdict[player_name]
    plist1.append([player['name'], player['ba'], player['max_hit_speed'] - player['avg_hit_speed']])

parr = np.asarray(plist1)
parr_name = parr[:,0]
parr_x = np.asarray(parr[:,1], dtype='float64')
parr_y = np.asarray(parr[:,2], dtype='float64')


trace0 = go.Scatter(
    x = parr_x,
    y = parr_y,
    name = 'Above',
    mode = 'markers',
    marker = dict(
        size = 10,
        color = 'rgba(152, 0, 0, .8)',
        line = dict(
            width = 2,
            color = 'rgb(0, 0, 0)'
        )
    )
)

layout = dict(title = 'Styled Scatter',
              yaxis = dict(zeroline = False),
              xaxis = dict(zeroline = False)
             )


fig = dict(data=trace0, layout=layout)
plply.iplot(fig, filename='styled-scatter')


# exec(open('battedball.py').read())
# bbp2.brl_pa_vs_avg_hit_speed(pdict, statdict) # uses mpld3
