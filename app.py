import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards
import streamlit.components.v1 as components

# Set page config
st.set_page_config(
    page_title="Global AI Content Impact Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .css-1d391kg {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description with emojis
st.title("🤖 Global AI Content Impact Analysis Dashboard")
st.markdown("""
    <div style='text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem; margin-bottom: 2rem;'>
        <h3>📊 Interactive Analytics Dashboard</h3>
        <p>Explore the global impact of AI across different industries, countries, and years through interactive visualizations and insights.</p>
    </div>
""", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("Global_AI_Content_Impact_Dataset.csv")
    return df

df = load_data()

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown("### 🎯 Filters")
    st.markdown("---")
    
    # Year filter with slider
    st.markdown("#### 📅 Year Range")
    year_range = st.slider(
        "Select Year Range",
        min_value=int(df['Year'].min()),
        max_value=int(df['Year'].max()),
        value=(int(df['Year'].min()), int(df['Year'].max()))
    )
    
    # Country filter with search
    st.markdown("#### 🌍 Countries")
    countries = sorted(df['Country'].unique())
    selected_countries = st.multiselect(
        "Select Countries",
        countries,
        default=countries[:5],
        key="countries"
    )
    
    # Industry filter with search
    st.markdown("#### 🏢 Industries")
    industries = sorted(df['Industry'].unique())
    selected_industries = st.multiselect(
        "Select Industries",
        industries,
        default=industries[:3],
        key="industries"
    )
    
    # AI Tools filter
    st.markdown("#### 🛠️ AI Tools")
    tools = sorted(df['Top AI Tools Used'].unique())
    selected_tools = st.multiselect(
        "Select AI Tools",
        tools,
        default=tools,
        key="tools"
    )
    
    # Regulation Status filter
    st.markdown("#### 📜 Regulation Status")
    reg_status = sorted(df['Regulation Status'].unique())
    selected_reg = st.multiselect(
        "Select Regulation Status",
        reg_status,
        default=reg_status,
        key="reg"
    )

# Filter the dataframe
filtered_df = df[
    (df['Year'].between(year_range[0], year_range[1])) &
    (df['Country'].isin(selected_countries)) &
    (df['Industry'].isin(selected_industries)) &
    (df['Top AI Tools Used'].isin(selected_tools)) &
    (df['Regulation Status'].isin(selected_reg))
]

# Key Metrics with enhanced styling
st.markdown("### 📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_adoption = filtered_df['AI Adoption Rate (%)'].mean()
    st.metric(
        "AI Adoption Rate",
        f"{avg_adoption:.2f}%",
        f"{filtered_df['AI Adoption Rate (%)'].max() - avg_adoption:.2f}% from max"
    )

with col2:
    avg_job_loss = filtered_df['Job Loss Due to AI (%)'].mean()
    st.metric(
        "Job Loss Due to AI",
        f"{avg_job_loss:.2f}%",
        f"{avg_job_loss - filtered_df['Job Loss Due to AI (%)'].min():.2f}% from min"
    )

with col3:
    avg_revenue = filtered_df['Revenue Increase Due to AI (%)'].mean()
    st.metric(
        "Revenue Increase",
        f"{avg_revenue:.2f}%",
        f"{filtered_df['Revenue Increase Due to AI (%)'].max() - avg_revenue:.2f}% from max"
    )

with col4:
    avg_collaboration = filtered_df['Human-AI Collaboration Rate (%)'].mean()
    st.metric(
        "Human-AI Collaboration",
        f"{avg_collaboration:.2f}%",
        f"{avg_collaboration - filtered_df['Human-AI Collaboration Rate (%)'].min():.2f}% from min"
    )

style_metric_cards()

# Advanced Analytics Section
st.markdown("### 📊 Advanced Analytics")

# Create tabs for different analysis sections
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🌍 Geographic", "🏢 Industry", "🔍 Deep Dive"])

with tab1:
    # Time Series Analysis with multiple metrics
    st.subheader("📈 Time Series Analysis")
    
    # Create subplot for multiple metrics
    fig_trend = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "AI Adoption Rate", "Job Loss",
            "Revenue Increase", "Human-AI Collaboration"
        )
    )
    
    metrics = [
        'AI Adoption Rate (%)',
        'Job Loss Due to AI (%)',
        'Revenue Increase Due to AI (%)',
        'Human-AI Collaboration Rate (%)'
    ]
    
    for i, metric in enumerate(metrics):
        row = i // 2 + 1
        col = i % 2 + 1
        
        yearly_data = filtered_df.groupby('Year')[metric].mean().reset_index()
        fig_trend.add_trace(
            go.Scatter(
                x=yearly_data['Year'],
                y=yearly_data[metric],
                name=metric,
                mode='lines+markers'
            ),
            row=row, col=col
        )
    
    fig_trend.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig_trend, use_container_width=True)

with tab2:
    # Geographic Analysis
    st.subheader("🌍 Geographic Analysis")
    
    # Create a choropleth map (simulated with scatter plot)
    fig_map = px.scatter_geo(
        filtered_df,
        locations='Country',
        locationmode='country names',
        color='AI Adoption Rate (%)',
        size='Revenue Increase Due to AI (%)',
        hover_name='Country',
        hover_data=['Industry', 'Year', 'AI Adoption Rate (%)'],
        title='Global AI Impact Distribution'
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Country comparison
    st.subheader("Country Comparison")
    country_metrics = filtered_df.groupby('Country').agg({
        'AI Adoption Rate (%)': 'mean',
        'Job Loss Due to AI (%)': 'mean',
        'Revenue Increase Due to AI (%)': 'mean'
    }).reset_index()
    
    fig_country = px.bar(
        country_metrics,
        x='Country',
        y=['AI Adoption Rate (%)', 'Job Loss Due to AI (%)', 'Revenue Increase Due to AI (%)'],
        title='Country-wise Metrics Comparison',
        barmode='group'
    )
    st.plotly_chart(fig_country, use_container_width=True)

with tab3:
    # Industry Analysis
    st.subheader("🏢 Industry Analysis")
    
    # Industry comparison
    industry_metrics = filtered_df.groupby('Industry').agg({
        'AI Adoption Rate (%)': 'mean',
        'Job Loss Due to AI (%)': 'mean',
        'Revenue Increase Due to AI (%)': 'mean',
        'Human-AI Collaboration Rate (%)': 'mean'
    }).reset_index()
    
    # Radar chart using plotly.graph_objects
    categories = ['AI Adoption Rate (%)', 'Job Loss Due to AI (%)', 'Revenue Increase Due to AI (%)', 'Human-AI Collaboration Rate (%)']
    fig_industry = go.Figure()
    for i, row in industry_metrics.iterrows():
        values = [row[cat] for cat in categories]
        values += values[:1]  # close the loop
        fig_industry.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            name=row['Industry']
        ))
    fig_industry.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        title='Industry Performance Radar Chart'
    )
    st.plotly_chart(fig_industry, use_container_width=True)
    
    # Industry trends over time
    st.subheader("Industry Trends Over Time")
    fig_industry_trend = px.line(
        filtered_df,
        x='Year',
        y='AI Adoption Rate (%)',
        color='Industry',
        title='Industry-wise AI Adoption Trends'
    )
    st.plotly_chart(fig_industry_trend, use_container_width=True)

with tab4:
    # Deep Dive Analysis
    st.subheader("🔍 Deep Dive Analysis")
    
    # Correlation Analysis
    st.markdown("#### Correlation Analysis")
    corr_matrix = filtered_df[[
        'AI Adoption Rate (%)',
        'Job Loss Due to AI (%)',
        'Revenue Increase Due to AI (%)',
        'Human-AI Collaboration Rate (%)'
    ]].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        title='Correlation Matrix of Key Metrics',
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # AI Tools Analysis
    st.markdown("#### AI Tools Analysis")
    tool_analysis = filtered_df.groupby('Top AI Tools Used').agg({
        'AI Adoption Rate (%)': 'mean',
        'Revenue Increase Due to AI (%)': 'mean'
    }).reset_index()
    
    fig_tools = px.scatter(
        tool_analysis,
        x='AI Adoption Rate (%)',
        y='Revenue Increase Due to AI (%)',
        text='Top AI Tools Used',
        title='AI Tools Performance Analysis'
    )
    st.plotly_chart(fig_tools, use_container_width=True)

# Interactive Data Explorer
st.markdown("### 📋 Interactive Data Explorer")
st.markdown("""
    <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem;'>
        <p>Explore the detailed data with interactive features:</p>
        <ul>
            <li>Sort by clicking column headers</li>
            <li>Filter using the search box</li>
            <li>Download data using the menu</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Enhanced data table with styling
st.dataframe(
    filtered_df.style.background_gradient(
        subset=['AI Adoption Rate (%)', 'Job Loss Due to AI (%)', 'Revenue Increase Due to AI (%)'],
        cmap='RdYlGn'
    ),
    use_container_width=True
)

# Footer with additional information
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <p>Data Source: Global AI Content Impact Dataset</p>
        <p>Last Updated: 2024</p>
    </div>
""", unsafe_allow_html=True) 