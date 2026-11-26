from analysis import analyse
from replay_added_call import ReplayAdded
from config import load_config

if __name__ == "__main__":
    cfg = load_config()
    replay_path = cfg.replays_dir
    ReplayAdded(replay_path, analyse)


## need to create the full table and pass it to sqlite3,