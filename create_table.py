import hashlib
from pathlib import Path
import sqlite3

def creatDB(folder:Path):
    con = sqlite3.connect("hashes.db")
    con.execute("create table if not exists Maps(hash TEXT PRIMARY KEY, path TEXT)")
    maps = {
        ## hash : file name
    }

    osu_files = list(folder.rglob("*.osu"))
    for file in osu_files:
        maps[file_to_md5(file)] = str(file)

    con.executemany("INSERT OR REPLACE INTO maps VALUES(?,?)", maps.items())
    con.commit()
    con.close()

def file_to_md5(path:Path):
    md5 = hashlib.md5()
    with open(path, 'rb') as opened_file:
            md5.update(opened_file.read())
    return md5.hexdigest()

folder = Path(r"D:\osu!\Songs")
creatDB(folder)




