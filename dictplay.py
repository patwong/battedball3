# for cli debugging purposes
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