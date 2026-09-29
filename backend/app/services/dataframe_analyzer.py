import pandas as pd

from app.services.llm_service import generate_analysis_plan


def analyze_dataframe(
    dataframe: pd.DataFrame,
    question: str
):
    df = dataframe.copy()

    try:
        plan = generate_analysis_plan(question, df)
        print("AI ANALYSIS PLAN:", plan)

        operation = plan.get("operation")
        column = plan.get("column")
        aggregation = plan.get("aggregation")
        group_by = plan.get("group_by")
        limit = plan.get("limit", 5)

        # Validate column names
        valid_columns = df.columns.astype(str).tolist()

        if column is not None and column not in valid_columns:
            raise ValueError("Invalid column name")

        if group_by is not None and group_by not in valid_columns:
            raise ValueError("Invalid grouping column")

        # 1. Count rows
        if operation == "count_rows":
            return {
                "type": "text",
                "answer": f"The dataset contains {len(df)} rows."
            }

        # 2. List columns
        if operation == "list_columns":
            return {
                "type": "text",
                "answer": "Columns: " + ", ".join(valid_columns)
            }

        # 3. Show first N rows
        if operation == "head":
            limit = max(1, min(int(limit), 100))
            result = df.head(limit)

        # 4. Aggregate a numeric column
        elif operation == "aggregate":
            if column is None:
                raise ValueError("Missing column")

            if aggregation not in ["sum", "mean", "min", "max", "count"]:
                raise ValueError("Invalid aggregation")

            series = df[column]

            if aggregation != "count":
                series = pd.to_numeric(series, errors="coerce")

            value = getattr(series, aggregation)()

            return {
                "type": "text",
                "answer": f"{aggregation.title()} of {column}: {value:,.2f}"
            }

        # 5. Group and aggregate
        elif operation == "groupby_aggregate":
            if not column or not group_by:
                raise ValueError("Missing analysis columns")

            if aggregation not in ["sum", "mean", "min", "max", "count"]:
                raise ValueError("Invalid aggregation")

            working_df = df.copy()

            if aggregation != "count":
                working_df[column] = pd.to_numeric(
                    working_df[column],
                    errors="coerce"
                )

            result = (
                working_df.groupby(group_by, dropna=False)[column]
                .agg(aggregation)
                .reset_index()
            )

            result.columns = [group_by, f"{aggregation}_{column}"]

            result = result.sort_values(
                by=result.columns[-1],
                ascending=False
            )

        # 6. Filter rows
        elif operation == "filter":
            condition = plan.get("filter")

            if not condition:
                raise ValueError("Missing filter condition")

            filter_column = condition.get("column")
            operator = condition.get("operator")
            value = condition.get("value")

            if filter_column not in valid_columns:
                raise ValueError("Invalid filter column")

            series = df[filter_column]

            if operator == "equals":
                result = df[series.astype(str) == str(value)]

            elif operator == "greater_than":
                result = df[
                    pd.to_numeric(series, errors="coerce")
                    > float(value)
                ]

            elif operator == "less_than":
                result = df[
                    pd.to_numeric(series, errors="coerce")
                    < float(value)
                ]

            elif operator == "contains":
                result = df[
                    series.astype(str).str.contains(
                        str(value),
                        case=False,
                        na=False,
                        regex=False
                    )
                ]

            else:
                raise ValueError("Invalid filter operator")

        # 7. Top N rows
        elif operation == "top_n":
            if column is None:
                raise ValueError("Missing ranking column")

            limit = max(1, min(int(limit), 100))

            result = df.sort_values(
                by=column,
                ascending=False
            ).head(limit)

        else:
            raise ValueError("Unsupported analysis operation")

        # Return a table for operations producing rows
        result = result.astype(object).where(
            pd.notna(result),
            None
        )

        chart = None
        # Select chart type based on the user's question
        question_lower = question.lower()

        if any(word in question_lower for word in [
            "distribution",
            "proportion",
            "percentage",
            "share",
            "contribution"
        ]):
            chart_type = "pie"

        elif any(word in question_lower for word in [
            "over time",
            "trend",
            "monthly",
            "daily",
            "yearly",
            "by month",
            "by year"
        ]):
            chart_type = "line"

        else:
            chart_type = "bar"

        print("QUESTION:", question)
        print("CHART TYPE SELECTED:", chart_type)
        print("OPERATION:", operation)

        # Recommend a chart for grouped analysis
        if operation == "groupby_aggregate":
            chart = {
                "type": chart_type,
                "x": group_by,
                "y": f"{aggregation}_{column}",
                "title": f"{aggregation.title()} of {column} by {group_by}"
            }

        # Recommend a chart for top-N analysis
        elif operation == "top_n":
            categorical_columns = [
                col for col in result.columns
                if not pd.api.types.is_numeric_dtype(result[col])
            ]

            if categorical_columns:
                chart = {
                    "type": chart_type,
                    "x": categorical_columns[0],
                    "y": column,
                    "title": f"Top {limit} by {column}"
                }

        result = result.astype(object).where(
            pd.notna(result),
            None
        )

        return {
            "type": "table",
            "columns": result.columns.astype(str).tolist(),
            "rows": result.values.tolist(),
            "chart": chart
        }

    except Exception as e:
        return {
            "type": "text",
            "answer": (
                "I could not complete this analysis. "
                "Please try rephrasing your question. "
                f"Details: {str(e)}"
            )
        }