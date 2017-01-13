import bb3class


x1 = bb3class.bb3class()
yname = 'iso_str'
yname2 = 'wRC+'
xname = 'avg_hit_speed'
bins = 10
# x1.scatter(xname,yname,(True, True))
x1.hist(xname, yname2, bins)

# x1.cleanfiles() # clears all the pickle files
# x1.__init__()   # after clearing the pickles, reinitialize the class with fresh pickle files + dicts

