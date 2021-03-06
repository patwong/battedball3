import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import mpld3


# plots barrels/PA verus average hitting speed
# may be useful to see who isn't squaring the ball with authority
def brl_pa_vs_avg_hit_speed(pdict, statdict):
    fastr = "Free Agent"
    notfastr = "Contracted Player"
    facolor = 'red'
    notfacolor = 'blue'

    # for line of best fit, two lists of equal size created
    # one list corresponding to the x-value, the other with y-values
    # using list instead of array; no idea the actual size so list is better
    lobf_x = []
    lobf_y = []
    lobf_fa_x = []
    lobf_fa_y = []
    playerlist = []
    playerlist_fa = []

    # initialize the plots
    fig1, ax1 = plt.subplots()

    # iterate through the dictionary
    for key in pdict:
        player = pdict[key]
        if player['brl_pa'] != 0:
            if player['freeagent']:
                lobf_fa_x.append(player['avg_hit_speed'])
                lobf_fa_y.append(player['brl_pa'])
                playerlist_fa.append(player['name'])
            else:
                lobf_x.append(player['avg_hit_speed'])
                lobf_y.append(player['brl_pa'])
                playerlist.append(player['name'])
            if player['name'] == "Tuffy Gosewisch":
                print("x, y, name:", player['avg_hit_speed'], player['brl_pa'], player['name'])
    # end loop

    # converts x and y lists to numpy arrays for matplotlib/mpld3
    xarray = np.asarray(lobf_x)
    yarray = np.asarray(lobf_y)
    xarray_fa = np.asarray(lobf_fa_x)
    yarray_fa = np.asarray(lobf_fa_y)
    ax1.scatter(xarray, yarray, c=notfacolor)                 # not free agent
    ax1.scatter(xarray_fa, yarray_fa, marker='D', c=facolor)  # free agent

    # hacky plot-over-plot to allow hoverable tooltips
    # combines the two arrays (free agent + not free agent) and plots invisible points
    # (too dumb to figure out a clever way to ensure both colors appear)
    xarray = np.concatenate((xarray, xarray_fa), axis=0)
    yarray = np.concatenate((yarray, yarray_fa), axis=0)
    playerlist = playerlist + playerlist_fa
    sc1 = ax1.scatter(xarray, yarray, alpha=0)  # alpha=0 plots invisible points

    # line of best fit
    lr_array = stats.linregress(xarray, yarray)
    xa_lobf = np.linspace(80, 98, 10, dtype=int)
    ya_lobf = lr_array.slope * xa_lobf + lr_array.intercept
    # print(lr_array.rvalue)  # correlation coefficient 0.6739 ; slight positive correlation
    ax1.plot(xa_lobf, ya_lobf)

    ax1.set_xlabel('Average Hit Speed')
    ax1.set_ylabel('Barrels/PA')
    ax1.set_title('Average Hit Speed Underformers')

    # fig1.legend(loc='upper left', scatterpoints=1)

    tooltip = mpld3.plugins.PointLabelTooltip(sc1, labels=playerlist)
    ax1.grid(color='white', linestyle='solid')

    # plot the plot
    mpld3.plugins.connect(fig1, tooltip)
    mpld3.show()
    # mpld3.save_html(fig1, "brlpa_ahs.html")
#    plt.show(block=False)  # prevents matplotlib plot from blocking
#    plt.close('all')
#    return

    # debugging statements:
    # statdict['surprise'] = "dict is mutable :)"   # dictionaries are mutable
#end plotter
