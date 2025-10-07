import json
from .player import Player

SAVE_PATH = "game_save.json"

def save_player(player: Player, path: str = SAVE_PATH):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(player.to_dict(), f, indent=2)

def load_player(path: str = SAVE_PATH):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Player.from_dict(data)
    except Exception as e:
        print("Load error:", e)
        return None