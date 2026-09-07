"""
charts.py
---------
All Matplotlib / Seaborn / Plotly chart helpers used by the Streamlit app.
Every function returns a Plotly Figure object (for st.plotly_chart).
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

# ── Shared colour palette ──────────────────────────────────────────────────────
PALETTE   = px.colors.qualitative.Set2
BLUE_SEQ  = px.colors.sequential.Blues
TEAL_SEQ  = px.colors.sequential.Teal


def _style(fig: go.Figure, title: str = "") -> go.Figure:
    """Apply a consistent clean white layout to every chart."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color="#1f2937"),
                   x=0.0, xanchor="left"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=13, color="#374151"),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)"),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    fig.update_xaxes(showgrid=False, linecolor="#e5e7eb", tickfont=dict(size=12))
    fig.update_yaxes(showgrid=True,  gridcolor="#f3f4f6", linecolor="#e5e7eb",
                     tickfont=dict(size=12))
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# BAR CHARTS
# ──────────────────────────────────────────────────────────────────────────────

def bar_revenue_by_category(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_summary,
        x="category", y="total_revenue",
        text="total_revenue",
        color="category",
        color_discrete_sequence=PALETTE,
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    return _style(fig, "Total Revenue by Category")


def bar_revenue_by_item(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_summary.sort_values("total_revenue"),
        x="total_revenue", y="item",
        orientation="h",
        color="total_revenue",
        color_continuous_scale=TEAL_SEQ,
        text="total_revenue",
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, yaxis_title="")
    return _style(fig, "Top Items by Revenue")


def bar_revenue_by_season(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_summary,
        x="season", y="total_revenue",
        text="total_revenue",
        color="season",
        color_discrete_sequence=["#86efac", "#fde68a", "#fca5a5", "#93c5fd"],
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    return _style(fig, "Revenue by Season")


def bar_revenue_by_location(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_summary.sort_values("total_revenue"),
        x="total_revenue", y="location",
        orientation="h",
        color="total_revenue",
        color_continuous_scale=BLUE_SEQ,
        text="total_revenue",
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, yaxis_title="")
    return _style(fig, "Top Locations by Revenue")


def bar_revenue_by_age_group(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_summary,
        x="age_group", y="total_revenue",
        text="total_revenue",
        color="age_group",
        color_discrete_sequence=PALETTE,
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    return _style(fig, "Revenue by Age Group")


def bar_avg_spend_by_frequency(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_summary.sort_values("avg_purchase", ascending=False),
        x="purchase_frequency", y="avg_purchase",
        text="avg_purchase",
        color="purchase_frequency",
        color_discrete_sequence=PALETTE,
    )
    fig.update_traces(texttemplate="$%{text:.1f}", textposition="outside")
    fig.update_layout(xaxis_title="Purchase Frequency", yaxis_title="Avg Spend (USD)")
    return _style(fig, "Avg Spend by Purchase Frequency")


def bar_revenue_by_payment(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_summary.sort_values("total_revenue"),
        x="total_revenue", y="payment_method",
        orientation="h",
        text="total_revenue",
        color="payment_method",
        color_discrete_sequence=PALETTE,
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(showlegend=False, yaxis_title="")
    return _style(fig, "Revenue by Payment Method")


def bar_count_by_shipping(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_summary.sort_values("purchase_count"),
        x="purchase_count", y="shipping_type",
        orientation="h",
        text="purchase_count",
        color="shipping_type",
        color_discrete_sequence=PALETTE,
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, yaxis_title="")
    return _style(fig, "Orders by Shipping Type")


# ──────────────────────────────────────────────────────────────────────────────
# PIE / DONUT CHARTS
# ──────────────────────────────────────────────────────────────────────────────

def pie_revenue_by_category(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        df_summary,
        names="category", values="total_revenue",
        hole=0.4,
        color_discrete_sequence=PALETTE,
    )
    fig.update_traces(textinfo="percent+label", pull=[0.03] * len(df_summary))
    return _style(fig, "Revenue Share by Category")


def pie_gender_split(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        df_summary,
        names="gender", values="total_revenue",
        hole=0.4,
        color_discrete_sequence=["#60a5fa", "#f472b6"],
    )
    fig.update_traces(textinfo="percent+label")
    return _style(fig, "Revenue Split by Gender")


def pie_subscription(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        df_summary,
        names="subscription", values="total_revenue",
        hole=0.4,
        color_discrete_sequence=["#34d399", "#f87171"],
    )
    fig.update_traces(textinfo="percent+label")
    return _style(fig, "Subscriber vs Non-Subscriber Revenue")


def pie_discount(df_summary: pd.DataFrame) -> go.Figure:
    fig = px.pie(
        df_summary,
        names="discount_applied", values="total_revenue",
        hole=0.4,
        color_discrete_sequence=["#fb923c", "#a78bfa"],
    )
    fig.update_traces(textinfo="percent+label")
    return _style(fig, "Discount Applied Revenue Split")


# ──────────────────────────────────────────────────────────────────────────────
# HISTOGRAMS
# ──────────────────────────────────────────────────────────────────────────────

def histogram_age(series: pd.Series) -> go.Figure:
    fig = px.histogram(
        series, x=series,
        nbins=20,
        color_discrete_sequence=["#60a5fa"],
        labels={"x": "Age"},
    )
    fig.update_layout(bargap=0.05, xaxis_title="Age", yaxis_title="Count")
    return _style(fig, "Age Distribution of Customers")


def histogram_purchase_amount(series: pd.Series) -> go.Figure:
    fig = px.histogram(
        series, x=series,
        nbins=25,
        color_discrete_sequence=["#34d399"],
        labels={"x": "Purchase Amount (USD)"},
    )
    fig.update_layout(bargap=0.05,
                      xaxis_title="Purchase Amount (USD)", yaxis_title="Count")
    return _style(fig, "Purchase Amount Distribution")


def histogram_rating(series: pd.Series) -> go.Figure:
    fig = px.histogram(
        series, x=series,
        nbins=20,
        color_discrete_sequence=["#f472b6"],
        labels={"x": "Review Rating"},
    )
    fig.update_layout(bargap=0.05, xaxis_title="Review Rating", yaxis_title="Count")
    return _style(fig, "Review Rating Distribution")


# ──────────────────────────────────────────────────────────────────────────────
# GROUPED BAR — Gender × Category
# ──────────────────────────────────────────────────────────────────────────────

def grouped_bar_gender_category(df: pd.DataFrame) -> go.Figure:
    summary = (
        df.groupby(["category", "gender"], observed=True)["purchase_amount"]
        .sum()
        .reset_index()
    )
    fig = px.bar(
        summary,
        x="category", y="purchase_amount",
        color="gender",
        barmode="group",
        text="purchase_amount",
        color_discrete_sequence=["#60a5fa", "#f472b6"],
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(xaxis_title="Category", yaxis_title="Total Revenue (USD)")
    return _style(fig, "Revenue by Category & Gender")


# ──────────────────────────────────────────────────────────────────────────────
# CORRELATION HEATMAP
# ──────────────────────────────────────────────────────────────────────────────

def heatmap_correlation(corr_df: pd.DataFrame) -> go.Figure:
    labels = list(corr_df.columns)
    z      = corr_df.values.round(2).tolist()

    fig = ff.create_annotated_heatmap(
        z=z,
        x=labels,
        y=labels,
        annotation_text=[[f"{v:.2f}" for v in row] for row in corr_df.values],
        colorscale="RdBu",
        zmid=0,
        showscale=True,
    )
    fig.update_layout(
        title=dict(text="Correlation Heatmap (Numeric Features)",
                   font=dict(size=16, color="#1f2937")),
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# SCATTER — Age vs Purchase Amount
# ──────────────────────────────────────────────────────────────────────────────

def scatter_age_vs_spend(df: pd.DataFrame) -> go.Figure:
    sample = df.sample(min(800, len(df)), random_state=42)
    fig = px.scatter(
        sample,
        x="age", y="purchase_amount",
        color="category",
        opacity=0.65,
        color_discrete_sequence=PALETTE,
        labels={"age": "Age", "purchase_amount": "Purchase Amount (USD)"},
    )
    fig.update_layout(xaxis_title="Age", yaxis_title="Purchase Amount (USD)")
    return _style(fig, "Age vs Purchase Amount (sample)")


# ──────────────────────────────────────────────────────────────────────────────
# TOP CUSTOMERS TABLE CHART
# ──────────────────────────────────────────────────────────────────────────────

def bar_top_customers(df_top: pd.DataFrame) -> go.Figure:
    fig = px.bar(
        df_top,
        x="customer_id", y="total_spend",
        text="total_spend",
        color="total_spend",
        color_continuous_scale=TEAL_SEQ,
        labels={"customer_id": "Customer ID", "total_spend": "Total Spend (USD)"},
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(coloraxis_showscale=False,
                      xaxis=dict(type="category"))
    return _style(fig, "Top 10 Highest-Spending Customers")
