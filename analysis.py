from osrparse import Replay, GameMode
from pathlib import Path


def analyse(path:Path):
    replay = Replay.from_path(path)

    if(replay.mode == GameMode.MANIA):
        r = replay
        print(r.beatmap_hash)

        
    


