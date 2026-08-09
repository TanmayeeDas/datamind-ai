import pandas as pd


def analyze_dataframe(
    dataframe: pd.DataFrame,
    question: str
):

    question_lower = question.lower()

    # Count rows
    if "how many rows" in question_lower:
        return {
            "type": "text",
            "answer": f"The dataset contains {len(dataframe)} rows."
        }

    # Show columns
    if "columns" in question_lower:
        return {
            "type": "text",
            "answer": (
                "The dataset contains these columns: "
                + ", ".join(dataframe.columns.astype(str))
            )
        }

    # Show first rows
    if (
        "show first" in question_lower
        or "show top" in question_lower
    ):
        return {
            "type": "table",
            "columns": list(dataframe.columns),
            "rows": dataframe.head(5).values.tolist()
        }

    return {
        "type": "text",
        "answer": (
            "I could not understand the question yet. "
            "More data analysis capabilities will be added next."
        )
    }