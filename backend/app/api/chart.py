from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd

from app.services.file_cache import get_dataframe
from app.services.chart_service import (
    create_bar_chart,
    create_line_chart,
    create_pie_chart
)


router = APIRouter(
    prefix="/chart",
    tags=["Charts"]
)


class ChartRequest(BaseModel):
    chart_type: str
    x_column: str
    y_column: str


@router.post("/generate")
def generate_chart(request: ChartRequest):

    dataframe = get_dataframe()

    if dataframe is None:
        raise HTTPException(
            status_code=404,
            detail="Please upload a CSV or Excel file first."
        )

    if request.x_column not in dataframe.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Column '{request.x_column}' not found."
        )

    if request.y_column not in dataframe.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Column '{request.y_column}' not found."
        )

    if request.chart_type == "bar":

        chart = create_bar_chart(
            dataframe,
            request.x_column,
            request.y_column
        )

    elif request.chart_type == "line":

        chart = create_line_chart(
            dataframe,
            request.x_column,
            request.y_column
        )

    elif request.chart_type == "pie":

        chart = create_pie_chart(
            dataframe,
            request.x_column,
            request.y_column
        )

    else:

        raise HTTPException(
            status_code=400,
            detail="Supported chart types: bar, line, pie."
        )

    return {
        "chart": chart
    }



class DatabaseChartRequest(BaseModel):
    chart_type: str
    x_column: str
    y_column: str
    columns: list[str]
    rows: list[list]


@router.post("/generate-result")
def generate_database_result_chart(
    request: DatabaseChartRequest
):

    dataframe = pd.DataFrame(
        request.rows,
        columns=request.columns
    )

    if request.x_column not in dataframe.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Column '{request.x_column}' not found."
        )

    if request.y_column not in dataframe.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Column '{request.y_column}' not found."
        )

    if request.chart_type == "bar":

        chart = create_bar_chart(
            dataframe,
            request.x_column,
            request.y_column
        )

    elif request.chart_type == "line":

        chart = create_line_chart(
            dataframe,
            request.x_column,
            request.y_column
        )

    elif request.chart_type == "pie":

        chart = create_pie_chart(
            dataframe,
            request.x_column,
            request.y_column
        )

    else:

        raise HTTPException(
            status_code=400,
            detail="Supported chart types: bar, line, pie."
        )

    return {
        "chart": chart
    }