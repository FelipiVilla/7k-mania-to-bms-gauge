import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

@dataclass(frozen=True)
class AppConfig:
    osu_dir: Path
    replays_dir: Path
    songs_dir: Path
    db_path: Path

def load_config() -> AppConfig:
    load_dotenv()

    osu_dir_str = os.getenv("OSU_PATH")
    if not osu_dir_str:
        raise ValueError("OSU_PATH not found in .env")

    osu_dir = Path(osu_dir_str)
    return AppConfig(
        osu_dir=osu_dir,
        replays_dir=osu_dir / "Replays",
        songs_dir=osu_dir / "Songs",
        db_path=Path(__file__).parent / "hashes.db",
    )