# example script on how to this code
# simply uncomment the function calls to see the results

import battedball

x1 = battedball.battedball()
yname = 'iso_str'
yname2 = 'wRC+'
yname3 = 'brl_pa'
xname = 'avg_hit_speed'
bins = 10

# finding a player - if player found, outputs their stats to the console
x1.find('Mike Trout')

# making a scatter plot - tuple argument specifies if x or y values are allowed to be zero
# x1.scatter(xname, yname, (True, True))
x1.scatter(xname, yname3, (True, False))

# making a histogram - (binned stat, hover text stat, number of bins)
# x1.hist(xname, yname2, bins)

### how to call "help" on a particular method - examples ###
# print(x1.hist.__doc__)
# print(x1.scatter.__doc__)
# print(x1.find.__doc__)

# clears all the pickle files and recreates them
# x1.cleanfiles()