from chessrating.extract import Extract
from chessrating.transform import Transform
import chessrating.plot


if __name__ == "__main__":
    username = "Ainceer"
    user_data = Extract()
    user_data_df = user_data.run_data_extract(username)
    print(user_data_df)
    game_data = Transform.clean(user_data_df, username)
