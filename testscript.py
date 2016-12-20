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
falist = []
for player_name in pdict:
    player = pdict[player_name]
    if player['freeagent']:
        falist.append([player['name'], player['ba'], player['max_hit_speed'] - player['avg_hit_speed']])
    else:
        plist1.append([player['name'], player['ba'], player['max_hit_speed'] - player['avg_hit_speed']])

# normal players
parr = np.asarray(plist1)
parr_name = parr[:,0]
parr_x = np.asarray(parr[:,1], dtype='float64')
parr_y = np.asarray(parr[:,2], dtype='float64')

# free agents
fa_arr = np.asarray(falist)
faa_name = fa_arr[:,0]
faa_x = np.asarray(fa_arr[:,1], dtype='float64')
faa_y = np.asarray(fa_arr[:,2], dtype='float64')

trace0 = go.Scatter(
    x = parr_x,
    y = parr_y,
    name = 'Contracted Players',
    text=parr_name,
    mode = 'markers'
    # marker = dict(
    #     size = 10,
    #     color = 'rgba(152, 0, 0, .8)',
    #     line = dict(
    #         width = 2,
    #         color = 'rgb(0, 0, 0)'
    #     )
    # )
)

trace1 = go.Scatter(
    x = faa_x,
    y = faa_y,
    name = 'Free Agents',
    text=faa_name,
    mode = 'markers'
)

layout = dict(title = '(Max BB Speed-Avg BB Speed) Versus Batting Average',
              yaxis = dict(zeroline = False),
              xaxis = dict(zeroline = False)
             )
data = [trace0, trace1]

fig = dict(data=data, layout=layout)
plply.plot(fig, filename='styled-scatter')


# exec(open('battedball.py').read())
# bbp2.brl_pa_vs_avg_hit_speed(pdict, statdict) # uses mpld3
