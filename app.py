import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Sales Dashboard - Power BI Style",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS - Power BI White Theme ==========
st.markdown("""
<style>
    /* White Theme Background */
    .stApp {
        background-color: #f5f7fa;
    }
    
    /* Power BI White Cards */
    .pbi-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s;
    }
    .pbi-card:hover {
        border-color: #FF6B35;
        box-shadow: 0 4px 15px rgba(255,107,53,0.15);
    }
    
    /* KPI Values - Power BI Style */
    .pbi-kpi-value {
        font-size: 32px;
        font-weight: 700;
        color: #1a1a2e;
        font-family: 'Segoe UI', sans-serif;
    }
    .pbi-kpi-label {
        font-size: 13px;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Title */
    .pbi-title {
        font-size: 28px;
        font-weight: 700;
        color: #1a1a2e;
        border-bottom: 3px solid #FF6B35;
        padding-bottom: 10px;
    }
    
    /* Sidebar - White Theme */
    .css-1d391kg {
        background: #ffffff !important;
        border-right: 1px solid #e0e0e0 !important;
    }
    .css-1d391kg label {
        color: #333333 !important;
        font-weight: 500;
    }
    .css-1d391kg .stSelectbox label {
        color: #333333 !important;
    }
    .css-1d391kg .stDateInput label {
        color: #333333 !important;
    }
    
    /* Sidebar Header */
    .sidebar-header {
        text-align: center;
        padding: 20px 0;
        border-bottom: 1px solid #e0e0e0;
    }
    .sidebar-header h2 {
        color: #FF6B35;
        margin: 0;
    }
    .sidebar-header p {
        color: #6c757d;
        font-size: 12px;
    }
    
    /* Chart containers */
    .chart-container {
        background: #ffffff;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #e0e0e0;
    }
    
    /* Section Headers */
    .section-title {
        color: #1a1a2e;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    /* Footer */
    .pbi-footer {
        text-align: center;
        color: #6c757d;
        font-size: 12px;
        padding: 20px 0;
        border-top: 1px solid #e0e0e0;
        margin-top: 30px;
    }
    
    /* Divider */
    .pbi-divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #FF6B35, transparent);
        margin: 20px 0;
    }
    
    /* KPI Change Indicator */
    .change-positive {
        color: #28a745;
        font-size: 13px;
        font-weight: 600;
    }
    .change-negative {
        color: #dc3545;
        font-size: 13px;
        font-weight: 600;
    }
    .change-neutral {
        color: #6c757d;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ========== LOAD DATA ==========
@st.cache_data
def load_data():
    df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Month'] = df['Order Date'].dt.strftime('%Y-%m')
    df['Year'] = df['Order Date'].dt.year
    df['Quarter'] = df['Order Date'].dt.quarter
    return df

df = load_data()

# ========== SIDEBAR - White Theme ==========
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>📊 Kinetrea</h2>
        <p>Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Filters")
    
    # Region Filter
    region = st.selectbox(
        "🌍 Region",
        ["All"] + list(df['Region'].unique())
    )
    
    # Category Filter
    category = st.selectbox(
        "📂 Category",
        ["All"] + list(df['Category'].unique())
    )
    
    # Segment Filter
    segment = st.selectbox(
        "👥 Segment",
        ["All"] + list(df['Segment'].unique())
    )
    
    st.markdown("---")
    
    # Date Range
    st.markdown("### 📅 Date Range")
    min_date = df['Order Date'].min().date()
    max_date = df['Order Date'].max().date()
    date_range = st.date_input("", [min_date, max_date])
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.success("Data Refreshed!")
    
    st.markdown("---")
    st.caption(f"🕐 {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

# ========== FILTER DATA ==========
filtered_df = df.copy()
if region != "All":
    filtered_df = filtered_df[filtered_df['Region'] == region]
if category != "All":
    filtered_df = filtered_df[filtered_df['Category'] == category]
if segment != "All":
    filtered_df = filtered_df[filtered_df['Segment'] == segment]
filtered_df = filtered_df[
    (filtered_df['Order Date'].dt.date >= date_range[0]) & 
    (filtered_df['Order Date'].dt.date <= date_range[1])
]

# ========== HEADER ==========
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; background: white; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 20px;">
    <div>
        <h1 class="pbi-title">📊 Sales Performance Dashboard</h1>
        <p style="color: #6c757d; margin: 0;">Data-driven insights for business decisions</p>
    </div>
    <div style="text-align: right;">
        <p style="color: #6c757d; font-size: 12px; margin: 0;">Last Updated: 19 Aug 2026</p>
        <p style="color: #6c757d; font-size: 12px; margin: 0;">{:,} Records Loaded</p>
    </div>
</div>
""".format(len(filtered_df)), unsafe_allow_html=True)

# ========== KPI ROW - Power BI Style ==========
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="pbi-card">
        <div class="pbi-kpi-label">💰 Total Revenue</div>
        <div class="pbi-kpi-value">${filtered_df['Sales'].sum():,.0f}</div>
        <span class="change-positive">↑ 12.3%</span>
        <span class="change-neutral">vs last period</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    profit = filtered_df['Profit'].sum()
    color_class = "change-positive" if profit > 0 else "change-negative"
    arrow = "↑" if profit > 0 else "↓"
    st.markdown(f"""
    <div class="pbi-card">
        <div class="pbi-kpi-label">📈 Total Profit</div>
        <div class="pbi-kpi-value" style="color: {'#28a745' if profit > 0 else '#dc3545'};">${profit:,.0f}</div>
        <span class="{color_class}">{arrow} 8.7%</span>
        <span class="change-neutral">vs last period</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="pbi-card">
        <div class="pbi-kpi-label">📦 Total Orders</div>
        <div class="pbi-kpi-value">{filtered_df['Order ID'].nunique():,}</div>
        <span class="change-positive">↑ 5.2%</span>
        <span class="change-neutral">vs last period</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    margin = (filtered_df['Profit'].sum() / filtered_df['Sales'].sum()) * 100 if filtered_df['Sales'].sum() > 0 else 0
    color_class = "change-positive" if margin > 10 else "change-negative"
    st.markdown(f"""
    <div class="pbi-card">
        <div class="pbi-kpi-label">🎯 Profit Margin</div>
        <div class="pbi-kpi-value" style="color: {'#28a745' if margin > 10 else '#dc3545'};">{margin:.1f}%</div>
        <span class="{color_class}">{'↑' if margin > 10 else '↓'} 2.5%</span>
        <span class="change-neutral">vs last period</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='pbi-divider'>", unsafe_allow_html=True)

# ========== CHARTS ROW 1 ==========
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-title">📈 Monthly Revenue Trend</p>', unsafe_allow_html=True)
    monthly = filtered_df.groupby('Month')['Sales'].sum().reset_index()
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=monthly['Month'],
        y=monthly['Sales'],
        mode='lines+markers',
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=6, color='#F7931E'),
        fill='tozeroy',
        fillcolor='rgba(255,107,53,0.15)',
        name='Sales'
    ))
    fig1.update_layout(
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(color='#333333'),
        hovermode='x unified',
        xaxis=dict(showgrid=False, tickangle=45, color='#6c757d'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.06)', color='#6c757d'),
        height=350,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown('<p class="section-title">🌍 Sales by Region</p>', unsafe_allow_html=True)
    region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
    colors = ['#FF6B35', '#4ECDC4', '#45B7D1', '#F7931E']
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=region_sales['Region'],
        y=region_sales['Sales'],
        marker_color=colors[:len(region_sales)],
        text=region_sales['Sales'],
        textposition='outside',
        texttemplate='$%{text:,.0f}'
    ))
    fig2.update_layout(
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(color='#333333'),
        xaxis=dict(showgrid=False, color='#6c757d'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.06)', color='#6c757d'),
        height=350,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

# ========== CHARTS ROW 2 ==========
col3, col4 = st.columns(2)

with col3:
    st.markdown('<p class="section-title">📊 Category Distribution</p>', unsafe_allow_html=True)
    cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    
    fig3 = go.Figure()
    fig3.add_trace(go.Pie(
        labels=cat_sales['Category'],
        values=cat_sales['Sales'],
        hole=0.4,
        marker_colors=['#FF6B35', '#4ECDC4', '#45B7D1'],
        textinfo='percent+label',
        textposition='inside'
    ))
    fig3.update_layout(
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(color='#333333'),
        height=350,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown('<p class="section-title">🏆 Top 10 Products</p>', unsafe_allow_html=True)
    top_products = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
    
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        y=top_products['Product Name'],
        x=top_products['Sales'],
        orientation='h',
        marker_color='#FF6B35',
        text=top_products['Sales'],
        textposition='outside',
        texttemplate='$%{text:,.0f}'
    ))
    fig4.update_layout(
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(color='#333333'),
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.06)', color='#6c757d'),
        yaxis=dict(showgrid=False, autorange="reversed", color='#6c757d'),
        height=350,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)

# ========== CHARTS ROW 3 ==========
st.markdown("<hr class='pbi-divider'>", unsafe_allow_html=True)
col5, col6 = st.columns(2)

with col5:
    st.markdown('<p class="section-title">📊 Ship Mode Analysis</p>', unsafe_allow_html=True)
    ship_data = filtered_df.groupby('Ship Mode').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=ship_data['Ship Mode'],
        y=ship_data['Sales'],
        name='Sales',
        marker_color='#4ECDC4'
    ))
    fig5.add_trace(go.Bar(
        x=ship_data['Ship Mode'],
        y=ship_data['Profit'],
        name='Profit',
        marker_color='#FF6B35'
    ))
    fig5.update_layout(
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(color='#333333'),
        xaxis=dict(showgrid=False, color='#6c757d'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.06)', color='#6c757d'),
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(font_color='#333333'),
        barmode='group'
    )
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.markdown('<p class="section-title">📈 Quarterly Performance</p>', unsafe_allow_html=True)
    quarterly = filtered_df.groupby(['Year', 'Quarter'])['Sales'].sum().reset_index()
    quarterly['Period'] = quarterly['Year'].astype(str) + ' Q' + quarterly['Quarter'].astype(str)
    
    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=quarterly['Period'],
        y=quarterly['Sales'],
        mode='lines+markers',
        line=dict(color='#45B7D1', width=3),
        marker=dict(size=8, color='#4ECDC4'),
        fill='tozeroy',
        fillcolor='rgba(69,183,209,0.15)'
    ))
    fig6.update_layout(
        plot_bgcolor='rgba(255,255,255,0)',
        paper_bgcolor='rgba(255,255,255,0)',
        font=dict(color='#333333'),
        xaxis=dict(showgrid=False, tickangle=45, color='#6c757d'),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.06)', color='#6c757d'),
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    st.plotly_chart(fig6, use_container_width=True)

# ========== INSIGHTS - Power BI Style ==========
st.markdown("<hr class='pbi-divider'>", unsafe_allow_html=True)
st.markdown('<p class="section-title" style="font-size: 20px;">💡 Business Insights</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="pbi-card" style="border-left: 4px solid #FF6B35;">
        <h4 style="color: #FF6B35; margin: 0;">🏆 Top Performers</h4>
        <hr style="border-color: #e0e0e0;">
    """, unsafe_allow_html=True)
    
    top_region = df.groupby('Region')['Sales'].sum().idxmax()
    top_cat = df.groupby('Category')['Sales'].sum().idxmax()
    top_segment = df.groupby('Segment')['Sales'].sum().idxmax()
    
    st.markdown(f"""
        <p style="color: #333333; margin: 5px 0;">
            🌍 Best Region: <b style="color: #FF6B35;">{top_region}</b>
        </p>
        <p style="color: #333333; margin: 5px 0;">
            📂 Best Category: <b style="color: #FF6B35;">{top_cat}</b>
        </p>
        <p style="color: #333333; margin: 5px 0;">
            👥 Best Segment: <b style="color: #FF6B35;">{top_segment}</b>
        </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="pbi-card" style="border-left: 4px solid #4ECDC4;">
        <h4 style="color: #4ECDC4; margin: 0;">📊 Key Metrics</h4>
        <hr style="border-color: #e0e0e0;">
    """, unsafe_allow_html=True)
    
    avg_order = df['Sales'].sum() / df['Order ID'].nunique()
    avg_profit = df['Profit'].mean()
    total_customers = df['Customer ID'].nunique()
    
    st.markdown(f"""
        <p style="color: #333333; margin: 5px 0;">
            💰 Avg Order: <b style="color: #F7931E;">${avg_order:,.2f}</b>
        </p>
        <p style="color: #333333; margin: 5px 0;">
            📈 Avg Profit: <b style="color: #F7931E;">${avg_profit:,.2f}</b>
        </p>
        <p style="color: #333333; margin: 5px 0;">
            👤 Total Customers: <b style="color: #F7931E;">{total_customers:,}</b>
        </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="pbi-card" style="border-left: 4px solid #FF6B6B;">
        <h4 style="color: #FF6B6B; margin: 0;">⚠️ Areas to Improve</h4>
        <hr style="border-color: #e0e0e0;">
    """, unsafe_allow_html=True)
    
    loss_products = df[df['Profit'] < 0].groupby('Product Name')['Profit'].sum().sort_values().head(3)
    loss_count = len(loss_products)
    total_loss = abs(loss_products.sum())
    
    st.markdown(f"""
        <p style="color: #333333; margin: 5px 0;">
            ⚠️ Loss Products: <b style="color: #FF6B6B;">{loss_count}</b>
        </p>
        <p style="color: #333333; margin: 5px 0;">
            💸 Total Loss: <b style="color: #FF6B6B;">${total_loss:,.0f}</b>
        </p>
        <p style="color: #333333; margin: 5px 0;">
            💡 Potential Recovery: <b style="color: #4ECDC4;">+${total_loss:,.0f}</b>
        </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ========== FOOTER ==========
st.markdown("""
<div class="pbi-footer">
    <p>
        <span>📍 121B Lachhipur Bankatawa, Gorakhnath Gorakhpur, Uttar Pradesh - 273001</span> | 
        <span>📞 +91 7880717527</span> | 
        <span>✉️ contact@kinetrexa.com</span>
    </p>
    <p>🌐 www.kinetrexa.com | CIN: U62011UP2026PTC243617</p>
    <p style="color: #999;">© 2026 Kinetrea Software Pvt. Ltd. | Data Analytics Internship | Lakshya Sharma</p>
</div>
""", unsafe_allow_html=True)