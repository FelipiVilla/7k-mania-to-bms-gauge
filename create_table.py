import hashlib
from pathlib import Path

def creatDict(folder:Path):
    maps = {
        ## hash : file name
    }

    osu_files = list(folder.rglob("*.osu"))
    for file in osu_files:
        maps[file_to_md5(file)] = file

    print(maps)

def file_to_md5(path:Path):
    md5 = hashlib.md5()
    with open(path, 'rb') as opened_file:
            md5.update(opened_file.read())
    return md5.hexdigest()


folder = Path() ## path for testing
creatDict(folder)