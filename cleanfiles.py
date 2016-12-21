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

cleanfiles()
