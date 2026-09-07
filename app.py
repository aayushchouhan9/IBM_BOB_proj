"""
app.py
------
Streamlit dashboard for Customer Shopping Behaviour Analysis.

Run:
    streamlit run app.py

Pages (sidebar navigation):
  1. 🏠 Overview & Data Quality
  2. 📊 Sales KPIs
  3. 🛍️ Product Analysis
  4. 🌍 Demographics
  5. 📅 Seasonal & Behavioural
  6. 💡 Insights & Recommendations
"""

import sys
import os

# Make the src package importable when running from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd

from data_loader import load_data, dataset_summary
import analysis as an
import charts as ch

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Shopping Behaviour Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Minimal global CSS tweaks ──────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stMetric"] {
        background-color: #f7f8fa;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 14px 18px;
    }
    [data-testid="stMetricLabel"]  { font-size: 13px !important; color: #57606a; }
    [data-testid="stMetricValue"]  { font-size: 26px !important; color: #1f2328; font-weight:700; }
    h1 { color: #1f2328; }
    h2 { color: #1f2328; border-bottom: 2px solid #e5e7eb; padding-bottom: 6px; }
    h3 { color: #374151; }
    .stDataFrame { border-radius: 8px; }
    div[data-testid="stSidebarNav"] { font-size: 15px; }
    .insight-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #1e3a5f;
    }
    .rec-box {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #14532d;
    }
    .warn-box {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        border-radius: 6px;
        padding: 10px 16px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #78350f;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOAD  (cached so it doesn't reload on every interaction)
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner="Loading dataset…")
def get_data() -> pd.DataFrame:
    return load_data()


df_full = get_data()


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — navigation + global filters
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image(
        "https://img.icons8.com/color/96/shopping-cart.png",
        width=64,
    )
    st.title("🛒 Shopping Analytics")
    st.markdown("---")

    page = st.radio(
        "Navigate to",
        [
            "🏠 Overview & Data Quality",
            "📊 Sales KPIs",
            "🛍️ Product Analysis",
            "🌍 Demographics",
            "📅 Seasonal & Behavioural",
            "💡 Insights & Recommendations",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### Global Filters")

    # Season filter
    seasons_all = sorted(df_full["season"].dropna().unique())
    sel_seasons = st.multiselect("Season", seasons_all, default=seasons_all)

    # Gender filter
    genders_all = sorted(df_full["gender"].dropna().unique())
    sel_gender = st.multiselect("Gender", genders_all, default=genders_all)

    # Category filter
    cats_all = sorted(df_full["category"].dropna().unique())
    sel_cats = st.multiselect("Category", cats_all, default=cats_all)

    st.markdown("---")
    st.caption("Dataset: customer_shopping_behavior.csv")
    st.caption(f"Records loaded: **{len(df_full):,}**")


# Apply filters
df = df_full.copy()
if sel_seasons: df = df[df["season"].isin(sel_seasons)]
if sel_gender:  df = df[df["gender"].isin(sel_gender)]
if sel_cats:    df = df[df["category"].isin(sel_cats)]

if df.empty:
    st.warning("⚠️ No data matches your filters. Please adjust the sidebar selections.")
    st.stop()


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE 1 ── OVERVIEW & DATA QUALITY
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview & Data Quality":
    st.title("🏠 Dataset Overview & Data Quality")
    st.markdown(
        "A quick inspection of the raw dataset before any analysis is performed."
    )

    summary = dataset_summary(df_full)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records",    f"{summary['total_records']:,}")
    col2.metric("Total Columns",    summary["total_columns"])
    col3.metric("Missing Values",   summary["missing_values"])
    col4.metric("Duplicate Rows",   summary["duplicate_rows"])

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📋 Raw Sample", "🔢 Column Types", "📉 Missing Values"])

    with tab1:
        st.markdown("**First 20 rows of the dataset**")
        st.dataframe(df_full.head(20), use_container_width=True, height=420)

    with tab2:
        dtype_df = pd.DataFrame(
            {"Column": list(summary["dtypes"].keys()),
             "Data Type": list(summary["dtypes"].values())}
        )
        st.dataframe(dtype_df, use_container_width=True)

    with tab3:
        miss = df_full.isnull().sum().reset_index()
        miss.columns = ["Column", "Missing Count"]
        miss["Missing %"] = (miss["Missing Count"] / len(df_full) * 100).round(2)
        st.dataframe(miss, use_container_width=True)
        if miss["Missing Count"].sum() == 0:
            st.success("✅ No missing values found in the dataset.")

    st.markdown("---")
    st.subheader("📊 Descriptive Statistics")
    st.dataframe(
        df_full[["age", "purchase_amount", "rating", "previous_purchases"]].describe().round(2),
        use_container_width=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE 2 ── SALES KPIs
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Sales KPIs":
    st.title("📊 Sales Key Performance Indicators")
    st.markdown("Headline metrics computed from the filtered dataset.")

    kpis = an.compute_kpis(df)

    # Row 1
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Total Revenue",        f"${kpis['total_revenue']:,.2f}")
    c2.metric("🛒 Total Purchases",       f"{kpis['total_purchases']:,}")
    c3.metric("📦 Avg Purchase Amount",   f"${kpis['avg_purchase_amount']:,.2f}")
    c4.metric("⭐ Avg Review Rating",      f"{kpis['avg_rating']:.2f} / 5")

    # Row 2
    c5, c6, c7, c8 = st.columns(4)
    c5.metric("👤 Unique Customers",      f"{kpis['unique_customers']:,}")
    c6.metric("📧 Subscription Rate",     f"{kpis['subscription_rate']}%")
    c7.metric("🏷️ Discount Applied Rate", f"{kpis['discount_rate']}%")
    c8.metric("🔄 Avg Prior Purchases",   f"{kpis['avg_previous_purchases']}")

    st.markdown("---")
    st.subheader("Revenue by Category")
    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(
            ch.bar_revenue_by_category(an.sales_by_category(df)),
            use_container_width=True,
        )
    with col_right:
        st.plotly_chart(
            ch.pie_revenue_by_category(an.sales_by_category(df)),
            use_container_width=True,
        )

    st.markdown("---")
    st.subheader("Revenue by Payment Method & Shipping")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(ch.bar_revenue_by_payment(an.sales_by_payment(df)),
                        use_container_width=True)
    with c2:
        st.plotly_chart(ch.bar_count_by_shipping(an.sales_by_shipping(df)),
                        use_container_width=True)

    st.markdown("---")
    st.subheader("Detailed Summary Table")
    cat_summary = an.sales_by_category(df)
    cat_summary.columns = ["Category", "Total Revenue", "Purchase Count",
                            "Avg Purchase", "Avg Rating"]
    st.dataframe(cat_summary.style.format({
        "Total Revenue": "${:,.2f}",
        "Avg Purchase":  "${:,.2f}",
        "Avg Rating":    "{:.2f}",
    }), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE 3 ── PRODUCT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🛍️ Product Analysis":
    st.title("🛍️ Product & Item Analysis")

    top_n = st.slider("Number of top items to display", 5, 25, 15)

    st.subheader(f"Top {top_n} Items by Revenue")
    st.plotly_chart(
        ch.bar_revenue_by_item(an.sales_by_item(df, top_n)),
        use_container_width=True,
    )

    st.markdown("---")
    st.subheader("Revenue by Category & Gender")
    st.plotly_chart(ch.grouped_bar_gender_category(df), use_container_width=True)

    st.markdown("---")
    st.subheader("Purchase Amount Distribution")
    st.plotly_chart(ch.histogram_purchase_amount(an.purchase_amount_distribution(df)),
                    use_container_width=True)

    st.markdown("---")
    st.subheader("Review Rating Distribution")
    st.plotly_chart(ch.histogram_rating(an.rating_distribution(df)),
                    use_container_width=True)

    st.markdown("---")
    st.subheader("Correlation Heatmap")
    st.markdown(
        "Pearson correlation between numeric features: age, purchase amount, rating, "
        "and number of previous purchases."
    )
    st.plotly_chart(ch.heatmap_correlation(an.correlation_matrix(df)),
                    use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Full Item Summary Table")
    item_tbl = an.sales_by_item(df, top_n)
    item_tbl.columns = ["Item", "Total Revenue", "Purchase Count",
                         "Avg Purchase", "Avg Rating"]
    st.dataframe(item_tbl.style.format({
        "Total Revenue": "${:,.2f}",
        "Avg Purchase":  "${:,.2f}",
        "Avg Rating":    "{:.2f}",
    }), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE 4 ── DEMOGRAPHICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🌍 Demographics":
    st.title("🌍 Customer Demographics")

    # Gender
    st.subheader("Gender")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(ch.pie_gender_split(an.sales_by_gender(df)),
                        use_container_width=True)
    with c2:
        g_tbl = an.sales_by_gender(df)
        g_tbl.columns = ["Gender", "Total Revenue", "Purchase Count",
                         "Avg Purchase", "Avg Rating"]
        st.dataframe(g_tbl.style.format({
            "Total Revenue": "${:,.2f}",
            "Avg Purchase":  "${:,.2f}",
            "Avg Rating":    "{:.2f}",
        }), use_container_width=True)

    st.markdown("---")

    # Age
    st.subheader("Age")
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(ch.histogram_age(an.age_distribution(df)),
                        use_container_width=True)
    with c4:
        st.plotly_chart(ch.bar_revenue_by_age_group(an.sales_by_age_group(df)),
                        use_container_width=True)

    st.markdown("---")

    # Location
    st.subheader("Top Locations by Revenue")
    loc_n = st.slider("Top N locations", 5, 20, 15, key="loc_n")
    st.plotly_chart(
        ch.bar_revenue_by_location(an.sales_by_location(df, loc_n)),
        use_container_width=True,
    )

    st.markdown("---")

    # Scatter
    st.subheader("Age vs Purchase Amount")
    st.plotly_chart(ch.scatter_age_vs_spend(df), use_container_width=True)

    st.markdown("---")

    # Subscription
    st.subheader("Subscriber vs Non-Subscriber")
    c5, c6 = st.columns(2)
    with c5:
        st.plotly_chart(ch.pie_subscription(an.sales_by_subscription(df)),
                        use_container_width=True)
    with c6:
        sub_tbl = an.sales_by_subscription(df)
        sub_tbl.columns = ["Subscription Status", "Total Revenue", "Purchase Count",
                           "Avg Purchase", "Avg Rating"]
        st.dataframe(sub_tbl.style.format({
            "Total Revenue": "${:,.2f}",
            "Avg Purchase":  "${:,.2f}",
            "Avg Rating":    "{:.2f}",
        }), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE 5 ── SEASONAL & BEHAVIOURAL
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📅 Seasonal & Behavioural":
    st.title("📅 Seasonal & Behavioural Patterns")

    # Season
    st.subheader("Revenue by Season")
    st.plotly_chart(ch.bar_revenue_by_season(an.sales_by_season(df)),
                    use_container_width=True)

    st.markdown("---")

    # Purchase frequency
    st.subheader("Purchase Frequency & Avg Spend")
    st.plotly_chart(ch.bar_avg_spend_by_frequency(an.sales_by_frequency(df)),
                    use_container_width=True)

    st.markdown("---")

    # Discount
    st.subheader("Discount vs No Discount")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(ch.pie_discount(an.sales_by_discount(df)),
                        use_container_width=True)
    with c2:
        disc_tbl = an.sales_by_discount(df)
        disc_tbl.columns = ["Discount Applied", "Total Revenue", "Purchase Count",
                            "Avg Purchase", "Avg Rating"]
        st.dataframe(disc_tbl.style.format({
            "Total Revenue": "${:,.2f}",
            "Avg Purchase":  "${:,.2f}",
            "Avg Rating":    "{:.2f}",
        }), use_container_width=True)

    st.markdown("---")

    # Top customers
    st.subheader("Top 10 Highest-Spending Customers")
    top_c = an.top_customers(df, 10)
    st.plotly_chart(ch.bar_top_customers(top_c), use_container_width=True)
    st.dataframe(top_c.style.format({
        "total_spend": "${:,.2f}",
        "avg_rating":  "{:.2f}",
    }), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ── PAGE 6 ── INSIGHTS & RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💡 Insights & Recommendations":
    st.title("💡 Business Insights & Recommendations")
    st.markdown(
        "All insights are derived directly from the dataset using the current filters."
    )

    kpis = an.compute_kpis(df)
    cat_df   = an.sales_by_category(df)
    item_df  = an.sales_by_item(df, 5)
    season_df = an.sales_by_season(df)
    gender_df = an.sales_by_gender(df)
    sub_df   = an.sales_by_subscription(df)
    disc_df  = an.sales_by_discount(df)
    loc_df   = an.sales_by_location(df, 5)
    age_df   = an.sales_by_age_group(df)

    # ── Derived facts ──────────────────────────────────────────────────────────
    top_cat    = cat_df.iloc[0]["category"]
    top_cat_rev = cat_df.iloc[0]["total_revenue"]
    top_item   = item_df.iloc[0]["item"]
    top_item_rev = item_df.iloc[0]["total_revenue"]
    top_season = season_df.sort_values("total_revenue", ascending=False).iloc[0]["season"]
    top_gender = gender_df.iloc[0]["gender"]
    top_loc    = loc_df.iloc[0]["location"]
    top_age    = age_df.iloc[0]["age_group"]

    sub_yes = sub_df[sub_df["subscription"].str.lower() == "yes"]
    sub_no  = sub_df[sub_df["subscription"].str.lower() == "no"]
    sub_yes_avg = sub_yes["avg_purchase"].values[0] if len(sub_yes) else 0
    sub_no_avg  = sub_no["avg_purchase"].values[0]  if len(sub_no)  else 0

    disc_yes = disc_df[disc_df["discount_applied"].str.lower() == "yes"]
    disc_no  = disc_df[disc_df["discount_applied"].str.lower() == "no"]
    disc_yes_avg = disc_yes["avg_purchase"].values[0] if len(disc_yes) else 0
    disc_no_avg  = disc_no["avg_purchase"].values[0]  if len(disc_no)  else 0

    # ── Insights ───────────────────────────────────────────────────────────────
    st.subheader("📌 Key Findings")

    insights = [
        f"🏆 <b>Top category:</b> <em>{top_cat}</em> generates the highest revenue "
        f"(${top_cat_rev:,.2f}), making it the primary revenue driver.",

        f"🛒 <b>Best-selling item:</b> <em>{top_item}</em> leads all products with "
        f"${top_item_rev:,.2f} in total revenue.",

        f"📅 <b>Peak season:</b> <em>{top_season}</em> records the highest sales volume. "
        "Seasonal promotions during this period can maximise revenue.",

        f"👤 <b>Gender dominance:</b> <em>{top_gender}</em> shoppers account for the largest "
        "share of purchases and revenue.",

        f"📍 <b>Top location:</b> <em>{top_loc}</em> is the highest-revenue market — a key "
        "region for targeted marketing campaigns.",

        f"🎂 <b>Highest-spending age group:</b> <em>{top_age}</em> customers spend the most. "
        "Tailor product recommendations and offers to this segment.",

        f"📧 <b>Subscription impact:</b> Subscribers average ${sub_yes_avg:,.2f} per purchase "
        f"vs ${sub_no_avg:,.2f} for non-subscribers — a "
        f"{'higher' if sub_yes_avg >= sub_no_avg else 'lower'} spend per transaction.",

        f"🏷️ <b>Discount effect:</b> Customers who applied a discount averaged "
        f"${disc_yes_avg:,.2f} vs ${disc_no_avg:,.2f} for those who did not.",

        f"⭐ <b>Average review rating:</b> {kpis['avg_rating']:.2f}/5 — indicates overall "
        "customer satisfaction. Aim to push this above 4.0 through quality improvements.",

        f"🔁 <b>Loyal customers:</b> Avg prior purchases = {kpis['avg_previous_purchases']} "
        "— customers are repeat buyers and strong targets for loyalty programmes.",
    ]

    for ins in insights:
        st.markdown(f'<div class="insight-box">{ins}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Recommendations ────────────────────────────────────────────────────────
    st.subheader("✅ Business Recommendations")

    recs = [
        f"<b>1. Double down on {top_cat}.</b>  Since it generates the most revenue, "
        "invest in broader range, better stock availability, and premium tier offerings.",

        f"<b>2. Seasonal campaigns during {top_season}.</b>  Plan inventory builds, "
        "flash sales, and email campaigns 4–6 weeks before the peak season begins.",

        f"<b>3. Expand presence in {top_loc}.</b>  Allocate higher ad spend and "
        "explore partnerships or pop-up stores in this region.",

        f"<b>4. Target the {top_age} age group.</b>  Personalise home-page banners, "
        "push notifications, and loyalty rewards for this cohort.",

        "<b>5. Grow the subscriber base.</b>  Run a 'First 3 months free' trial to "
        "convert casual shoppers — subscribers show stronger long-term value.",

        "<b>6. Smart discount strategy.</b>  Reserve discounts for cart-abandonment "
        "recovery and new-customer acquisition rather than blanket offers, "
        "to protect margin.",

        "<b>7. Upsell complementary categories.</b>  Bundle Accessories with Clothing "
        "or Footwear purchases via 'Frequently bought together' prompts.",

        "<b>8. Improve review rating.</b>  Send post-purchase follow-up emails "
        "requesting feedback and resolve negative reviews proactively. "
        "Target ≥ 4.2 stars.",

        "<b>9. Reward high-frequency buyers.</b>  Identify 'Weekly' purchase-frequency "
        "customers and offer a VIP tier with free expedited shipping and early access.",

        "<b>10. Optimise shipping mix.</b>  Analyse which shipping types drive the "
        "highest satisfaction scores and renegotiate carrier rates for the most "
        "popular options.",
    ]

    for rec in recs:
        st.markdown(f'<div class="rec-box">{rec}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("⚠️ Watch-Outs")
    warns = [
        "Dataset contains only static snapshot data — no time series. "
        "True seasonality trends require multi-year data.",
        "Customer IDs are 1–3900 with no repeat entries per row, "
        "so 'previous_purchases' is a self-reported metric — validate with transactional logs.",
        "Rating data is fairly uniformly distributed; contextual drivers of low ratings "
        "are not captured in this dataset.",
    ]
    for w in warns:
        st.markdown(f'<div class="warn-box">⚠️ {w}</div>', unsafe_allow_html=True)
