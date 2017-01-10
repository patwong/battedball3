import bbclass
# def plotter(pdict, xax, yax, ptitle, pfilename,lobf,type, xy0):
# xax: (pdict val, x-axis title)
# yax (scatter): (pdict val, y-axis title)
# yax (hist): string -> to label each bin
# ptitle: string
# pfilename: filename
# (Max BB Speed-Avg BB Speed) Versus Batting Average'
# lobf: True or False
# type: "scatter", "hist"
# xy0: (boolean, boolean) => if True, x or y = 0 value won't be ignored
# bbp3.plotter(pdict,0,0,0,'maxbb_ahs_ba2')
# player keys: fbld, k%, wRC+, season, brl_pa, fWAR, max_hit_speed,
#   brl_percent, avg_distance, slg, max_distance, iso_str, ba, obp
#   barrels, attempts, babip, avg_hit_speed, avg_hr_distance, min_hit_speed
#   gb, wOBA, BsR, bb%

x1 = bbclass()
yname = 'iso_str'
xname = 'avg_hit_speed'
gtype = "hist"
if xname in axesdict and yname in axesdict:
    yax = (yname, axesdict[yname])
    xax = (xname, axesdict[xname])
    if gtype == "scatter":
        ptitle = yax[1] + " versus " + xax[1]
        pfilename = yname + "_vs_" + xname + ".html"
    # bbp3.plotter(pdict, xax, yax, ptitle, pfilename, True, "scatter", (True, True))     # scatter test
    if gtype == "hist":
        yname = "wRC+"
        ptitle = xax[1] + " histogram"
        pfilename = xax[0] + "_histogram.html"
        bbp3.plotter(pdict, xax, yname, ptitle, pfilename, True, "hist", (True, True))    # hist test

else:
    print("enter correct player stat!")

# implements "main" from battedball.py
x1.scatter(xname, yname, gtype)
x1.cleanfiles() # clears all the pickle files
x1.__init__()   # after clearing the pickles, reinitialize the class with fresh pickle files + dicts

