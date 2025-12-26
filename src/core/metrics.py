import pandas as pd


def total_revenue(df: pd.DataFrame) -> float:
    """
    Calculate total revenue from the dataset.
    """
    return df["revenue"].sum()


def total_units_sold(df: pd.DataFrame) -> int:
    """
    Calculate total units sold from the dataset.
    """
    return df["units_sold"].sum()


def revenue_by_dimension(df: pd.DataFrame, dimension: str) -> pd.Series:
    """
    Calculate total revenue grouped by a given dimension
    (e.g., region, salesperson, product).
    """
    return df.groupby(dimension)["revenue"].sum().sort_values(ascending=False)


def revenue_over_time(df: pd.DataFrame, freq: str = "M") -> pd.Series:
    """
    Calculate revenue over time.

    freq examples:
    - 'D' = daily
    - 'M' = monthly
    - 'Q' = quarterly
    """
    df_copy = df.copy()
    df_copy["order_date"] = pd.to_datetime(df_copy["order_date"])
    return (
        df_copy
        .groupby(pd.Grouper(key="order_date", freq=freq))["revenue"]
        .sum()
        .sort_index()
    )


def revenue_change(current_value: float, previous_value: float) -> float:
    """
    Calculate percentage change between two values.
    """
    if previous_value == 0:
        return 0.0
    return ((current_value - previous_value) / previous_value) * 100
