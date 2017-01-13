import bb3class


x1 = bb3class.battedball()
yname = 'iso_str'
yname2 = 'wRC+'
xname = 'avg_hit_speed'
bins = 10

# finding a player - if player found, displays their stats
x1.find('Mike Trout')

# making a scatter plot - tuple argument specifies if x or y values are allowed to be zero
# x1.scatter(xname, yname,(True, True))
x1.scatter(xname, 'brl_pa', (True, False))

# making a histogram - (binned stat, stat to appear as hover text, number of bins)
# x1.hist(xname, yname2, bins)

# clears all the pickle files
# x1.cleanfiles()

# after clearing the pickles, reinitialize the class with fresh pickle files + dicts
# x1.__init__()
