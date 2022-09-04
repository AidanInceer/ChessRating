from dataclasses import dataclass
import chessdotcom
import json
import pandas as pd
import requests

@dataclass
class Extract:
    username: str

    def run_data_extract(self: str) -> None:
        urls = chessdotcom.get_player_game_archives(self.username).json
        username_list = []
        games_list = []

        for url in urls["archives"]:
            data = requests.get(url).json()

            for game_pgn in data["games"]:
                # chess_game_string = str(game_pgn["pgn"]).replace("\n", " ; ")
                games_list.append(game_pgn["pgn"])
                username_list.append(self.username)

        game_dict = {
            "username": username_list,
            "game_data": games_list
        }
        pgn_df = pd.DataFrame(game_dict)
        print(pgn_df["game_data"])

 
Extract.run_data_extract("Ainceer")
