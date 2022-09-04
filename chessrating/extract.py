import chessdotcom
import json
import pandas as pd
import requests


def run_data_extract(username: str) -> None:
    urls = chessdotcom.get_player_game_archives(username).json
    username_list = []
    games_list = []

    for url in urls["archives"]:
        data = requests.get(url).json()

        for game_pgn in data["games"]:
            # chess_game_string = str(game_pgn["pgn"]).replace("\n", " ; ")
            games_list.append(game_pgn["pgn"])
            username_list.append(username)

    game_dict = {
        "username": username_list,
        "game_data": games_list
    }
    pgn_df = pd.DataFrame(game_dict)
    print(pgn_df["game_data"])

 
run_data_extract("Ainceer")
