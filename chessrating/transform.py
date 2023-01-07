from dataclasses import dataclass
from datetime import datetime

import chess
import chess.engine
import chess.pgn
import pandas as pd


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
                "time_control": time_cont,
                "user_rating": user_rating,
                "game_date": game_date,
                "game_date_time": game_datetime,
            }
            filtered_game_list.append(game_dict)
        headers = [
            "username",
            "time_control",
            "user_rating",
            "game_date",
            "game_date_time",
            "max_rating",
            "min_rating",
            "mean_rating",
        ]
        core_df = pd.DataFrame(filtered_game_list)
        df_max = core_df.groupby(["time_control", "game_date"]).max("user_rating")
        df_min = core_df.groupby(["time_control", "game_date"]).min("user_rating")
        df_mean = core_df.groupby(["time_control", "game_date"]).mean("user_rating")
        df_join_max = pd.merge(core_df, df_max, on=["time_control", "game_date"])
        df_join_max.rename(columns={"user_rating_y": "max_rating"}, inplace=True)
        df_join_min = pd.merge(df_join_max, df_min, on=["time_control", "game_date"])
        df_join_min.rename(columns={"user_rating_x": "user_rating"}, inplace=True)
        df_join_mean = pd.merge(df_join_min, df_mean, on=["time_control", "game_date"])
        df_join_mean.rename(columns={"user_rating_y": "mean_rating"}, inplace=True)
        df_join_mean.to_csv(
            r"./data/game_data.csv", sep=",", index=False, header=headers
        )
        return df_join_mean
