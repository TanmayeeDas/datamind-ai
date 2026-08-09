import pandas as pd


UPLOADED_DATAFRAME = None
UPLOADED_FILENAME = None


def store_dataframe(dataframe: pd.DataFrame, filename: str):

    global UPLOADED_DATAFRAME
    global UPLOADED_FILENAME

    UPLOADED_DATAFRAME = dataframe
    UPLOADED_FILENAME = filename


def get_dataframe():

    return UPLOADED_DATAFRAME


def get_filename():

    return UPLOADED_FILENAME