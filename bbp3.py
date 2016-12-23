import numpy as np
from scipy import stats
import plotly
import plotly.graph_objs as go


# successor to bbp2 - uses plotly instead of mpld3
def plotter(pdict, xax, yax, ptitle, pfilename, lobf,gtype):
    g_types = ["scatter", "hist"]
    if not(gtype in g_types):
        print('you provided a wrong graph type!')
        return
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
    plf_arr_name = plf_arr[:,0]
    plf_x = np.asarray(plf_arr[:,1], dtype='float64')
    plf_y = np.asarray(plf_arr[:,2], dtype='float64')

    if gtype == "scatter":
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
        if (xmax1 - xmin1) > 1:
            xmin1 -= 1
            xmax1 += 1
        else:
            xmin1 -= 0.05
            xmax1 += 0.05
        # print("xmin1:", xmin1, "xmax1:", xmax1)
        x_lobf = np.linspace(xmin1, xmax1, 2)
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
        # plotly.offline.plot(fig, filename=pfilename)


        #plotly.offline.plot({
        #    "data": [go.Scatter(x=parr_x, y=parr_y)],
        #    "layout": go.Layout(title="test graph")
        #})
    elif gtype == "hist":
        # HISTOGRAM CODE!!!!!!!
        numbins = int(np.ceil((xmax1 - xmin1)/2))
        l1 = []
        for player in pdict:
            tr0 = go.Scatter(
                x = player[xax[0]]
            )
        tr1 = go.Histogram(x=plf_x,  # histnorm='probability density',
                           text=plf_arr_name, name="velo buckets",
                           xbins=dict(start=np.min(plf_x), size=1.83, end=np.max(plf_x))
                           )
        layout1 = dict(
            title="helo",
            autosize=True,
            bargap=0.015,
            height=600,
            width=700,
            hovermode='x',
            xaxis=dict(
                autorange=True,
                zeroline=False),
            yaxis=dict(
                autorange=True,
                showticklabels=True,
            ))
        fig1 = dict(data=[tr1], layout=layout1)
        plotly.offline.plot(fig1)

        # END HISTOGRAM CODE!!!!!!!!
    # end if

    # printing out the linear regression values
    print("rval:", str(lr_array.rvalue), "slope:", str(lr_array.slope), "y-intercept:", str(lr_array.intercept))
# end plotter
