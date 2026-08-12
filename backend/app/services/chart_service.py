import pandas as pd
import plotly.express as px


def create_bar_chart(
    dataframe: pd.DataFrame,
    x_column: str,
    y_column: str
):

    figure = px.bar(
        dataframe,
        x=x_column,
        y=y_column,
        title=f"{y_column} by {x_column}"
    )

    return figure.to_json()


def create_line_chart(
    dataframe: pd.DataFrame,
    x_column: str,
    y_column: str
):

    figure = px.line(
        dataframe,
        x=x_column,
        y=y_column,
        title=f"{y_column} over {x_column}"
    )

    return figure.to_json()


def create_pie_chart(
    dataframe: pd.DataFrame,
    names_column: str,
    values_column: str
):

    figure = px.pie(
        dataframe,
        names=names_column,
        values=values_column,
        title=f"{values_column} by {names_column}"
    )

    return figure.to_json()