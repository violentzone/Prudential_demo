import pandas as pd


def get_data(path: str):
    """
    Read CSV data from path and convert to json format row by row
    :param path: The path of csv file
    :return: Length of data in row
    """
    data = pd.read_csv(path)
    return data.to_dict(orient='records')
