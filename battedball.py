class battedball:
    """
    modularizes the battedball method collection into a class object.
    bbclass can only be defined if the valid json, csv, and txt files
    are located in the Data subdirectory of the working folder
    """

    # initialization routine
    def __init__(self):
        self.player_dictionary = {}
        self.stat_dictionary = {}
        self.axes_dictionary = {}
        self.__bb_parser()

    # remove all auxiliary files created by my program
    # list: playersnotindict.txt, player_dictionary.pickle, stat_dictionary.pickle
    def cleanfiles(self):
        """
        cleanfiles()
        - removes all auxiliary files created by the script and recreates them
        - e.g. playersnotindict.txt, player_dictionary.pickle, stat_dictionary.pickle
        """

        import os
        os.chdir('Data')
        file_directory = os.listdir()
        print("source files currently in directory\n" + str(file_directory))
        print("deleting all pickle files + playersnotindict.txt")
        # remove pickle files
        for a_file in file_directory:
            if a_file.endswith(".pickle"):
                os.remove(a_file)
            elif a_file == 'playersnotindict.txt':
                os.remove(a_file)
        print('operation complete')
        file_directory = os.listdir()
        print("files currently in directory\n" + str(file_directory))
        os.chdir('..')  # get back to home directory
        # reinitialize the auxiliary files
        self.__init__()
    # end cleanfiles()

    # given player name, list his stats
    def find(self, player_name):
        """
        find(player_name)
        :param player_name: string (player's name)
        :return: player's stats in console output
        """

        if player_name in self.player_dictionary:
            player = self.player_dictionary[player_name]
            i = 0
            output_string = []
            column_length = 0
            for keys in player:
                if isinstance(player[keys], float):
                    key_value = format(player[keys], '.2f')
                else:
                    key_value = player[keys]
                key_plus_stats = keys + ": " + str(key_value)
                kps_length = len(key_plus_stats)
                if kps_length > column_length:
                    column_length = kps_length
            column_length += 2
            for keys in player:
                if isinstance(player[keys], float):
                    key_value = format(player[keys], '.2f')
                else:
                    key_value = player[keys]
                output_string.append(keys + ": " + str(key_value))
                i += 1
                if i == 3:
                    print("".join(word.ljust(column_length) for word in output_string))
                    output_string = []
                    i = 0
            if output_string:
                print("".join(word.ljust(column_length) for word in output_string))
        else:
            print("player not found: " + player_name)
    # end findplayer

    # produces scatter plots
    def scatter(self, x_stat, y_stat, xy_0_limit):
        """
        scatter(x_stat, y_stat, xy_0_limit)
        :param x_stat: string, stat to be plotted on x-axis
        :param y_stat: string, stat to be plotted on y-axis
        :param xy_0_limit: (boolean, boolean)
            if xy_0_limit[0] is true, then x is allowed to be 0
            if xy_0_limit[1] is true, then y is allowed to be 0
            otherwise, they are not allowed to be 0 and tuples that fail the test are ignored
        :return: html file with the plotted stats (opens in default web browser)
        """

        # sanity checks
        # checking if x_stat and y_stat exist in the axes_dictionary
        # if they exist, then they will be formatted and put into the title and appear on graph axes
        if x_stat in self.axes_dictionary:
            x_title = self.axes_dictionary[x_stat]
        else:
            print("stat for x-axis not found:", x_stat)
            return
        if y_stat in self.axes_dictionary:
            y_title = self.axes_dictionary[y_stat]
        else:
            print("stat for y-axis not found:", y_stat)
            return
        if isinstance(xy_0_limit, tuple):
            if not(isinstance(xy_0_limit[0], bool)) or not(isinstance(xy_0_limit[0], bool)):
                print("xy_0_limit needs to be a tuple of boolean values")
                return
        else:
            print("xy_0_limit needs to be a tuple of boolean values")
            return

        import numpy as np
        from scipy import stats
        import plotly
        import plotly.graph_objs as go

        plot_title = y_title + " versus " + x_title
        plot_filename = y_stat + "_vs_" + x_stat + ".html"
        full_player_list = []
        contracted_player_list = []
        free_agent_list = []
        max_x_value = 0.0
        min_x_value = 0
        min_x_value_check = 1
        for player_name in self.player_dictionary:
            player = self.player_dictionary[player_name]

            # set the first dictionary value as the first min value
            if min_x_value_check == 1:
                min_x_value = player[x_stat]
                min_x_value_check = 0
            # if xy_0_limit[0] is true, then x is allowed to be 0
            # if xy_0_limit[1] is true, then y is allowed to be 0
            # otherwise, they are not allowed to be 0 and tuples that fail the test are ignored
            xy2 = [True, True]
            if not (xy_0_limit[0]):
                xy2[0] = player[x_stat] > 0
            if not (xy_0_limit[1]):
                xy2[1] = player[y_stat] > 0

            if xy2[0] and xy2[1]:  # if player[yax[0]] > 0 and player[xax[0]] > 0:
                if player['freeagent']:
                    free_agent_list.append([player['name'], player[x_stat], player[y_stat]])
                else:
                    contracted_player_list.append([player['name'], player[x_stat], player[y_stat]])
                full_player_list.append([player['name'], player[x_stat], player[y_stat]])

                if player[x_stat] > max_x_value:
                    max_x_value = player[x_stat]
                if player[x_stat] < min_x_value:
                    min_x_value = player[x_stat]
        # end loop

        # convert FA/contracted player lists to array;
        # lists are easy to append, arrays as input to plotly

        # normal players
        contracted_player_array = np.asarray(contracted_player_list)
        contracted_players_names = contracted_player_array[:, 0]
        contracted_players_x_array = np.asarray(contracted_player_array[:, 1], dtype='float64')
        contracted_players_y_array = np.asarray(contracted_player_array[:, 2], dtype='float64')

        # free agents
        free_agent_array = np.asarray(free_agent_list)
        free_agent_names = free_agent_array[:, 0]
        free_agent_x_array = np.asarray(free_agent_array[:, 1], dtype='float64')
        free_agent_y_array = np.asarray(free_agent_array[:, 2], dtype='float64')

        # full player array - for the line of best fit
        players_array = np.asarray(full_player_list)
        players_x_array = np.asarray(players_array[:, 1], dtype='float64')
        players_y_array = np.asarray(players_array[:, 2], dtype='float64')

        # plotting the contracted players
        contracted_plot = go.Scatter(
            x=contracted_players_x_array,
            y=contracted_players_y_array,
            name='Contracted Players',
            text=contracted_players_names,
            mode='markers'
        )

        # plotting the free agents
        free_agent_plot = go.Scatter(
            x=free_agent_x_array,
            y=free_agent_y_array,
            name='Free Agents',
            text=free_agent_names,
            mode='markers'
        )

        # line of best fit code
        # isinstance(value, type) => boolean, i.e. isinstance(0.5, float) => True
        # use this to adjust the xmin/xmax values
        linear_regress_array = stats.linregress(players_x_array, players_y_array)

        if (max_x_value - min_x_value) > 1:
        # hacky way to adjust the line of best fit length to make it stretch less
            min_x_value -= 1
            max_x_value += 1
        else:
            min_x_value -= 0.05
            max_x_value += 0.05
        x_line_of_best_fit_array = np.linspace(min_x_value, max_x_value, 2)
        y_line_of_best_fit_array = linear_regress_array.slope * x_line_of_best_fit_array + linear_regress_array.intercept
        line_of_best_fit_plot = go.Scatter(
            x=x_line_of_best_fit_array,
            y=y_line_of_best_fit_array,
            name='Line of Best Fit',
            mode='lines'
        )

        # put the correlation coefficient (r) in the title (up to 2 decimal places)
        r_value = format(linear_regress_array.rvalue, '.2f')
        plot_title = plot_title + " (rvalue: " + r_value + ")"
        layout = dict(title=plot_title,
                      yaxis=dict(
                          zeroline=False,
                          title=y_title
                      ),
                      xaxis=dict(
                          zeroline=False,
                          title=x_title
                      )
                      )

        # contracted_plot: contracted players, free_agent_plot: free agents, line_of_best_fit_plot: line of best fit
        # plots line of best fit if there is moderate or better correlation
        if linear_regress_array.rvalue > 0.3 or linear_regress_array.rvalue < -0.3:     # positive or negative correlation
            data = [contracted_plot, free_agent_plot, line_of_best_fit_plot]
        else:
            data = [contracted_plot, free_agent_plot]

        fig = dict(data=data, layout=layout)
        plotly.offline.plot(fig, filename=plot_filename)

        # printing out the linear regression values
        print("rval:", str(linear_regress_array.rvalue), ", slope:", str(linear_regress_array.slope), ", y-intercept:",
              str(linear_regress_array.intercept))
    # end scatter

    # updated histogram plotter - uses pandas and plotly's bar graphs rather than its built-in hist
    def hist(self, frequency_stat, hover_stat, bins):
        """
        hist(x, y, bins)
        :param frequency_stat: string, stat to be binned and plotted
        :param hover_stat: string, stat that will be as hoverable text over each bin
        :param bins: int, number of bins to be plotted
        :return: html file with the plotted stats (opens in default web browser)
        """

        # sanity checks
        # checking if frequency_stat and hover_stat exist in the axes_dictionary
        # if they exist, then they will be formatted and put into the title and appear on graph axes
        if frequency_stat in self.axes_dictionary:
            x_title = self.axes_dictionary[frequency_stat]
        else:
            print("stat for x-axis not found:", frequency_stat)
            return
        if hover_stat in self.axes_dictionary:
            y_title = self.axes_dictionary[hover_stat]
        else:
            print("stat for y-axis not found:", hover_stat)
            return
        if not(isinstance(bins, int)):
            print("enter a positive integer number of bins!!!")
            return
        elif bins < 2:
            print("please enter a valid number of bins (bins > 1)")
            return

        import numpy as np
        import pandas as pd
        import plotly
        import plotly.graph_objs as go

        # the "x-axis list" used for frequency data
        # the "y-axis list" used for additional data to appear as hover text
        frequency_data_list = []
        hover_text_stat_list = []
        plot_title = x_title + " histogram"
        plot_filename = frequency_stat + "_hist.html"

        # populate the frequency/hover text lists
        for player_name in self.player_dictionary:
            player = self.player_dictionary[player_name]
            frequency_data_list.append(player[frequency_stat])
            hover_text_stat_list.append(player[hover_stat])
        # end loop

        # put frequency_data_list and hover_text_stat_list into pandas' dataframe - pandas is very useful!!
        raw_data = {frequency_stat: frequency_data_list, hover_stat: hover_text_stat_list}
        pandas_dataframe1 = pd.DataFrame(raw_data, columns=[frequency_stat, hover_stat])

        #get min/max value for bin sizes
        frequency_max = float((pandas_dataframe1.describe()).loc['max', frequency_stat])
        frequency_min = float((pandas_dataframe1.describe()).loc['min', frequency_stat])

        # bin processing
        bin_size = (frequency_max - frequency_min) / bins
        bin_list = []               # list of bin ranges
        names_of_bins = []          # list of bin names, i.e. bin0,...,binN
        bin_ranges = []             # list of bin names by range, i.e. (x0, x1], (x1, x2],..., (xn-1, xn]
        num_bins_init = frequency_min                # to initialize the bin ranges
        for i in range(bins):
            bin_name = "bin" + str(i)                               # bin_name: for names_of_bins
            bin_list.append(round(num_bins_init, 2))                # round to two sigfigs; precision unimportant
            bin_range_name = "(" + str(round(num_bins_init, 2))     # bin_range_name: for bin_ranges
            num_bins_init += bin_size
            bin_range_name += ", " + str(round(num_bins_init, 2)) + "]"
            names_of_bins.append(bin_name)
            bin_ranges.append(bin_range_name)
        bin_list.append(round(num_bins_init, 2))             # add the "max" to the bin, adjusted for stupid float vals

        # adjust min bin by lowering its threshold, since binned by rightmost, i.e. (x1,x2] (see docs)
        bin_list[0] = float(bin_list[0] - np.ceil(bin_list[0]*0.01))
        bin_ranges[0] = "(" + str(bin_list[0]) + ", " + str(bin_list[1]) + "]"

        # using pandas' cut to bin the values
        pandas_dataframe1['bins'] = pd.cut(pandas_dataframe1[frequency_stat], bin_list, labels=names_of_bins)

        # groups all the rows in the dataframe by their bin name and gets their count
        # pd.value_counts returns a pd.Series, not a dataframe
        pandas_series1 = pd.value_counts(pandas_dataframe1['bins'])
        pandas_series1 = pandas_series1.sort_index(axis=0)        # sorts dataframe by bin name - default is by value

        # get the average y-val per bin name and put it in a list
        avg_hover_stat_list = []
        avg_hover_stat_name = 'avg_' + hover_stat
        for some_bin_name in names_of_bins:
            # ugly code to get the average y-stat per bin
            # 1. get the value, 2. round the value, 3. format the value for hover text
            avg_hover_stat = ((pandas_dataframe1[pandas_dataframe1['bins'] == some_bin_name]).describe()).loc['mean', hover_stat]
            avg_hover_stat = round(float(avg_hover_stat), 2)
            bin_count = "count: " + str(pandas_series1.loc[some_bin_name])
            avg_hover_stat = bin_count + ", avg " + y_title + ": " + str(avg_hover_stat)
            avg_hover_stat_list.append(avg_hover_stat)

        # stat_dictionary['pc'] is the total count of players in the dictionary
        pandas_dataframe2 = pd.DataFrame({'bin_pct': pandas_series1 / self.stat_dictionary['pc'],
                                          avg_hover_stat_name: avg_hover_stat_list,
                                          'bin_ranges': bin_ranges})

        histogram_plot = go.Bar(
            x=pandas_dataframe2['bin_ranges'],
            y=pandas_dataframe2['bin_pct'],
            text = pandas_dataframe2[avg_hover_stat_name],
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5,
                )
            ),
            opacity=0.6
        )
        data = [histogram_plot]
        layout = go.Layout(
            title=plot_title,
            yaxis=dict(
                zeroline=False,
                title="Frequency"),
            xaxis=dict(
                zeroline=False,
                title="Bin Ranges: "+x_title)
        )
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename=plot_filename)
    # end hist1

    ################################
    ####### PRIVATE ROUTINES #######
    ################################

    # merging list of free agents with dictionary
    # if player is a free agent, change their free agent status to True
    def __merge_free_agents(self, fa_file):
        free_agent_list = open(fa_file)
        for free_agent in free_agent_list:
            free_agent = free_agent.strip('\r\n')
            if free_agent in self.player_dictionary:
                player = self.player_dictionary[free_agent]
                player['freeagent'] = True
    # end merge_fas

    # opens the json file and creates a dictionary
    # working with static json file 'playerlist.json'
    # playerlist.json retrieved from page source at https://baseballsavant.mlb.com/statcast_leaderboard
    # query: minimum batted balls events of 30, season 2016
    # would be better if json file is specified from user, but this is just for fun :)
    def __parse_and_dict(self, json_file):
        import json
        json1_file = open(json_file)
        json1_str = json1_file.read()

        # json.loads turns the json into a list of dictionaries
        json1_data = json.loads(json1_str)  # gets the whole dictionary
        player_counter = 0
        max_ahs_name = ""
        min_ahs_name = ""
        max_avg_hit_speed = 0
        min_avg_hit_speed = 100
        league_ahs = 0

        # useful for setting the axes of the brl_pa/avg hit speed graph
        max_brl_pa_name = ""
        max_brl_pa = 0

        # populate the dictionary player_dictionary
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

            # populating player_dictionary
            # sets a player's value in the dictionary
            self.player_dictionary[pname] = player
            player_counter += 1

            # min/max cases for stats
            # finding player with max avg hit speed
            # finding player with max amount of "barrels"/PA
            if player['avg_hit_speed'] > max_avg_hit_speed:
                max_avg_hit_speed = player['avg_hit_speed']
                max_ahs_name = pname
            if player['avg_hit_speed'] < min_avg_hit_speed:
                min_avg_hit_speed = player['avg_hit_speed']
                min_ahs_name = pname
            if player['brl_pa'] > max_brl_pa:
                max_brl_pa_name = player['name']
                max_brl_pa = player['brl_pa']
            # debugging statements go here:

            # end loop
        # more code

        ############ league-wide stats!!! ############
        self.stat_dictionary['pc'] = player_counter

        # name of player with max/min average hitting speed, max/min hitting speed
        self.stat_dictionary['max_avg_hs'] = max_avg_hit_speed
        self.stat_dictionary['max_avg_hs_name'] = max_ahs_name
        self.stat_dictionary['min_avg_hs'] = min_avg_hit_speed
        self.stat_dictionary['min_avg_hs_name'] = min_ahs_name

        self.stat_dictionary['max_brl_pa_name'] = max_brl_pa_name  # :)
        self.stat_dictionary['max_brl_pa'] = max_brl_pa

        self.stat_dictionary['league_ahs'] = float('%.2f' % (league_ahs / player_counter))  # truncate the float
    # end parse_and_dict

    # from csv file, add a player's BA to the dictionary
    def __fgstats_to_dict(self, csv_filename):
        import csv
        import os.path

        # would be safer to have script determine csv's encoding
        # manually determined in linux by "file -bi <filename>"
        csv_file = open(csv_filename, 'rt', encoding='utf-8')
        csv_reader = csv.reader(csv_file)
        not_in_dict = "Data/playersnotindict.txt"
        f1 = open(not_in_dict, 'a')
        nic = 0
        if not (os.path.isfile(not_in_dict)):
            nic = 1  # if nic == 1, file only written once
            print("creating file that contains players not in dictionary")
            f1.write("players not in dictionary:\n")

        for row in csv_reader:
            # csv file is currently formatted with the first line being "Name, Avg"
            # all subsequent elements are of that form
            # csv.reader formats each line ("row") as a list of strings
            # list indices:
            # 0: name, 1: team, 2: games played, 3: plate appearances, 4: HR
            # 5: runs, 6: rbi, 7: # stolen bases, 8: BB%, 9: K%, 10: ISO
            # 11: BABIP, 12: BA, 13: OBP, 14: SLG, 15: wOBA, 16: wRC+, 17: BsR
            # 18: off rating, 19: def rating, 20: fWAR, 21: playerID
            player_name = row[0]
            if player_name in self.player_dictionary:
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

                player = self.player_dictionary[player_name]
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
            elif os.path.isfile(not_in_dict) and nic == 1 and row[0] != 'Name':
                to_out = row[0] + '\n'
                f1.write(to_out)
        # for safety, close the file
        f1.close()
    # end adding_ba_to_dict


    # maps the shorthand key name to its full name
    # useful when sending data to the plotter; for the axes
    def __key_to_axes(self):
        import os
        import pickle
        filename = "Data/key_to_axes.pickle"
        if os.path.isfile(filename):
            print(filename, "found")
            with open(filename, 'rb') as ktahandle:
                self.axes_dictionary = pickle.load(ktahandle)
        else:
            print(filename, "not found")
            self.axes_dictionary['fbld'] = "Average FB/LD Exit Velocity (MPH)"
            self.axes_dictionary['k%'] = "K%"
            self.axes_dictionary['wRC+'] = "wRC+"
            self.axes_dictionary['season'] = "Season"
            self.axes_dictionary['brl_pa'] = "Barrels/Plate Appearances"
            self.axes_dictionary['fWAR'] = "fWAR"
            self.axes_dictionary['max_hit_speed'] = "Maximum Exit Velocity (MPH)"
            self.axes_dictionary['brl_percent'] = "Barrels/Batted Ball Events"
            self.axes_dictionary['avg_distance'] = "Average Distance (ft)"
            self.axes_dictionary['slg'] = "SLG"
            self.axes_dictionary['max_distance'] = "Maximum Distance (ft)"
            self.axes_dictionary['iso_str'] = "Isolated Power"
            self.axes_dictionary['ba'] = "Batting Average"
            self.axes_dictionary['obp'] = "On-Base Percentage"
            self.axes_dictionary['barrels'] = "Total Barreled Balls"
            self.axes_dictionary['attempts'] = "Batted Ball Events"
            self.axes_dictionary['babip'] = "BABIP"
            self.axes_dictionary['avg_hit_speed'] = "Average Exit Velocity (MPH)"
            self.axes_dictionary['avg_hr_distance'] = "Average Home Run Distance (ft)"
            self.axes_dictionary['min_hit_speed'] = "Minimum Hit Speed (MPH)"
            self.axes_dictionary['gb'] = "Average Groundball Exit Velocity (MPH"
            self.axes_dictionary['wOBA'] = "wOBA"
            self.axes_dictionary['BsR'] = "BsR"
            self.axes_dictionary['bb%'] = "bb%"
            with open(filename, 'wb') as ktahandle:
                pickle.dump(self.axes_dictionary, ktahandle, protocol=pickle.HIGHEST_PROTOCOL)
    # end key_to_axes()

    # second initialization routine: calls the parsers
    # checks if the source files exist and populates the dictionaries
    def __bb_parser(self):
        import os.path
        import sys
        import pickle

        # source files located in the Data directory:
        # 1. json file used to populate player_dictionary
        # 2. list of free agent players for the current offseason
        # 3. fangraphs leaderboard stats
        json_fname = "Data/playerlist.json"
        fa_file = "Data/fullfalist.txt"
        csvfname = "Data/fgleaders1.csv"

        # exit if source files not found
        if not (os.path.isfile(csvfname)):
            print("csv not found")
            sys.exit(1)
        if not (os.path.isfile(json_fname)):
            print("battedball json not found")
            sys.exit(1)
        if not (os.path.isfile(fa_file)):
            print("free agent list not found")
            sys.exit(1)

        # runs the parsers or retrieves the dicts from pickle files
        # using pickle to store player_dictionary and stat_dictionary
        pickled_player_dict = "Data/player_dictionary.pickle"
        pickled_stat_dict = "Data/stat_dictionary.pickle"
        self.__key_to_axes()  # creates the shorthands for axes creation - has its own pickle checker
        if os.path.isfile(pickled_player_dict) and os.path.isfile(pickled_stat_dict):
            print('pickled player_dictionary and stat_dictionary found')
            with open(pickled_player_dict, 'rb') as pdhandle:
                self.player_dictionary = pickle.load(pdhandle)
            with open(pickled_stat_dict, 'rb') as sdhandle:
                self.stat_dictionary = pickle.load(sdhandle)
        else:
            print('pickled player_dictionary and stat_dictionary file not found')
            self.__parse_and_dict(json_fname)  # populate player_dictionary
            self.__fgstats_to_dict(csvfname)
            self.__merge_free_agents(fa_file)  # adds free agent status to players
            with open(pickled_player_dict, 'wb') as pdhandle:
                pickle.dump(self.player_dictionary, pdhandle, protocol=pickle.HIGHEST_PROTOCOL)
            with open(pickled_stat_dict, 'wb') as sdhandle:
                pickle.dump(self.stat_dictionary, sdhandle, protocol=pickle.HIGHEST_PROTOCOL)
    # end parser

# end battedball class
