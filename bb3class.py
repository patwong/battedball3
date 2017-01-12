class bb3class:
    """
    modularizes the battedball method collection into a class object
    bbclass can only be defined if the valid json, csv, and txt files
    are located in the Data subdirectory of the working folder
    """

    def __init__(self):
        self.pdict = {}
        self.statdict = {}
        self.axesdict = {}
        self.bbparser()

    # merging list of free agents with dictionary
    # if player is a free agent, change their free agent status to True
    def merge_fas(self, fa_file):
        falist = open(fa_file)
        for fa in falist:
            f_a = fa.strip('\r\n')
            if f_a in self.pdict:
                player = self.pdict[f_a]
                player['freeagent'] = True  # this actually changes the value of the player in pdict
    # end merge_fas

    # opens the json file and creates a dictionary
    # working with static jason file 'playerlist.json'
    # playerlist.json retrieved from page source at https://baseballsavant.mlb.com/statcast_leaderboard
    # query: minimum batted balls events of 30, season 2016
    # would be better if json file is specified from user, but this is just for fun :)
    def parse_and_dict(self, json_fname):
        import json
        json1_file = open(json_fname)
        json1_str = json1_file.read()

        # json.loads turns the json into a list of dictionaries
        json1_data = json.loads(json1_str)  # gets the whole dictionary
        playercounter = 0
        mavahs_name = ""
        minahs_name = ""
        mavahs = 0
        minahs = 100
        league_ahs = 0

        # useful for setting the axes of the brl_pa/avg hit speed graph
        max_brl_pa_name = ""
        max_brl_pa = 0

        # populate the dictionary pdict
        for player in json1_data:
            pname = player['name']

            # to int: avg_distance, avg_hr_distance, batter, max_distance, player_id
            player['avg_distance'] = int(player['avg_distance'])
            ahd = str(player['avg_hr_distance'])  # manually changed null to "null" in list
            if ahd.lower() == 'null':  # sometimes ahd is null; players w/o hr
                player['avg_hr_distance'] = 0
            else:
                player['avg_hr_distance'] = int(player['avg_hr_distance'])
            player['batter'] = int(player['batter'])
            player['max_distance'] = int(player['max_distance'])
            player['player_id'] = int(player['player_id'])

            # to float: avg_hit_speed, brl_pa(%), brl_percent(%), fbld, gb, max_hit_speed, min_hit_speed
            player['avg_hit_speed'] = float(player['avg_hit_speed'])
            league_ahs = league_ahs + player['avg_hit_speed']
            player['brl_pa'] = float(player['brl_pa'].strip('%')) / 100
            player['brl_percent'] = float(player['brl_percent'].strip('%')) / 100
            player['fbld'] = float(player['fbld'])
            player['gb'] = float(player['gb'])
            player['max_hit_speed'] = float(player['max_hit_speed'])
            player['min_hit_speed'] = float(player['min_hit_speed'])

            # to bool: freeagent
            if player['freeagent'].lower() == 'true':
                player['freeagent'] = True
            else:
                player['freeagent'] = False

            # populating pdict
            # sets a player's value in the dictionary
            self.pdict[pname] = player
            playercounter += 1

            # min/max cases for stats
            # finding player with max avg hit speed
            # finding player with max amount of "barrels"/PA
            if player['avg_hit_speed'] > mavahs:
                mavahs = player['avg_hit_speed']
                mavahs_name = pname
            if player['avg_hit_speed'] < minahs:
                minahs = player['avg_hit_speed']
                minahs_name = pname
            if player['brl_pa'] > max_brl_pa:
                max_brl_pa_name = player['name']
                max_brl_pa = player['brl_pa']
                # debugging statements
                # pseason = str(player['season'])     # season is treated as an int
                # pmhs = player['max_hit_speed']
                # print "in " + pseason + ", " + pname + " had max hit speed of " + str(pmhs)

                # end loop
        # more code

        ############ league-wide stats!!! ############
        self.statdict['pc'] = playercounter

        # name of player with max/min average hitting speed, max/min hitting speed
        self.statdict['max_avg_hs'] = mavahs
        self.statdict['max_avg_hs_name'] = mavahs_name
        self.statdict['min_avg_hs'] = minahs
        self.statdict['min_avg_hs_name'] = minahs_name

        self.statdict['max_brl_pa_name'] = max_brl_pa_name  # :)
        self.statdict['max_brl_pa'] = max_brl_pa

        self.statdict['league_ahs'] = float('%.2f' % (league_ahs / playercounter))  # truncate the float
    # end parse_and_dict

    # from csv file, add a player's BA to the dictionary
    def fgstats_to_dict(self, csv_fname):
        import csv
        import os.path

        csvfile = open(csv_fname, 'rt', encoding='utf-8')   # safer to have script determine csv's encoding
        csvreader = csv.reader(csvfile)
        notindict = "Data/playersnotindict.txt"
        f1 = open(notindict, 'a')
        nic = 0
        if not (os.path.isfile(notindict)):
            nic = 1  # if nic == 1, file only written once
            print("creating file that contains players not in dictionary")
            f1.write("players not in dictionary:\n")

        for row in csvreader:
            # csv file is currently formatted with the first line being "Name, Avg"
            # all subsequent elements are of that form
            # csv.reader formats each line ("row") as a list of strings
            # list indices:
            # 0: name, 1: team, 2: games played, 3: plate appearances, 4: HR
            # 5: runs, 6: rbi, 7: # stolen bases, 8: BB%, 9: K%, 10: ISO
            # 11: BABIP, 12: BA, 13: OBP, 14: SLG, 15: wOBA, 16: wRC+, 17: BsR
            # 18: off rating, 19: def rating, 20: fWAR, 21: playerID
            player_name = row[0]
            if player_name in self.pdict:
                bb_percent = float(row[8].strip(' %')) / 100
                k_percent = float(row[9].strip(' %')) / 100
                iso_str = float(row[10])
                BABIP = float(row[11])
                BA = float(row[12])
                OBP = float(row[13])
                SLG = float(row[14])
                wOBA = float(row[15])
                wRCp = int(row[16])
                BsR = float(row[17])
                fWAR = float(row[20])

                player = self.pdict[player_name]
                player['bb%'] = bb_percent
                player['k%'] = k_percent
                player['iso_str'] = iso_str
                player['babip'] = BABIP
                player['ba'] = BA
                player['obp'] = OBP
                player['slg'] = SLG
                player['wOBA'] = wOBA
                player['wRC+'] = wRCp
                player['BsR'] = BsR
                player['fWAR'] = fWAR
            # if player not found, add his name to the file
            elif os.path.isfile(notindict) and nic == 1 and row[0] != 'Name':
                to_out = row[0] + '\n'
                f1.write(to_out)
        # for safety, close the file
        f1.close()
    # end adding_ba_to_dict

    # remove all auxiliary files created by my program
    # list: playersnotindict.txt, pdict.pickle, statdict.pickle
    def cleanfiles(self):
        import os
        os.chdir('Data')
        filedir = os.listdir()
        print("source files currently in directory\n" + str(filedir))
        print("deleting all pickle files + playersnotindict.txt")
        # remove pickle files
        for f in filedir:
            if f.endswith(".pickle"):
                os.remove(f)
            elif f == 'playersnotindict.txt':
                os.remove(f)
        print('operation complete')
        filedir = os.listdir()
        print("files currently in directory\n" + str(filedir))
        filedir = os.chdir('..')
    # end cleanfiles()


    # maps the shorthand key name to its full name
    # useful when sending data to the plotter; for the axes
    def key_to_axes(self):
        import os
        import pickle
        fname = "Data/key_to_axes.pickle"
        if os.path.isfile(fname):
            print(fname, "found")
            with open(fname, 'rb') as ktahandle:
                self.axesdict = pickle.load(ktahandle)
        else:
            print(fname, "not found")
            self.axesdict['fbld'] = "Average FB/LD Exit Velocity (MPH)"
            self.axesdict['k%'] = "K%"
            self.axesdict['wRC+'] = "wRC+"
            self.axesdict['season'] = "Season"
            self.axesdict['brl_pa'] = "Barrels/Plate Appearances"
            self.axesdict['fWAR'] = "fWAR"
            self.axesdict['max_hit_speed'] = "Maximum Exit Velocity (MPH)"
            self.axesdict['brl_percent'] = "Barrels/Batted Ball Events"
            self.axesdict['avg_distance'] = "Average Distance (ft)"
            self.axesdict['slg'] = "SLG"
            self.axesdict['max_distance'] = "Maximum Distance (ft)"
            self.axesdict['iso_str'] = "Isolated Power"
            self.axesdict['ba'] = "Batting Average"
            self.axesdict['obp'] = "On-Base Percentage"
            self.axesdict['barrels'] = "Total Barreled Balls"
            self.axesdict['attempts'] = "Batted Ball Events"
            self.axesdict['babip'] = "BABIP"
            self.axesdict['avg_hit_speed'] = "Average Exit Velocity (MPH)"
            self.axesdict['avg_hr_distance'] = "Average Home Run Distance (ft)"
            self.axesdict['min_hit_speed'] = "Minimum Hit Speed (MPH)"
            self.axesdict['gb'] = "Average Groundball Exit Velocity (MPH"
            self.axesdict['wOBA'] = "wOBA"
            self.axesdict['BsR'] = "BsR"
            self.axesdict['bb%'] = "bb%"
            with open(fname, 'wb') as ktahandle:
                pickle.dump(self.axesdict, ktahandle, protocol=pickle.HIGHEST_PROTOCOL)
    # end key_to_axes()

    # given player name, list his stats
    def find(self, pname):
        if pname in self.pdict:
            player = self.pdict[pname]
            i = 0
            output_str = []
            col_len = 0
            for keys in player:
                if isinstance(player[keys], float):
                    keyvalue = format(player[keys], '.2f')
                else:
                    keyvalue = player[keys]
                key_plus_stats = keys + ": " + str(keyvalue)
                kps_len = len(key_plus_stats)
                if kps_len > col_len:
                    col_len = kps_len
            col_len += 2
            for keys in player:
                if isinstance(player[keys], float):
                    keyvalue = format(player[keys], '.2f')
                else:
                    keyvalue = player[keys]
                output_str.append(keys + ": " + str(keyvalue))
                i += 1
                if i == 3:
                    # print(output_str)
                    print("".join(word.ljust(col_len) for word in output_str))
                    output_str = []
                    i = 0
            if output_str:
                print("".join(word.ljust(col_len) for word in output_str))
        else:
            print("player not found: " + pname)
    # end findplayer

    # second initialization routine: calls the parsers
    # checks if the source files exist and populates the dictionaries
    def bbparser(self):
        import os.path
        import sys
        import pickle

        # source files located in the Data directory:
        # 1. json file used to populate pdict
        # 2. list of free agent players for the current offseason
        # 3. fangraphs leaderboard stats
        json_fname = "Data/playerlist.json"
        fa_file = "Data/fullfalist.txt"
        csvfname = "Data/fgleaders1.csv"

        # exit if source files not found
        if not(os.path.isfile(csvfname)):
            print("csv not found")
            sys.exit(1)
        if not(os.path.isfile(json_fname)):
            print("battedball json not found")
            sys.exit(1)
        if not(os.path.isfile(fa_file)):
            print("free agent list not found")
            sys.exit(1)

        # runs the parsers or retrieves the dicts from pickle files
        # using pickle to store pdict and statdict
        pickled_pdict = "Data/pdict.pickle"
        pickled_statdict = "Data/statdict.pickle"
        self.key_to_axes()   # creates the shorthands for axes creation - has its own pickle checker
        if os.path.isfile(pickled_pdict) and os.path.isfile(pickled_statdict):
            print('pickled pdict and statdict found')
            with open(pickled_pdict, 'rb') as pdhandle:
                self.pdict = pickle.load(pdhandle)
            with open(pickled_statdict, 'rb') as sdhandle:
                self.statdict = pickle.load(sdhandle)
        else:
            print('pickled pdict and statdict file not found')
            self.parse_and_dict(json_fname)     # populate pdict
            self.fgstats_to_dict(csvfname)
            self.merge_fas(fa_file)             # adds free agent status to players
            with open(pickled_pdict, 'wb') as pdhandle:
                pickle.dump(self.pdict, pdhandle, protocol=pickle.HIGHEST_PROTOCOL)
            with open(pickled_statdict, 'wb') as sdhandle:
                pickle.dump(self.statdict, sdhandle, protocol=pickle.HIGHEST_PROTOCOL)
    # end parser

    # produces scatter plots
    def scatter(self, xval, yval, xy0):
        # xval: stat to be plotted on x-axis
        # yval: stat to be plotted on y-axis
        # xy0:
        # if xy0[0] is true, then x is allowed to be 0
        # if xy0[1] is true, then y is allowed to be 0
        # otherwise, they are not allowed to be 0 and tuples that fail the test are ignored

        if xval in self.axesdict:
            xtitle = self.axesdict[xval]
        else:
            print("xvalue stat not found:", xval)
            return
        if yval in self.axesdict:
            ytitle = self.axesdict[yval]
        else:
            print("[Exit Error]yvalue stat not found:", yval)
            return

        import numpy as np
        from scipy import stats
        import plotly
        import plotly.graph_objs as go

        ptitle = ytitle + " versus " + xtitle
        pfilename = yval + "_vs_" + xval + ".html"
        plist_full = []
        plist1 = []
        falist = []
        xmax1 = 0.0
        xmaxname = ""
        xmin1 = 0
        xmin1_c = 1
        for player_name in self.pdict:
            player = self.pdict[player_name]

            # set the first dictionary value as the first min value
            if xmin1_c == 1:
                xmin1 = player[xval]
                xmin1_c = 0
            # if xy0[0] is true, then x is allowed to be 0
            # if xy0[1] is true, then y is allowed to be 0
            # otherwise, they are not allowed to be 0 and tuples that fail the test are ignored
            xy2 = [True, True]
            if not (xy0[0]):
                xy2[0] = player[xval] > 0
            if not (xy0[1]):
                xy2[1] = player[yval] > 0

            if xy2[0] and xy2[1]:  # if player[yax[0]] > 0 and player[xax[0]] > 0:
                if player['freeagent']:
                    falist.append([player['name'], player[xval], player[yval]])
                else:
                    plist1.append([player['name'], player[xval], player[yval]])
                plist_full.append([player['name'], player[xval], player[yval]])

                if player[xval] > xmax1:
                    xmax1 = player[xval]
                    xmaxname = player['name']
                if player[xval] < xmin1:
                    xmin1 = player[xval]
        # print(xmaxname, xmax1)    # checking who's the x-max value

        # normal players
        parr = np.asarray(plist1)
        parr_name = parr[:, 0]
        parr_x = np.asarray(parr[:, 1], dtype='float64')
        parr_y = np.asarray(parr[:, 2], dtype='float64')

        # free agents
        fa_arr = np.asarray(falist)
        faa_name = fa_arr[:, 0]
        faa_x = np.asarray(fa_arr[:, 1], dtype='float64')
        faa_y = np.asarray(fa_arr[:, 2], dtype='float64')

        # full player list
        plf_arr = np.asarray(plist_full)
        # plf_arr_name = plf_arr[:, 0]
        plf_x = np.asarray(plf_arr[:, 1], dtype='float64')
        plf_y = np.asarray(plf_arr[:, 2], dtype='float64')

        # plotting the contracted players
        trace0 = go.Scatter(
            x=parr_x,
            y=parr_y,
            name='Contracted Players',
            text=parr_name,
            mode='markers'
        )

        # plotting the free agents
        trace1 = go.Scatter(
            x=faa_x,
            y=faa_y,
            name='Free Agents',
            text=faa_name,
            mode='markers'
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
            # text=faa_name,
            mode='lines'
        )

        # put the correlation coefficient in the title
        rvstring = format(lr_array.rvalue, '.2f')
        ptitle = ptitle + " (rvalue: " + rvstring + ")"
        layout = dict(title=ptitle,
                      yaxis=dict(
                          zeroline=False,
                          title=ytitle
                      ),
                      xaxis=dict(
                          zeroline=False,
                          title=xtitle
                      )
                      )

        # trace0: contracted players, trace1: free agents, trace2: line of best fit

        # plots line of best fit if there is moderate or better correlation
        if lr_array.rvalue > 0.3 or lr_array.rvalue < -0.3:     # positive or negative correlation
            data = [trace0, trace1, trace2]
        else:
            data = [trace0, trace1]

        fig = dict(data=data, layout=layout)
        plotly.offline.plot(fig, filename=pfilename)

        # printing out the linear regression values
        print("rval:", str(lr_array.rvalue), ", slope:", str(lr_array.slope), ", y-intercept:",
              str(lr_array.intercept))
    # end scatter

    # uses pandas
    def hist1(self, xval, yval, num_bins):
        if xval in self.axesdict:
            xtitle = self.axesdict[xval]
        else:
            print("xvalue stat not found:", xval)
            return
            # sys.exit(1)
        if yval in self.axesdict:
            ytitle = self.axesdict[yval]
        else:
            print("[Exit Error]yvalue stat not found:", yval)
            return
        import numpy as np
        import pandas as pd
        xlist = []
        ylist = []
        plist_full = []
        plist1 = []
        xmax1 = 0.0
        xmin1 = 0
        xmin1_c = 1

        for player_name in self.pdict:
            if xmin1_c == 1:
                xmin1 = player[xval]
                xmin1_c = 0
            player = self.pdict[player_name]
            xlist.append(player[xval])
            ylist.append(player[yval])
            if player[xval] > xmax1:
                xmax1 = player[xval]    # need max value to determine bin size
            if player[xval] < xmin1:
                xmin1 = player[xval]    # need min value to determine bin size
        # end loop

        raw_data = {xval: xlist, yval: ylist}
        pandaframe1 = pd.DataFrame(raw_data, columns=[xval, yval])
        binsize = (xmax1 - xmin1) / num_bins
        bin_list = []               # list of bin ranges
        bin_list_names = []         # list of names for the bins, i.e. bin0,...,binN
        bl_c = xmin1
        for i in range(num_bins):
            bl_str = "bin " + str(i)
            bin_list.append(bl_c)
            bin_list_names.append(round(bl_str, 2)) # round to two sigfigs
            bl_c += binsize
        bin_list.append(round(bl_c, 2))             # add the "max" to the bin, adjusted for stupid float vals
        bin_list[0] -= np.ceil(bin_list[0]*0.01)    # adjust min bin by lowering its threshold, since bin by rightmost (see docs)
        pandaframe1['bins'] = pd.cut(pandaframe1[xval], bin_list, labels=bin_list_names)
        # demo pandas by checking if pd.value_counts(df[name]) works
    # end hist1

    # successor to bbp2 - uses plotly instead of mpld3
    def hist(self, xval, yval, xy0):
        if xval in self.axesdict:
            xtitle = self.axesdict[xval]
        else:
            print("xvalue stat not found:", xval)
            return
            # sys.exit(1)
        if yval in self.axesdict:
            ytitle = self.axesdict[yval]
        else:
            print("[Exit Error]yvalue stat not found:", yval)
            return
            # sys.exit(1)
        import numpy as np
        import plotly
        import plotly.graph_objs as go
        yname = "wRC+"
        ptitle = xtitle + " histogram"
        pfilename = xval + "_histogram.html"

        # xax: (pdict val, x-axis title), yax: (pdict val, y-axis title)

        plist_full = []
        plist1 = []
        falist = []
        xmax1 = 0.0
        xmaxname = ""
        xmin1 = 0
        xmin1_c = 1

        # HISTOGRAM CODE!!!!!!!
        for player_name in self.pdict:
            player = self.pdict[player_name]
            if xmin1_c == 1:
                xmin1 = player[xval]
                xmin1_c = 0

            # if xy0[0] is true, then x is allowed to be 0
            # if xy0[1] is true, then y is allowed to be 0
            # otherwise, they are not allowed to be 0 and tuples that fail the test are ignored
            xy2 = [True, True]
            if not (xy0[0]):
                xy2[0] = player[xval] > 0
            if not (xy0[1]):
                xy2[1] = player[yval] > 0

            if xy2[0] and xy2[1]:
                if player['freeagent']:
                    falist.append([player['name'], player[xval]])
                else:
                    plist1.append([player['name'], player[xval]])
                plist_full.append([player['name'], player[xval]])
                if player[xval] > xmax1:
                    xmax1 = player[xval]
                    xmaxname = player['name']
                if player[xval] < xmin1:
                    xmin1 = player[xval]

        # using 10 bins for the histogram
        numbins = 10
        binsize = (xmax1 - xmin1) / numbins

        # list 1 for the 10th percentile, 2 for the 20th, etc
        bin_of_bins = [[] for x in range(numbins)]

        # get the average wRC+ for each bin
        for player_name in self.pdict:
            player = self.pdict[player_name]
            bin_finder = xmin1
            for x in range(0, numbins):
                bin_finder += binsize
                if player[xval] < bin_finder:
                    bin_of_bins[x - 1].append(player[yval])
                    break

        # getting the stdev, mean of each bin
        bin_stats = []
        c = 0
        for bin_list in bin_of_bins:
            bin_array = np.asarray(bin_list)
            bin_mean = np.mean(bin_array)
            bin_sd = np.std(bin_array)
            bin_stats.append(
                "Average wRC+: " + format(bin_mean, '.2f') + "\nStandard Dev: " + format(bin_sd, '.2f'))
        bin_stats_array = np.asarray(bin_stats)

        # create the arrays to plot
        plf_arr = np.asarray(plist_full)
        # plf_arr_name = plf_arr[:, 0]
        plf_x = np.asarray(plf_arr[:, 1], dtype='float64')

        # plot the histogram
        tr1 = go.Histogram(x=plf_x,
                           # histnorm='probability density',
                           text='hi',  # text= bin_stats_array,
                           # hoverinfo="text",
                           # name="velo buckets",
                           autobinx=False,
                           xbins=dict(start=np.min(plf_x), size=binsize, end=np.max(plf_x)),
                           # marker=dict(colorbar=dict(
                           #     tickmode='array',
                           #     ticktext=bin_stats_array
                           # )),
                           opacity=0.5
                           )
        layout1 = dict(
            title=ptitle,
            autosize=True,
            bargap=0.015,
            height=600,
            width=700,
            hovermode='x',
            xaxis=dict(
                autorange=True,
                title=xtitle,
                zeroline=False),
            yaxis=dict(
                autorange=True,
                title='count',
                showticklabels=True,
            ))
        fig1 = dict(data=[tr1], layout=layout1)
        plotly.offline.plot(fig1, filename=pfilename)
        print("length of x:", str(len(plf_x)))
        print(xtitle)
        print(np.min(plf_x), np.max(plf_x))
        # END HISTOGRAM CODE!!!!!!!!
        # end plotter

# end bbclass
