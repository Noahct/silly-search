# This builds a sqlite db to search for files and directories.
#run from root dir took 2 hrs 21 min and 26 sec.


import os, sys, time, sqlite3
##from watchdog.observers import Observer
##from watchdog.events import FileSystemEventHandler
##from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff

FILE_TO_SEARCH = input('Enter a file you want you search for: ')
DBNAME = 'files.db'
if sys.platform.startswith('darwin'):
    PATHTODB = "./filelogs/"
    STARTPATH = os.environ['HOME']
    PATHSTOSKIP = ['/dev', '/tmp']
if sys.platform.startswith('linux'):
    PATHTODB = "./filelogs/"
    STARTPATH = os.environ['HOME']
    PATHSTOSKIP = ['/dev', '/proc', '/tmp', '/sys']
if sys.platform.startswith('win32'):
    print('There is currently no Windows support for this program')
    sys.exit()


if not os.path.exists(PATHTODB): os.mkdir(PATHTODB)
CONN = sqlite3.connect(PATHTODB + DBNAME)
C = CONN.cursor()
C.execute('CREATE TABLE IF NOT EXISTS dir_tree(ID INTEGER PRIMARY KEY, Parent TEXT, Child TEXT);')
C.execute('CREATE TABLE IF NOT EXISTS child_dir_info(FullPath TEXT, Size INTEGER, CDate TEXT, MDate TEXT, ChildID INTEGER, FOREIGN KEY(ChildID) REFERENCES dir_tree(ID));')

def lookForFile(p):
    try:
        allFiles = [f for f in os.scandir(p) if f.is_file()]
        allDirs  = [d for d in os.scandir(p) if d.is_dir() and not d.is_symlink()]
    except PermissionError:
        return
    
    for f in allFiles:
        buildDB(p, f)

    fullPath = ''
    if p == '/':
        print(allDirs)
        allDirs = skipPath(allDirs)
        print(allDirs)
    for j in allDirs:
        buildDB(p, j)
        fullPath = lookForFile(j.path)
    
    return

def buildDB(parent, file):
    child = file.name
    st = file.stat()
    C.execute('INSERT INTO dir_tree(Parent, Child) VALUES(?,?)', (parent, child))
    C.execute("SELECT * FROM dir_tree WHERE Parent = ? AND Child = ?;", (parent, child))
    row = C.fetchone()
    rid = row[0]
    C.execute('INSERT INTO child_dir_info(FullPath, Size, CDate, MDate, ChildID) VALUES(?,?,?,?,?)', (file.path, st.st_size, st.st_atime, st.st_mtime, rid))


def skipPath(paths):
    for pa in paths:
        if pa.path in PATHSTOSKIP:
            paths.remove(pa)
    return paths

t1 = time.time()
lookForFile(STARTPATH)
C.execute("SELECT Child FROM dir_tree WHERE Child = ?;", (FILE_TO_SEARCH,))
rows = C.fetchall()
if rows == ():
    print('Could not find the file ' + FILE_TO_SEARCH)
else:
    for r in rows:
        print(str(r))

t2 = time.time()
total = t2 - t1
print('final time: %f' % (total))
CONN.commit()
CONN.close()
