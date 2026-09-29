import pandas as pd


def analyze_dataframe(
    dataframe: pd.DataFrame,
    question: str
):
    df = dataframe.copy()
    q = question.lower().strip()

    # 1. Count rows
    if "how many rows" in q or "row count" in q:
        return {
            "type": "text",
            "answer": f"The dataset contains {len(df)} rows."
        }

    # 2. Show columns
    if "columns" in q:
        return {
            "type": "text",
            "answer": "Columns: " + ", ".join(
                df.columns.astype(str)
            )
        }

    # 3. Show first or top 5 rows
    if "show first" in q or "show top" in q:
        return {
            "type": "table",
            "columns": list(df.columns),
            "rows": df.head(5).values.tolist()
        }

    # 4. Numeric column summary
    if "average" in q or "mean" in q:
        for col in df.select_dtypes(include="number").columns:
            if col.lower() in q:
                return {
                    "type": "text",
                    "answer": (
                        f"Average {col}: "
                        f"{df[col].mean():,.2f}"
                    )
                }

    # 5. Sum of a numeric column
    if "total" in q or "sum" in q:
        for col in df.select_dtypes(include="number").columns:
            if col.lower() in q:
                return {
                    "type": "text",
                    "answer": (
                        f"Total {col}: "
                        f"{df[col].sum():,.2f}"
                    )
                }

    return {
        "type": "text",
        "answer": (
            "This question is not supported by the "
            "current analysis engine yet."
        )
    }