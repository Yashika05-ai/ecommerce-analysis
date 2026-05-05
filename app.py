import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title=" E-commerce Dashboard", layout="wide")

# Custom CSS (Advanced UI)
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #00f5d4;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
}
.footer {
    text-align: center;
    color: grey;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# Load Data
df = pd.read_csv("cleaned_data.csv")

# HEADER
st.title("🚀E-commerce-Analysis Dashboard")

# KPI Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='card'><h3>📦 Products</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='card'><h3>💰 Avg Price</h3><h2>{round(df['price'].mean(),2)}</h2></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='card'><h3>⭐ Avg Rating</h3><h2>{round(df['rating'].mean(),2)}</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# SIDEBAR
st.sidebar.title("🔍 Smart Filters")

category = st.sidebar.selectbox("Category", df['category'].unique())

price_range = st.sidebar.slider(
    "Price Range",
    float(df['price'].min()),
    float(df['price'].max()),
    (float(df['price'].min()), float(df['price'].max()))
)

rating_filter = st.sidebar.slider(
    "Minimum Rating",
    float(df['rating'].min()),
    float(df['rating'].max()),
    float(df['rating'].min())
)

search = st.sidebar.text_input("🔎 Search Product")

# APPLY FILTERS
filtered_df = df[
    (df['category'] == category) &
    (df['price'] >= price_range[0]) &
    (df['price'] <= price_range[1]) &
    (df['rating'] >= rating_filter)
]

if search:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search, case=False)]

# CHARTS
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Price vs Rating")
    st.scatter_chart(filtered_df[['price', 'rating']])

with col2:
    st.subheader("⭐ Rating by Category")
    st.bar_chart(df.groupby('price_category')['rating'].mean())

# TOP PRODUCTS
st.subheader("🏆 Top Value Products")

top_products = df.sort_values(by='value_score', ascending=False).head(5)

for i, row in top_products.iterrows():
    st.markdown(f"""
    <div class='card'>
        <h3>{row['title']}</h3>
        <p>💰 Price: {row['price']} | ⭐ Rating: {row['rating']}</p>
    </div>
    """, unsafe_allow_html=True)

# DATA TABLE
st.subheader("📊 Full Dataset")
st.dataframe(filtered_df, use_container_width=True)

# FOOTER
st.markdown("<div class='footer'>✨ Built with Streamlit | Ultra Premium UI</div>", unsafe_allow_html=True)
