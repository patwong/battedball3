import numpy as np
from scipy import stats
import os
import plotly.plotly as plply
import plotly.graph_objs as go

# pdict = {}
# statdict = {}
#
# pickled_pdict = "Data/pdict.pickle"
# pickled_statdict = "Data/statdict.pickle"
# if os.path.isfile(pickled_pdict) and os.path.isfile(pickled_statdict):
#     print('pickled pdict and statdict found')
#     with open(pickled_pdict, 'rb') as pdhandle:
#         # need to declare pdict and statdict as global to access the global variable
#         # otherwise will access a variable in the local scope
#         # global pdict
#         pdict = pickle.load(pdhandle)
#     with open(pickled_statdict, 'rb') as sdhandle:
#         # global statdict
#         statdict = pickle.load(sdhandle)
# end if
plist1 = []
falist = []
for player_name in pdict:
    player = pdict[player_name]
    if player['freeagent']:
        falist.append([player['name'], player['ba'], player['max_hit_speed'] - player['avg_hit_speed']])
    else:
        plist1.append([player['name'], player['ba'], player['max_hit_speed'] - player['avg_hit_speed']])


def bbp3_plotter(xarray, yarray, xarray_fa, yarray_fa, ptitle, pxax, pyax):
    trace0 = go.Scatter(
        x = xarray,
        y = yarray,
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
                  yaxis = dict(
                      zeroline = False,
                      title= "Max Batted Ball Velocity - Average Batted Ball Velocity (MPH)"
                  ),
                  xaxis = dict(
                      zeroline = False,
                      title = "Batting Average"
                  )
                  )
    data = [trace0, trace1]

    fig = dict(data=data, layout=layout)
    plply.plot(fig, filename='maxbb_ahs_ba')


# exec(open('battedball.py').read())
# bbp2.brl_pa_vs_avg_hit_speed(pdict, statdict) # uses mpld3
