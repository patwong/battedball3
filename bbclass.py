class bbclass:
    """
    modularizes the battedball method collection into a class object
    bbclass can only be defined if the valid json, csv, and txt files
    are located in the Data subdirectory of the working folder
    """

    def __init__(self):
        self.bbparser()
        self.pdict = {}
        self.statdict = {}
        self.axesdict = {}

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

        csvfile = open(csv_fname, 'rt', encoding='utf-8')
        csvreader = csv.reader(csvfile)
        notindict = "playersnotindict.txt"
        nic = 0
        if not (os.path.isfile(notindict)):
            nic = 1  # if nic == 1, file only written once
            print("creating file that contains players not in dictionary")
            f1 = open(notindict, 'a')
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

            elif os.path.isfile(notindict) and nic == 1 and row[0] != 'Name':
                to_out = row[0] + '\n'
                f1.write(to_out)

        # for safety, close the file
        if nic == 1:
            f1.close()
    # end adding_ba_to_dict

    # remove all auxiliary files created by my program
    # list: playersnotindict.txt, pdict.pickle, statdict.pickle
    def cleanfiles(self):
        import os
        filedir = os.listdir()
        print("files currently in directory\n" + str(filedir))
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
                # random_player = pdict.popitem()[1]

    # end key_to_axes()


    # other initialization routine
    def bbparser(self):
        """
        the other initialization routine
        checks if the source files exist and populates the dictionaries
        """
        import os.path
        import sys
        import pickle

        # source files located in the Data directory
        # json file used to populate pdict
        # list of free agent players for the current offseason
        # fangraphs leaderboard stats
        json_fname = "Data/playerlist.json"
        fa_file = "Data/fullfalist.txt"
        csvfname = "Data/fgleaders1.csv"

        if not(os.path.isfile(csvfname)):
            print("csv not found")
            sys.exit(1)
        if not(os.path.isfile(json_fname)):
            print("battedball json not found")
            sys.exit(1)
        if not(os.path.isfile(fa_file)):
            print("free agent list not found")
            sys.exit(1)

        # this block runs the parsers or retrieves the dicts from pickle files
        # using pickle to store pdict and statdict
        pickled_pdict = "Data/pdict.pickle"
        pickled_statdict = "Data/statdict.pickle"
        self.key_to_axes()   # creates the shorthands for axes creation
        if os.path.isfile(pickled_pdict) and os.path.isfile(pickled_statdict):
            print('pickled pdict and statdict found')
            with open(pickled_pdict, 'rb') as pdhandle:
                self.pdict = pickle.load(pdhandle)
            with open(pickled_statdict, 'rb') as sdhandle:
                self.statdict = pickle.load(sdhandle)
        else:
            print('pickled pdict and statdict file not found')
            self.parse_and_dict(json_fname)  # populate pdict
            self.fgstats_to_dict(csvfname)
            self.merge_fas(fa_file)  # adds free agent status to players
            with open(pickled_pdict, 'wb') as pdhandle:
                pickle.dump(self.pdict, pdhandle, protocol=pickle.HIGHEST_PROTOCOL)
            with open(pickled_statdict, 'wb') as sdhandle:
                pickle.dump(self.statdict, sdhandle, protocol=pickle.HIGHEST_PROTOCOL)

# end bbclass
