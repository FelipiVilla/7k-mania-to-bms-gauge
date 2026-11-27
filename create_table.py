import hashlib
from pathlib import Path
import sqlite3
import os

def file_to_md5(path:str) -> str:
    md5 = hashlib.md5()
    with open(path, 'rb') as opened_file:
            md5.update(opened_file.read())
    return md5.hexdigest()

def find_osu_files(songs_folder: Path) -> list[str]:
    osu_files = []
    folders_to_visit = [str(songs_folder)]

    while folders_to_visit:
        current_folder = folders_to_visit.pop()
        with os.scandir(current_folder) as entries:
            for entry in entries:
                if entry.is_dir():
                    folders_to_visit.append(entry.path)
                elif entry.name.endswith(".osu"):
                    osu_files.append(entry.path)
    return osu_files

def create_db(folder:Path):
    con = sqlite3.connect("hashes.db")
    con.execute("CREATE TABLE if NOT EXISTS maps(hash TEXT PRIMARY KEY, path TEXT NOT NULL, mtime REAL NOT NULL)")

    maps = []
    osu_files = find_osu_files(folder)
    for file in osu_files:
        maps.append((file_to_md5(file), file, os.path.getmtime(file),))
        

    con.executemany("INSERT OR REPLACE INTO maps values (?,?,?)", maps )
    
    con.commit()
    con.close()



folder = Path() ## path for songs
create_db(folder)




