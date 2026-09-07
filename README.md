<<<<<<< HEAD
# 🛒 Customer Shopping Behaviour Analytics Dashboard

A fully interactive **Streamlit** dashboard that analyses 3,900 retail customer
transactions and surfaces actionable business insights — all from a single CSV file.

---

## 📁 Project Structure

```
shopping_analysis/
├── app.py                  ← Streamlit entry-point (run this)
├── requirements.txt        ← Python dependencies
├── data/
│   └── customer_shopping_behavior.csv
└── src/
    ├── data_loader.py      ← Load + clean the CSV
    ├── analysis.py         ← KPIs & grouped summaries
    └── charts.py           ← Plotly chart helpers
```

---

## ⚙️ Setup & Run

### 1. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the dashboard

```bash
cd shopping_analysis
streamlit run app.py
```

Your browser will open automatically at **http://localhost:8501**
DEPLOYED LINK **https://aayushchouhan9-ibm-bob-proj-app-vmorhv.streamlit.app**.

---

## 🗂️ Dashboard Pages

| Page | What you'll find |
|------|-----------------|
| 🏠 Overview & Data Quality | Row count, column types, missing values, descriptive stats |
| 📊 Sales KPIs | Total revenue, purchase count, avg spend, avg rating, subscription rate |
| 🛍️ Product Analysis | Top items by revenue, purchase amount histogram, correlation heatmap |
| 🌍 Demographics | Gender split, age distribution, top locations, subscriber breakdown |
| 📅 Seasonal & Behavioural | Revenue by season, purchase frequency, discount impact, top customers |
| 💡 Insights & Recommendations | Data-driven findings + 10 actionable business recommendations |

---

## 🔍 Dataset Columns

| Column | Description |
|--------|-------------|
| Customer ID | Unique customer identifier (1–3900) |
| Age | Customer age |
| Gender | Male / Female |
| Item Purchased | Product name |
| Category | Clothing / Footwear / Accessories / Outerwear |
| Purchase Amount (USD) | Transaction value |
| Location | US state |
| Size | S / M / L / XL |
| Color | Product colour |
| Season | Spring / Summer / Fall / Winter |
| Review Rating | 1.0 – 5.0 stars |
| Subscription Status | Yes / No |
| Shipping Type | Standard / Express / Free Shipping / etc. |
| Discount Applied | Yes / No |
| Promo Code Used | Yes / No |
| Previous Purchases | Count of prior transactions |
| Payment Method | Cash / Credit Card / PayPal / etc. |
| Frequency of Purchases | Weekly / Monthly / Fortnightly / etc. |

---

## 🧹 Data Cleaning Steps

1. Remove BOM character from CSV header (utf-8-sig encoding)
2. Rename all columns to clean snake_case names
3. Drop exact duplicate rows
4. Drop rows with missing values in critical columns
5. Coerce numeric columns (`age`, `purchase_amount`, `rating`, `previous_purchases`)
6. Filter out invalid business values (negative amounts, ratings outside 1–5)
7. Standardise categorical text (Title Case, strip whitespace)
8. Add boolean flags: `is_subscriber`, `has_discount`, `used_promo`
9. Add `age_group` derived column using standard age bins

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web dashboard UI |
| `pandas` | Data loading, cleaning, analysis |
| `plotly` | Interactive charts (bar, pie, histogram, heatmap, scatter) |

---

## 📝 Notes

- All insights on the **💡 Insights & Recommendations** page are computed
  dynamically from the actual data — no hard-coded numbers.
- The **sidebar filters** (Season, Gender, Category) apply globally across every
  page so you can drill into any segment.
- The correlation heatmap uses Pearson correlation on the four numeric columns.
=======
# IBM_BOB_proj
>>>>>>> 345e82348fd775b60f03bcc407e59e55a06d22bd

