from osrparse import Replay, GameMode
from pathlib import Path
from beatmap_parser import replay_to_beatmap


def analyse(path:Path):
    replay = Replay.from_path(path)

    if(replay.mode == GameMode.MANIA):

        beatmap = replay_to_beatmap(replay)

        print(beatmap.title)
        print(beatmap.keys)
        print(beatmap.version)
        print(beatmap.od)

        

        
    


