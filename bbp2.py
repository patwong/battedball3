import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import mpld3


# plots barrels/PA verus average hitting speed
# may be useful to see who isn't squaring the ball with authority
def plotter1(pdict, statdict):
    fastr = "Free Agent"
    notfastr = "Contracted Player"
    facolor = 'red'
    defcolor = 'blue'
    # numplayers = statdict['pc']

    # for line of best fit, two arrays of equal size created
    # one array corresponding to the x-value, the other with y-values
    # using list instead of array; no idea the actual size so list is better
    lobf_x = []
    lobf_y = []
    lobf_fa_x = []
    lobf_fa_y = []
    playerlist = []
    playerlist_fa = []

    fa_c = 0        # free_agent counter: used to set the legend
    nfa_c = 0       # not free agent counter: used to set the legend

    fig1, ax1 = plt.subplots()
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

    xarray = np.asarray(lobf_x)
    yarray = np.asarray(lobf_y)
    xarray_fa = np.asarray(lobf_fa_x)
    yarray_fa = np.asarray(lobf_fa_y)
    ax1.scatter(xarray, yarray, c='blue')
    ax1.scatter(xarray_fa, yarray_fa, marker='D', c='red')


    # ax1.scatter(xarray_fa, yarray_fa, c=facolor)
    xarray = np.concatenate((xarray, xarray_fa), axis=0)
    yarray = np.concatenate((yarray, yarray_fa), axis=0)
    playerlist = playerlist + playerlist_fa
    sc1 = ax1.scatter(xarray, yarray, alpha=0)

    # line of best fit
    lr_array = stats.linregress(xarray, yarray)
    xa_lobf = np.linspace(80, 98, 10, dtype=int)
    ya_lobf = lr_array.slope * xa_lobf + lr_array.intercept
    # print(lr_array.rvalue)  # 0.6739
    ax1.plot(xa_lobf, ya_lobf)

    ax1.set_xlabel('Average Hit Speed')
    ax1.set_ylabel('Barrels/PA')
    ax1.set_title('Average Hit Speed Underformers')

    # fig1.legend(loc='upper left', scatterpoints=1)

    tooltip = mpld3.plugins.PointLabelTooltip(sc1, labels=playerlist)
    ax1.grid(color='white', linestyle='solid')
    #fig1.set_xlim(0, statdict['max_brl_pa'] + 0.02)
    # fig1.ylim(0, statdict['max_brl_pa'] + 0.02)
    # fig1.xlim(80, statdict['max_avg_hs'] + 1)

    # plot the plot
    mpld3.plugins.connect(fig1, tooltip)
    mpld3.show()
    # plt.show()
#    plt.show(block=False)  # prevents matplotlib plot from blocking
    # plt.close(bbfig)
#    plt.close('all')
#    return

    # debugging statements:
    # statdict['surprise'] = "dict is mutable :)"   # dictionaries are mutable
#end plotter
