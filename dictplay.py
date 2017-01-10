# for cli debugging purposes
# opens the dictionary files stored in pickle files
import pickle
import os
pdict = {}
statdict = {}

pickled_pdict = "Data/pdict.pickle"
pickled_statdict = "Data/statdict.pickle"
if os.path.isfile(pickled_pdict) and os.path.isfile(pickled_statdict):
    print('pickled pdict and statdict found')
    with open(pickled_pdict, 'rb') as pdhandle:
        # need to declare pdict and statdict as global to access the global variable
        # otherwise will access a variable in the local scope
        # global pdict
        pdict = pickle.load(pdhandle)
    with open(pickled_statdict, 'rb') as sdhandle:
        # global statdict
        statdict = pickle.load(sdhandle)
# end if

# given player name, list his stats
def find(pname):
    if pname in pdict:
        player = pdict[pname]
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
