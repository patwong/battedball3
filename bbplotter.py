import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# plots barrels/PA verus average hitting speed
# may be useful to see who isn't squaring the ball with authority
def fa_to_plot(pdict, statdict):
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

    fa_c = 0        # free_agent counter: used to set the legend
    nfa_c = 0       # not free agent counter: used to set the legend

    for key in pdict:
        player = pdict[key]
        if player['brl_pa'] != 0:
            if player['freeagent']:
                if fa_c == 1:
                    plt.scatter(player['avg_hit_speed'], player['brl_pa'], marker='D', c=facolor)
                else:
                    plt.scatter(player['avg_hit_speed'], player['brl_pa'], marker='D', c=facolor, label=fastr)
                    fa_c = 1
                lobf_x.append(player['avg_hit_speed'])
                lobf_y.append(player['brl_pa'])
            else:
                if nfa_c == 1:
                    plt.scatter(player['avg_hit_speed'], player['brl_pa'], c=defcolor)
                else:
                    plt.scatter(player['avg_hit_speed'], player['brl_pa'], c=defcolor, label=notfastr)
                    nfa_c = 1
                lobf_x.append(player['avg_hit_speed'])
                lobf_y.append(player['brl_pa'])
    # end loop

    xarray = np.asarray(lobf_x)
    yarray = np.asarray(lobf_y)
    lr_array = stats.linregress(xarray, yarray)
    xa_lobf = np.linspace(80, 98, 10, dtype=int)
    ya_lobf = lr_array.slope * xa_lobf + lr_array.intercept
    plt.plot(xa_lobf, ya_lobf)
    plt.xlabel('Average Hit Speed')
    plt.ylabel('Barrels/PA')
    plt.legend(loc='upper left', scatterpoints=1)
    plt.grid(True)
    plt.ylim(0, statdict['max_brl_pa'] + 0.02)
    plt.xlim(80, statdict['max_avg_hs'] + 1)
    plt.show()

    # debugging statements:
    # statdict['surprise'] = "dict is mutable :)"   # dictionaries are mutable
#end plotter
