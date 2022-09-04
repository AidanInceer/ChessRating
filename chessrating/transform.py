from dataclasses import dataclass
import chessdotcom
import pandas as pd
import chess
import chess.engine
import chess.pgn
from datetime import datetime


@dataclass
class Transform:
    @staticmethod
    def clean(user_data_df: pd.DataFrame, username: str):
        path_temppgn = r"./data/temp.pgn"
        filtered_game_list = []
        for game_num, game in enumerate(user_data_df["game_data"]):
            print(game_num, end="\r")
            with open(path_temppgn, mode="w") as temp_file:
                temp_file.write(str(game))

            chess_game_pgn = open(path_temppgn)
            chess_game = chess.pgn.read_game(chess_game_pgn)
            time_cont = chess_game.headers["TimeControl"]
            white = chess_game.headers["White"]
            black = chess_game.headers["Black"]
            player = "white" if white == username else "black"
            ratingwhite = int(chess_game.headers["WhiteElo"])
            ratingblack = int(chess_game.headers["BlackElo"])
            user_rating = ratingwhite if player == "White" else ratingblack
            game_date = chess_game.headers["UTCDate"]
            game_time = chess_game.headers["UTCTime"]
            game_date_time = f"{game_date} {game_time}"
            game_datetime = datetime.strptime(game_date_time, "%Y.%m.%d %H:%M:%S")

            game_dict = {
                "username": username,
                "colour": player,
                "time_control": time_cont,
                "user_rating": user_rating,
                "game_date_time": game_datetime,
            }
            filtered_game_list.append(game_dict)

        headers = [
            "username",
            "colour",
            "time_control",
            "user_rating",
            "game_date_time",
        ]

        game_data_df = pd.DataFrame(filtered_game_list)
        game_data_df.to_csv(
            r"./data/game_data.csv", sep=",", index=False, header=headers
        )
