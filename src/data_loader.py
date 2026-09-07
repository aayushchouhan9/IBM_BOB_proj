"""
data_loader.py
--------------
Loads and cleans the customer shopping behaviour CSV dataset.
Returns a clean, typed pandas DataFrame ready for analysis.
"""

import pandas as pd
import os

# ── Column rename map (original → clean) ──────────────────────────────────────
COLUMN_MAP = {
    "Customer ID":           "customer_id",
    "Age":                   "age",
    "Gender":                "gender",
    "Item Purchased":        "item",
    "Category":              "category",
    "Purchase Amount (USD)": "purchase_amount",
    "Location":              "location",
    "Size":                  "size",
    "Color":                 "color",
    "Season":                "season",
    "Review Rating":         "rating",
    "Subscription Status":   "subscription",
    "Shipping Type":         "shipping_type",
    "Discount Applied":      "discount_applied",
    "Promo Code Used":       "promo_code_used",
    "Previous Purchases":    "previous_purchases",
    "Payment Method":        "payment_method",
    "Frequency of Purchases":"purchase_frequency",
}

# Age-group bin edges and labels
AGE_BINS   = [0, 17, 25, 35, 45, 55, 65, 120]
AGE_LABELS = ["<18", "18-25", "26-35", "36-45", "46-55", "56-65", "65+"]


def load_data(filepath: str | None = None) -> pd.DataFrame:
    """
    Load the CSV, rename columns, cast types, add derived columns,
    and return a clean DataFrame.

    Parameters
    ----------
    filepath : str, optional
        Path to the CSV file.  Defaults to data/customer_shopping_behavior.csv
        relative to the project root.

    Returns
    -------
    pd.DataFrame
    """
    if filepath is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(base, "data", "customer_shopping_behavior.csv")

    # ── 1. Read ────────────────────────────────────────────────────────────────
    df = pd.read_csv(filepath, encoding="utf-8-sig")   # utf-8-sig strips BOM

    # ── 2. Rename ──────────────────────────────────────────────────────────────
    df.rename(columns=COLUMN_MAP, inplace=True)

    # ── 3. Drop exact duplicates ───────────────────────────────────────────────
    df.drop_duplicates(inplace=True)

    # ── 4. Drop rows with critical missing values ──────────────────────────────
    critical = ["purchase_amount", "age", "gender", "category", "item", "season"]
    df.dropna(subset=critical, inplace=True)

    # ── 5. Cast numeric types ──────────────────────────────────────────────────
    df["purchase_amount"]    = pd.to_numeric(df["purchase_amount"],    errors="coerce")
    df["age"]                = pd.to_numeric(df["age"],                errors="coerce")
    df["rating"]             = pd.to_numeric(df["rating"],             errors="coerce")
    df["previous_purchases"] = pd.to_numeric(df["previous_purchases"], errors="coerce")

    # Drop rows where numeric coercion left NaN in critical cols
    df.dropna(subset=["purchase_amount", "age"], inplace=True)

    # ── 6. Validate business ranges ────────────────────────────────────────────
    df = df[(df["purchase_amount"] > 0) & (df["age"] >= 0)]
    df = df[df["rating"].between(1, 5) | df["rating"].isna()]

    # ── 7. Standardise categorical text ───────────────────────────────────────
    for col in ["gender", "category", "item", "season", "subscription",
                "discount_applied", "promo_code_used", "shipping_type",
                "payment_method", "purchase_frequency", "location"]:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    # ── 8. Boolean flags ───────────────────────────────────────────────────────
    df["is_subscriber"]    = df["subscription"].str.lower()   == "yes"
    df["has_discount"]     = df["discount_applied"].str.lower() == "yes"
    df["used_promo"]       = df["promo_code_used"].str.lower()  == "yes"

    # ── 9. Derived columns ─────────────────────────────────────────────────────
    df["age_group"] = pd.cut(df["age"], bins=AGE_BINS, labels=AGE_LABELS,
                             right=True)

    df.reset_index(drop=True, inplace=True)
    return df


def dataset_summary(df: pd.DataFrame) -> dict:
    """Return a plain-dict summary used on the Overview page."""
    return {
        "total_records":    len(df),
        "total_columns":    df.shape[1],
        "missing_values":   int(df.isnull().sum().sum()),
        "duplicate_rows":   0,          # already dropped
        "numeric_columns":  list(df.select_dtypes("number").columns),
        "categorical_cols": list(df.select_dtypes("object").columns),
        "dtypes":           df.dtypes.astype(str).to_dict(),
    }
