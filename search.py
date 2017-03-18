# This searches the file system recursivly.
# i'll use REs and db entries for faster searches

import os, time, re, sqlite3
##from watchdog.observers import Observer
##from watchdog.events import FileSystemEventHandler
##from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
##from PyQt5 import QtWidgets


FILEN = 'files.db' #input('Enter a file you want you search for: ')
PATH = '/Users/noah/' #Volumes/KRAKEN) #Users/noah) #home/noah)
PATHSTOSKIP = ['/dev']#, '/Volumes/noah-backups']
CONN = sqlite3.connect(FILEN)
C = CONN.cursor()
C.execute('PRAGMA foreign_keys=ON;')
C.execute('CREATE TABLE IF NOT EXISTS dir_tree(ID INTEGER PTIMARY KEY, Parent TEXT, Child TEXT);')
C.execute('CREATE TABLE IF NOT EXISTS child_dir_info(FullPath TEXT, Size INTEGER, CDate TEXT, MDate TEXT, ChildID INTEGER, FOREIGN KEY(ChildID) REFERENCES dir_tree(ID0));')

def lookForFile(p):
    try:
        allFiles = [f for f in os.scandir(p) if f.is_file()]
        allDirs  = [d for d in os.scandir(p) if d.is_dir() and not d.is_symlink()]
    except PermissionError:
        return 

    for f in allFiles:
        buildDB(p, f)

    fullPath = ''
    allDirs = skipPath(allDirs)
    for j in allDirs:
        buildDB(p, j)
        fullPath = lookForFile(j)
 #       if fullPath: return fullPath
    
    return

def buildDB(parent, file):
    child = file.name
    st = file.stat()
    C.execute('INSERT INTO dir_tree(Parent, Child) VALUES(?,?)', (parent, child))
    rid = C.execute("SELECT ID FROM dir_tree WHERE parent = '%s' AND child = '%s';", (parent, child))
    C.execute('INSERT INTO child_dir_info(FullPath, Size, CDate, MDate, ChildID) VALUES(?,?,?,?,?)', (file.path, st.st_size, st.st_birthtime, st.st_mtime, rid))


def skipPath(paths):
    for pa in PATHSTOSKIP:
        if pa in paths:
            paths.remove(pa)
    return paths

t1 = time.time()
lookForFile(PATH)
rows = C.execute("SELECT * FROM dir_tree WHERE child = '%s';", (FILEN))
print(str(rows))
if rows == ():
    print('Could not find the file ' + FILEN)
t2 = time.time()
total = t2 - t1
print('final time: %f' % (total))
CONN.commit()
CONN.close()
