# This searches the file system recursivly.
# i'll use REs and db entries for faster searches

import os, time, re, sys, sqlite3

##from watchdog.observers import Observer
##from watchdog.events import FileSystemEventHandler
##from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff


FILEN = 'qtdemo.py' #input('Enter a file you want you search for: ')
PATH = '/' #Volumes/KRAKEN) #Users/noah) #home/noah)
PATHSTOSKIP = ['/dev', '/Volumes/noah-backups']

def lookForFile(p):
    try:
        allFiles = [f.path for f in os.scandir(p) if f.is_file()]
        allDirs  = [d.path for d in os.scandir(p) if d.is_dir() and not d.is_symlink()]
    except PermissionError:
        return 

    for f in allFiles:
        if os.path.basename(f) == FILEN:
            return f

    fullPath = ''
    allDirs = skipPath(allDirs)
    for j in allDirs:
        fullPath = lookForFile(j)
        if fullPath: return fullPath
    
    return

def skipPath(paths):
    for pa in PATHSTOSKIP:
        if pa in paths:
            paths.remove(pa)
    return paths

t1 = time.time()
fpath = lookForFile(PATH)
if fpath != None:
    print(str(fpath))
else:
    print('Could not find the file ' + FILEN)
t2 = time.time()
total = t2 - t1
print('final time: %f' % (total))
