from dataclasses import dataclass
from pathlib import Path
from osrparse import Replay
import sqlite3
from config import load_config

@dataclass
class HitObject:
    column: int
    time: int
    is_ln: bool
    end_time: int | None = None


@dataclass
class BeatmapData:
    title: str
    version: str
    keys: int
    od: float
    hit_objects: list[HitObject]


def parse_osu_file(osu_path: str | Path) -> BeatmapData:
    title = ""
    version = ""
    keys = 4
    od = 5.0
    hit_objects: list[HitObject] = []

    current_section = ""

    with open(osu_path, "r", encoding="utf-8-sig") as file:
        for raw_line in file:
            line = raw_line.strip()

            if not line or line.startswith("//"):
                continue

            if line.startswith("[") and line.endswith("]"):
                current_section = line
                continue

            if current_section == "[Metadata]":
                if line.startswith("Title:"):
                    title = line.split(":", 1)[1].strip()
                elif line.startswith("Version:"):
                    version = line.split(":", 1)[1].strip()

            elif current_section == "[Difficulty]":
                if line.startswith("CircleSize:"):
                    keys = int(float(line.split(":", 1)[1].strip()))
                elif line.startswith("OverallDifficulty:"):
                    od = float(line.split(":", 1)[1].strip())

            elif current_section == "[HitObjects]":
                parts = line.split(",")
                x = int(parts[0])
                time_ms = int(parts[2])
                obj_type = int(parts[3])

                column = min(keys - 1, max(0, int(x * keys / 512)))
                is_ln = bool(obj_type & 128)
                end_time = None

                if is_ln and len(parts) > 5:
                    end_time = int(parts[5].split(":")[0])

                hit_objects.append(
                    HitObject(
                        column=column,
                        time=time_ms,
                        is_ln=is_ln,
                        end_time=end_time,
                    )
                )

    return BeatmapData(
        title=title,
        version=version,
        keys=keys,
        od=od,
        hit_objects=hit_objects,
    )


def replay_to_beatmap(replay:Replay) -> BeatmapData:
    cfg = load_config()
    con = sqlite3.connect(cfg.db_path)
    cursor = con.cursor()
    cursor.execute("SELECT path FROM maps where hash = ?", (replay.beatmap_hash,))
    beatmap_path = cursor.fetchone()

    cursor.close()
    con.close()
    
    return parse_osu_file(beatmap_path[0])