import pandas as pd


def read_uploaded_file(file_path: str):

    if file_path.endswith(".csv"):
        dataframe = pd.read_csv(file_path)

    elif file_path.endswith(".xlsx"):
        dataframe = pd.read_excel(file_path)

    else:
        raise ValueError(
            "Only CSV and Excel files are supported."
        )

    return dataframe