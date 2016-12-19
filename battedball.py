# Python3 version of code
import bbplotter
import json

# global dictionaries
# pdict: conversion of json file to dictionary of players and their batted ball numbers
# statdict: stores certain playerbase stats, i.e. number of players in pdict
pdict = {}
statdict = {}


# merging list of free agents with dictionary
# if player is a free agent, change their free agent status to True
def merge_fas(fa_file):
    falist = open(fa_file)
    for fa in falist:
        f_a = fa.strip('\r\n')
        if f_a in pdict:
            player = pdict[f_a]
            player['freeagent'] = True      # this actually changes the value of the player in pdict
# end merge_fas


# opens the json file and creates a dictionary
# working with static jason file 'playerlist.json'
# playerlist.json retrieved from page source at https://baseballsavant.mlb.com/statcast_leaderboard
# query: minimum batted balls events of 30, season 2016
# would be better if json file is specified from user, but this is just for fun :)
def parse_and_dict(json_fname):
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
        ahd = str(player['avg_hr_distance'])                # manually changed null to "null" in list
        if ahd.lower() == 'null':               # sometimes ahd is null; players w/o hr
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
        pdict[pname] = player
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
    statdict['pc'] = playercounter

    # name of player with max/min average hitting speed, max/min hitting speed
    statdict['max_avg_hs'] = mavahs
    statdict['max_avg_hs_name'] = mavahs_name
    statdict['min_avg_hs'] = minahs
    statdict['min_avg_hs_name'] = minahs_name

    statdict['max_brl_pa_name'] = max_brl_pa_name       # :)
    statdict['max_brl_pa'] = max_brl_pa

    statdict['league_ahs'] = float('%.2f' % (league_ahs / playercounter))   # truncate the float
# end parse_and_dict


# from csv file, add a player's BA to the dictionary
def fgstats_to_dict(csv_fname):
    import csv
    import os.path

    # csvfile = open(csv_fname, 'rt', encoding='us-ascii')
    csvfile = open(csv_fname, 'rt', encoding='utf-8')
    csvreader = csv.reader(csvfile)
    notindict = "playersnotindict.txt"
    nic = 0
    if not(os.path.isfile(notindict)):
        nic = 1     # if nic == 1, file only written once
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
        if player_name in pdict:
            bb_percent = float(row[8].strip(' %'))/100
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

            player = pdict[player_name]
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
def cleanfiles():
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
#end cleanfiles()


# the main machine
# battedball.py populates player dictionary "pdict" and stat dictionary "statdict"
#   as it iterates through the json file of players
def main():
    # dictionary is a lot faster than list
    # will be useful when updating a player's FA stats
    # dictionary AO(1) speed to update, access
    # list is O(n) update, access

    # populate pdict
    json_fname = "playerlist.json"

    # using pickle to store pdict and statdict
    import os.path
    import pickle
    pickled_pdict = "pdict.pickle"
    pickled_statdict = "statdict.pickle"
    if os.path.isfile(pickled_pdict) and os.path.isfile(pickled_statdict):
        print('pickled pdict and statdict found')
        with open(pickled_pdict, 'rb') as pdhandle:
            # need to declare pdict and statdict as global to access the global variable
            # otherwise will access a variable in the local scope
            global pdict
            pdict = pickle.load(pdhandle)
        with open(pickled_statdict, 'rb') as sdhandle:
            global statdict
            statdict = pickle.load(sdhandle)
    else:
        print('pickled pdict and statdict file not found')
        parse_and_dict(json_fname)
        fa_file = "fullfalist.txt"
        merge_fas(fa_file)
        csvfname = "fgleaders1.csv"         # adding fangraphs leaderboard stats to player stat dictionary
        if os.path.isfile(csvfname):
            fgstats_to_dict(csvfname)
        else:
            print("csv not found")
        with open(pickled_pdict, 'wb') as pdhandle:
            pickle.dump(pdict, pdhandle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(pickled_statdict, 'wb') as sdhandle:
            pickle.dump(statdict, sdhandle, protocol=pickle.HIGHEST_PROTOCOL)



    # to check if item is in dict, do this: ITEM in dict_name
    gsname = "Giancarlo Stanton"
    if gsname in pdict:
        gs1 = pdict[gsname]
        print (str(gs1['name']) + " had an average speed of " + str(gs1['gb']) + " mph on his groundballs")
    else:
        print (gsname + " isn't in the dictionary")

    pcname = "pc"
    if pcname in statdict:
        print ("There are " + str(statdict[pcname]) + " players recorded")
    else:
        print (pcname + " isn't in the stat dictionary")

    # testing adding_ba_to_dict()
    miketrout = "Mike Trout"
    if miketrout in pdict:
        print(miketrout + " has a batting average of " + str(pdict[miketrout]['ba']) + " and an on-base percentage of " + str(pdict[miketrout]['obp']))
    else:
        print(miketrout + " not found")

    # use plotter function to produce scatter plot
    # bbplotter.fa_to_plot(pdict, statdict)

    # clean directory
    # cleanfiles()

    # update dictionaries
    # with open(pickled_pdict, 'wb') as pdhandle:
    #     pickle.dump(pdict, pdhandle, protocol=pickle.HIGHEST_PROTOCOL)
    # with open(pickled_statdict, 'wb') as sdhandle:
    #     pickle.dump(statdict, sdhandle, protocol=pickle.HIGHEST_PROTOCOL)

    # !!debugging statements!!

    # dictionaries are mutable
    # passing a dictionary to a function passes the object, not copy
    # if 'surprise' in statdict:
    #     print (statdict['surprise'])
    # else:
    #    print ("There is no surprise :(")
# end main

# time.time() times the program
# seems like saving the dictionaries into dict doesn't save any computation time
# might be because reading from the file is slower than populating a dictionary

# import time
# start_time = time.time()

# run program
main()

# end_time = time.time()
# bbruntime = end_time - start_time
# print("runtime was: " + str(bbruntime))
