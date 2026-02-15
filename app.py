import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Indian Companies Dashboard", layout="wide")

# ---------- Custom CSS for colorful cards ----------
st.markdown("""
<style>
.kpi-card {
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
.kpi-card.green {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}
.kpi-card.orange {
    background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
}
.kpi-title {
    font-size: 16px;
    opacity: 0.9;
}
.kpi-value {
    font-size: 36px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Indian Companies – Industry Insights Dashboard")

# ---------- Load Data ----------
@st.cache_data
def load_data():
    df = pd.read_excel("DVDM_Company_list FOR SET 1.xlsm")
    return df

df = load_data()
df.columns = [c.strip() for c in df.columns]

# ---------- Sidebar Filters ----------
st.sidebar.header("🔎 Filters")

selected_industries = st.sidebar.multiselect(
    "Select Industry",
    options=sorted(df["Industry"].dropna().unique()),
    default=[]
)

search_company = st.sidebar.text_input("Search Company Name")

filtered_df = df.copy()

if selected_industries:
    filtered_df = filtered_df[filtered_df["Industry"].isin(selected_industries)]

if search_company:
    filtered_df = filtered_df[filtered_df["Company Name"].str.contains(search_company, case=False, na=False)]

# ---------- KPI Section (Colorful Cards) ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total Companies</div>
        <div class="kpi-value">{filtered_df['Company Name'].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-title">Total Industries</div>
        <div class="kpi-value">{filtered_df['Industry'].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card orange">
        <div class="kpi-title">Total Records</div>
        <div class="kpi-value">{len(filtered_df)}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------- Charts ----------
left, right = st.columns(2)

# Industry-wise Count (Bar Chart)
industry_count = (
    filtered_df.groupby("Industry")["Company Name"]
    .nunique()
    .reset_index(name="Company Count")
    .sort_values("Company Count", ascending=False)
)

with left:
    st.subheader("🏭 Top 5 Industries by Company Count")
    top5 = industry_count.head(5)
    fig_bar = px.bar(
        top5,
        x="Industry",
        y="Company Count",
        title="Top 5 Industries",
        text="Company Count"
    )
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

# Pie Chart (Industry Share)
with right:
    st.subheader("🥧 Industry Share")
    fig_pie = px.pie(
        industry_count,
        names="Industry",
        values="Company Count",
        title="Industry-wise Share",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------- Tables ----------
st.subheader("📋 Company List (Filtered)")
st.dataframe(filtered_df, use_container_width=True)

# ---------- Download Button ----------
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_companies.csv",
    mime="text/csv"
)

# ---------- Insights ----------
st.success(
    "💡 Insights: This dashboard highlights the distribution of companies across industries. "
    "Financial Services and Capital Goods show strong representation, indicating sector dominance. "
    "Interactive filters enable focused exploration by industry and company name."
)
