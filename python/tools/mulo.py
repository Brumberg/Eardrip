
import os
import json

def CreatePlayList(basefolder, filename, append):
    """creates a playlist by searching for mp3 files in a specified
    folder and its sub folders

    :param basefolder: specify the base folder to scan for mp3 files. All sub folders will be traversed, too
    :type: string
    :param filename: defines the target filename to store the list of music tracks in json format
    :type: basestring
    :param append: False=create new file, True=append list to existing file
    :type: boolean
    """
    i = 0
    ending = '.mp3'
    writeaccess = 'a' if append else 'w'
    try:
        with open(filename, writeaccess) as f:
            len_ending = len(ending)
            dict = {}
            for root, dirs, files in os.walk(basefolder, topdown=False):
                for name in files:
                    if name.endswith('.mp3'):
                        n = name[0:-len_ending]
                        print('Songindex= {ix}, title= {title}'.format(ix=i, title=n))
                        dict[i] = n
                        i = i+1

            json.dump(dict, f)
            
            print('-------------------','Number of songs: {}'.format(i))

    except IOError:
        print('Can not create file')
    return