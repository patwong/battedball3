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

    # pdict.npy, statdict.py are our already populated dictionaries
    # will temporarily use to save computation time
    pdictfile = 'pdict.npy'
    statdictfile = 'statdict.npy'
    import os.path
    import numpy as np
    if os.path.isfile(pdictfile) and os.path.isfile(statdictfile):
        global pdict        # this allows access to global variable pdict/statdict
        global statdict     # without using pdict, creates a local scope pdict/statdict
        pdict = np.load(pdictfile).item()
        statdict = np.load(statdictfile).item()
    else:
        print('pdict and statdict file not found')
        parse_and_dict(json_fname)
        fa_file = "fullfalist.txt"
        merge_fas(fa_file)
        np.save(pdictfile, pdict)
        np.save(statdictfile, statdict)

    # to check if item is in dict, do this: ITEM in dict_name
    gsname = "Giancarlo Stanton"
    if gsname in pdict:
        gs1 = pdict[gsname]
        print (str(gs1['name']) + " had an average speed of " + str(gs1['gb']) + " mph on his groundballs")
    else:
        print (gsname + " isn't in the dictionary")
    if 'Bob Sutton' in pdict:
        print ("how??")
    else:
        print ("Bob Sutton not in the dictionary")

    pcname = "pc"
    if pcname in statdict:
        print ("There are " + str(statdict[pcname]) + " players recorded")
    else:
        print (pcname + " isn't in the stat dictionary")

    # use plotter function to produce scatter plot
    bbplotter.fa_to_plot(pdict, statdict)

    # !!debugging statements!!

    # dictionaries are mutable
    # passing a dictionary to a function passes the object, not copy
    # if 'surprise' in statdict:
    #     print (statdict['surprise'])
    # else:
    #    print ("There is no surprise :(")
# end main

# run program
main()
