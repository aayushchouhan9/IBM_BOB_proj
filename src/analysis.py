"""
analysis.py
-----------
Computes KPIs and group-level summaries from the cleaned DataFrame.
Every function returns a pandas DataFrame or a plain scalar/dict.
"""

import pandas as pd


# ──────────────────────────────────────────────────────────────────────────────
# 1.  TOP-LEVEL KPIs
# ──────────────────────────────────────────────────────────────────────────────

def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Return a dict of headline KPIs shown in the dashboard metric cards.
    """
    return {
        "total_revenue":        round(df["purchase_amount"].sum(), 2),
        "total_purchases":      len(df),
        "avg_purchase_amount":  round(df["purchase_amount"].mean(), 2),
        "avg_rating":           round(df["rating"].mean(), 2),
        "unique_customers":     df["customer_id"].nunique(),
        "subscription_rate":    round(df["is_subscriber"].mean() * 100, 1),
        "discount_rate":        round(df["has_discount"].mean() * 100, 1),
        "avg_previous_purchases": round(df["previous_purchases"].mean(), 1),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 2.  GROUPED SUMMARIES
# ──────────────────────────────────────────────────────────────────────────────

def _revenue_summary(df: pd.DataFrame, by: str | list) -> pd.DataFrame:
    """Generic helper: group by `by`, aggregate revenue + count + avg."""
    grouped = (
        df.groupby(by, observed=True)
        .agg(
            total_revenue   =("purchase_amount", "sum"),
            purchase_count  =("purchase_amount", "count"),
            avg_purchase    =("purchase_amount", "mean"),
            avg_rating      =("rating",          "mean"),
        )
        .reset_index()
    )
    grouped["total_revenue"] = grouped["total_revenue"].round(2)
    grouped["avg_purchase"]  = grouped["avg_purchase"].round(2)
    grouped["avg_rating"]    = grouped["avg_rating"].round(2)
    return grouped.sort_values("total_revenue", ascending=False)


def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return _revenue_summary(df, "category")


def sales_by_item(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    return _revenue_summary(df, "item").head(top_n)


def sales_by_season(df: pd.DataFrame) -> pd.DataFrame:
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    result = _revenue_summary(df, "season")
    result["season"] = pd.Categorical(result["season"],
                                      categories=season_order, ordered=True)
    return result.sort_values("season")


def sales_by_gender(df: pd.DataFrame) -> pd.DataFrame:
    return _revenue_summary(df, "gender")


def sales_by_age_group(df: pd.DataFrame) -> pd.DataFrame:
    return _revenue_summary(df, "age_group")


def sales_by_location(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    return _revenue_summary(df, "location").head(top_n)


def sales_by_subscription(df: pd.DataFrame) -> pd.DataFrame:
    return _revenue_summary(df, "subscription")


def sales_by_payment(df: pd.DataFrame) -> pd.DataFrame:
    return _revenue_summary(df, "payment_method")


def sales_by_shipping(df: pd.DataFrame) -> pd.DataFrame:
    return _revenue_summary(df, "shipping_type")


def sales_by_frequency(df: pd.DataFrame) -> pd.DataFrame:
    return _revenue_summary(df, "purchase_frequency")


def sales_by_discount(df: pd.DataFrame) -> pd.DataFrame:
    return _revenue_summary(df, "discount_applied")


# ──────────────────────────────────────────────────────────────────────────────
# 3.  CUSTOMER-LEVEL INSIGHTS
# ──────────────────────────────────────────────────────────────────────────────

def top_customers(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Highest-spending customers by total spend."""
    result = (
        df.groupby("customer_id")
        .agg(
            total_spend     =("purchase_amount", "sum"),
            num_purchases   =("purchase_amount", "count"),
            avg_rating      =("rating",          "mean"),
        )
        .reset_index()
        .sort_values("total_spend", ascending=False)
        .head(top_n)
    )
    result["avg_rating"] = result["avg_rating"].round(2)
    return result


def age_distribution(df: pd.DataFrame) -> pd.Series:
    """Raw age values for histogram."""
    return df["age"]


def rating_distribution(df: pd.DataFrame) -> pd.Series:
    """Raw rating values for histogram."""
    return df["rating"]


def purchase_amount_distribution(df: pd.DataFrame) -> pd.Series:
    return df["purchase_amount"]


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Pearson correlation of numeric columns."""
    numeric_cols = ["age", "purchase_amount", "rating",
                    "previous_purchases"]
    return df[numeric_cols].corr()
