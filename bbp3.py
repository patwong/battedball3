import numpy as np
from scipy import stats
import plotly.plotly as plply
import plotly.graph_objs as go


# successor to bbp2 - uses plotly instead of mpld3
def plotter(pdict, xax, yax, ptitle, pfilename, lobf):
    plist_full = []
    plist1 = []
    falist = []
    # xax: (pdict val, x-axis title), yax: (pdict val, y-axis title)
    # ptitle: string
    # pfilename: filename
    # (Max BB Speed-Avg BB Speed) Versus Batting Average'
    xmax1 = 0.0
    xmaxname = ""
    xmin1 = pdict.popitem()[1][xax[0]]
    for player_name in pdict:
        player = pdict[player_name]
        if player[yax[0]] > 0:
            if player['freeagent']:
                falist.append([player['name'], player[xax[0]], player[yax[0]]])
            else:
                plist1.append([player['name'], player[xax[0]], player[yax[0]]])
            plist_full.append([player['name'], player[xax[0]], player[yax[0]]])
            if player[xax[0]] > xmax1:
                xmax1 = player[xax[0]]
                xmaxname = player['name']
            if player[xax[0]] < xmin1:
                xmin1 = player[xax[0]]
    # print(xmaxname, xmax1)    # checking who's the x-max value

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

    # full player list
    plf_arr = np.asarray(plist_full)
    plf_x = np.asarray(plf_arr[:,1], dtype='float64')
    plf_y = np.asarray(plf_arr[:,2], dtype='float64')

    # plotting the contracted players
    trace0 = go.Scatter(
        x = parr_x,
        y = parr_y,
        name = 'Contracted Players',
        text=parr_name,
        mode = 'markers'
    )

    # plotting the free agents
    trace1 = go.Scatter(
        x = faa_x,
        y = faa_y,
        name = 'Free Agents',
        text=faa_name,
        mode = 'markers'
    )

    # line of best fit code
    # isinstance(value, type) => boolean, i.e. isinstance(0.5, float) => True
    # use this to adjust the xmin/xmax values
    lr_array = stats.linregress(plf_x, plf_y)
    x_lobf = np.linspace(xmin1-1, xmax1+1, 2, dtype=int)
    y_lobf = lr_array.slope * x_lobf + lr_array.intercept
    trace2 = go.Scatter(
        x=x_lobf,
        y=y_lobf,
        name='Line of Best Fit',
        text=faa_name,
        mode='lines'
    )

    # put the correlation coefficient in the title
    rvstring = format(lr_array.rvalue, '.2f')
    ptitle = ptitle + " (rvalue: " + rvstring + ")"
    layout = dict(title = ptitle,
                  yaxis = dict(
                      zeroline = False,
                      title= yax[1]
                  ),
                  xaxis = dict(
                      zeroline = False,
                      title = xax[1]
                  )
                  )

    # trace0: contracted players, trace1: free agents, trace2: line of best fit
    # lobf: True - print out of line of best fit, False - don't
    if lobf:
        data = [trace0, trace1, trace2]
    else:
        data = [trace0, trace1]

    fig = dict(data=data, layout=layout)
    plply.plot(fig, filename=pfilename)
    print(str(lr_array.rvalue), str(lr_array.slope), str(lr_array.intercept))
# end plotter
