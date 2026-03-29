"""
Retail Sales Analytics Dashboard
Snowflake Streamlit in Snowflake demo
"""

import streamlit as st
import pandas as pd
import altair as alt
from snowflake.snowpark.context import get_active_session

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="売上分析ダッシュボード",
    page_icon="📊",
    layout="wide",
)

# ── Session ───────────────────────────────────────────────────────────────────
session = get_active_session()

DB = "DEMO_STREAMLIT_DB"
SCHEMA = "ANALYTICS"


@st.cache_data(ttl=300)
def fetch(query: str) -> pd.DataFrame:
    return session.sql(query).to_pandas()


# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.title("フィルター")

    years_df = fetch(f"SELECT DISTINCT YEAR(SALE_DATE) AS YR FROM {DB}.{SCHEMA}.SALES ORDER BY 1")
    all_years = years_df["YR"].tolist()
    selected_years = st.multiselect("年度", all_years, default=all_years)

    categories_df = fetch(f"SELECT DISTINCT CATEGORY FROM {DB}.{SCHEMA}.SALES ORDER BY 1")
    all_categories = categories_df["CATEGORY"].tolist()
    selected_categories = st.multiselect("カテゴリ", all_categories, default=all_categories)

    regions_df = fetch(f"SELECT DISTINCT REGION FROM {DB}.{SCHEMA}.SALES ORDER BY 1")
    all_regions = regions_df["REGION"].tolist()
    selected_regions = st.multiselect("地域", all_regions, default=all_regions)

    st.divider()
    st.caption("※ データは2024〜2025年の小売業サンプルです")

# ── Filter condition ──────────────────────────────────────────────────────────
if not selected_years or not selected_categories or not selected_regions:
    st.warning("フィルターで少なくとも1つ選択してください。")
    st.stop()

yr_in  = ", ".join(str(y) for y in selected_years)
cat_in = ", ".join(f"'{c}'" for c in selected_categories)
reg_in = ", ".join(f"'{r}'" for r in selected_regions)

where = f"""
    YEAR(SALE_DATE) IN ({yr_in})
    AND CATEGORY IN ({cat_in})
    AND REGION IN ({reg_in})
"""

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("📊 売上分析ダッシュボード")
st.caption("Snowflake Streamlit in Snowflake デモ — 小売業サンプルデータ")
st.divider()

# ── KPI cards ─────────────────────────────────────────────────────────────────
kpi = fetch(f"""
    SELECT
        SUM(REVENUE)                                                     AS total_revenue,
        SUM(UNITS_SOLD)                                                  AS total_units,
        SUM(REVENUE - COST)                                              AS total_profit,
        CASE WHEN SUM(REVENUE) > 0
             THEN SUM(REVENUE - COST) / SUM(REVENUE) * 100 ELSE 0 END   AS margin_pct,
        COUNT(DISTINCT SALE_ID)                                          AS total_txn
    FROM {DB}.{SCHEMA}.SALES
    WHERE {where}
""")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("総売上",   f"¥{kpi['TOTAL_REVENUE'][0]:,.0f}")
c2.metric("販売数量", f"{kpi['TOTAL_UNITS'][0]:,.0f} 個")
c3.metric("粗利益",   f"¥{kpi['TOTAL_PROFIT'][0]:,.0f}")
c4.metric("粗利率",   f"{kpi['MARGIN_PCT'][0]:.1f} %")
c5.metric("取引件数", f"{kpi['TOTAL_TXN'][0]:,.0f} 件")

st.divider()

# ── Row 1: Monthly trend  |  Category breakdown ───────────────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("月次売上推移")
    monthly = fetch(f"""
        SELECT
            TO_VARCHAR(SALE_DATE, 'YYYY-MM') AS MONTH,
            SUM(REVENUE)       AS REVENUE,
            SUM(REVENUE-COST)  AS PROFIT
        FROM {DB}.{SCHEMA}.SALES
        WHERE {where}
        GROUP BY 1 ORDER BY 1
    """)
    monthly_melted = monthly.melt("MONTH", value_vars=["REVENUE", "PROFIT"],
                                  var_name="METRIC", value_name="AMOUNT")
    label_map = {"REVENUE": "売上", "PROFIT": "粗利益"}
    monthly_melted["METRIC"] = monthly_melted["METRIC"].map(label_map)

    chart = (
        alt.Chart(monthly_melted)
        .mark_line(point=True)
        .encode(
            x=alt.X("MONTH:O", title="月", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("AMOUNT:Q", title="金額（円）",
                    axis=alt.Axis(format=",.0f")),
            color=alt.Color("METRIC:N", title="指標",
                            scale=alt.Scale(
                                domain=["売上", "粗利益"],
                                range=["#1f77b4", "#2ca02c"])),
            tooltip=[
                alt.Tooltip("MONTH:O", title="月"),
                alt.Tooltip("METRIC:N", title="指標"),
                alt.Tooltip("AMOUNT:Q", title="金額", format=",.0f"),
            ],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, use_container_width=True)

with col_right:
    st.subheader("カテゴリ別売上")
    cat_df = fetch(f"""
        SELECT
            CATEGORY,
            SUM(REVENUE)                                                    AS REVENUE,
            ROUND(SUM(REVENUE-COST)/NULLIF(SUM(REVENUE),0)*100, 1)         AS MARGIN_PCT
        FROM {DB}.{SCHEMA}.SALES
        WHERE {where}
        GROUP BY 1 ORDER BY REVENUE DESC
    """)
    bar = (
        alt.Chart(cat_df)
        .mark_bar()
        .encode(
            x=alt.X("REVENUE:Q", title="売上（円）", axis=alt.Axis(format=",.0f")),
            y=alt.Y("CATEGORY:N", sort="-x", title="カテゴリ"),
            color=alt.Color("MARGIN_PCT:Q", title="粗利率(%)",
                            scale=alt.Scale(scheme="greens")),
            tooltip=[
                alt.Tooltip("CATEGORY:N", title="カテゴリ"),
                alt.Tooltip("REVENUE:Q",   title="売上",    format=",.0f"),
                alt.Tooltip("MARGIN_PCT:Q", title="粗利率", format=".1f"),
            ],
        )
        .properties(height=320)
    )
    st.altair_chart(bar, use_container_width=True)

st.divider()

# ── Row 2: Regional  |  Top products ─────────────────────────────────────────
col_l2, col_r2 = st.columns([2, 3])

with col_l2:
    st.subheader("地域別売上")
    region_df = fetch(f"""
        SELECT
            REGION,
            SUM(REVENUE)      AS REVENUE,
            SUM(UNITS_SOLD)   AS UNITS,
            ROUND(SUM(REVENUE-COST)/NULLIF(SUM(REVENUE),0)*100, 1) AS MARGIN_PCT
        FROM {DB}.{SCHEMA}.SALES
        WHERE {where}
        GROUP BY 1 ORDER BY REVENUE DESC
    """)
    region_df.columns = ["地域", "売上（円）", "販売数量", "粗利率(%)"]
    region_df["売上（円）"] = region_df["売上（円）"].map("{:,.0f}".format)
    region_df["販売数量"]   = region_df["販売数量"].map("{:,.0f}".format)
    st.dataframe(region_df, use_container_width=True, )

with col_r2:
    st.subheader("商品別売上トップ10")
    top_products = fetch(f"""
        SELECT
            PRODUCT_NAME,
            CATEGORY,
            SUM(REVENUE)      AS REVENUE,
            SUM(UNITS_SOLD)   AS UNITS,
            ROUND(SUM(REVENUE-COST)/NULLIF(SUM(REVENUE),0)*100,1) AS MARGIN_PCT
        FROM {DB}.{SCHEMA}.SALES
        WHERE {where}
        GROUP BY 1, 2 ORDER BY REVENUE DESC
        LIMIT 10
    """)
    top_products.columns = ["商品名", "カテゴリ", "売上（円）", "販売数量", "粗利率(%)"]
    top_products["売上（円）"] = top_products["売上（円）"].map("{:,.0f}".format)
    top_products["販売数量"]   = top_products["販売数量"].map("{:,.0f}".format)
    st.dataframe(top_products, use_container_width=True, )

st.divider()

# ── Row 3: Campaign performance ───────────────────────────────────────────────
st.subheader("キャンペーン チャネル別パフォーマンス")

camp_df = fetch(f"""
    SELECT
        CHANNEL,
        COUNT(*)                                                        AS CAMPAIGNS,
        SUM(ACTUAL_SPEND)                                               AS SPEND,
        ROUND(SUM(CLICKS)::FLOAT  / NULLIF(SUM(IMPRESSIONS),0)*100, 2) AS CTR,
        ROUND(SUM(CONVERSIONS)::FLOAT / NULLIF(SUM(CLICKS),0)*100, 2)  AS CVR,
        ROUND(SUM(ACTUAL_SPEND)   / NULLIF(SUM(CONVERSIONS),0), 0)     AS CPA
    FROM {DB}.{SCHEMA}.CAMPAIGNS
    WHERE CATEGORY IN ({cat_in})
    GROUP BY 1 ORDER BY CVR DESC
""")

c_chart, c_table = st.columns([3, 2])

with c_chart:
    ctr_cvr = camp_df[["CHANNEL", "CTR", "CVR"]].melt(
        "CHANNEL", var_name="METRIC", value_name="VALUE")
    grouped = (
        alt.Chart(ctr_cvr)
        .mark_bar()
        .encode(
            x=alt.X("METRIC:N", title="", axis=alt.Axis(labels=False, ticks=False)),
            y=alt.Y("VALUE:Q", title="率（%）"),
            color=alt.Color("METRIC:N", title="指標",
                            scale=alt.Scale(
                                domain=["CTR", "CVR"],
                                range=["#aec7e8", "#1f77b4"])),
            column=alt.Column("CHANNEL:N", title="チャネル",
                              header=alt.Header(labelAngle=-30, labelAlign="right")),
            tooltip=[
                alt.Tooltip("CHANNEL:N", title="チャネル"),
                alt.Tooltip("METRIC:N",  title="指標"),
                alt.Tooltip("VALUE:Q",   title="値(%)", format=".2f"),
            ],
        )
        .properties(height=260, width=70)
    )
    st.altair_chart(grouped)

with c_table:
    camp_df.columns = ["チャネル", "件数", "費用（円）", "CTR(%)", "CVR(%)", "CPA（円）"]
    camp_df["費用（円）"] = camp_df["費用（円）"].map("{:,.0f}".format)
    camp_df["CPA（円）"]  = camp_df["CPA（円）"].map("{:,.0f}".format)
    st.dataframe(camp_df, use_container_width=True, )

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Powered by Snowflake Streamlit in Snowflake | Data: 2024-2025 retail sample")
