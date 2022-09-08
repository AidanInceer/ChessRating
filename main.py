from chessrating.extract import Extract
from chessrating.transform import Transform
from IPython.display import display


if __name__ == "__main__":
    username = "Ainceer"
    user_data_df = Extract.run_data_extract(username)
    display(user_data_df)
    final_df = Transform.clean(user_data_df, username)
    display(final_df)
