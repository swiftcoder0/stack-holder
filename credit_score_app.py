import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="CredIntel: Explainable Credit Scoring",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved styling with better contrast
st.markdown("""
<style>
    /* Main styles */
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .sub-header {
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    
    /* Card styles */
    .card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #e0e0e0;
    }
    
    .score-card {
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 20px rgba(75, 108, 183, 0.3);
    }
    
    /* Trend indicators */
    .up-trend {
        color: #27ae60;
        font-weight: 600;
    }
    
    .down-trend {
        color: #e74c3c;
        font-weight: 600;
    }
    
    /* Event styles */
    .event-positive {
        border-left: 4px solid #27ae60;
        padding: 12px 15px;
        background-color: #eafaf1;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        color: #145a32;
    }
    
    .event-negative {
        border-left: 4px solid #e74c3c;
        padding: 12px 15px;
        background-color: #fdedec;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        color: #922b21;
    }
    
    /* Feature boxes */
    .feature-box {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #3498db;
        color: #2c3e50;
    }
    
    .feature-positive {
        border-left-color: #27ae60;
    }
    
    .feature-negative {
        border-left-color: #e74c3c;
    }
    
    /* Alert styles */
    .alert {
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        font-weight: 500;
    }
    
    .alert-danger {
        background-color: #fde8e8;
        color: #922b21;
        border-left: 4px solid #e74c3c;
    }
    
    .alert-success {
        background-color: #eafaf1;
        color: #145a32;
        border-left: 4px solid #27ae60;
    }
    
    .alert-info {
        background-color: #e8f4fd;
        color: #1a5276;
        border-left: 4px solid #3498db;
    }
    
    /* Sidebar improvements */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        padding: 10px;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.4rem;
        color: #2c3e50;
        margin-bottom: 15px;
        font-weight: 600;
        padding-bottom: 8px;
        border-bottom: 2px solid #eaeaea;
    }
    
    /* Make sure all text is visible */
    body {
        color: #2c3e50 !important;
    }
    
    /* Improve select box styling */
    .stSelectbox, .stMultiselect {
        background-color: white;
    }
    
    /* Fix any white-on-white text issues */
    .st-bd, .st-bj, .st-be, .st-bh, .st-bi {
        color: #2c3e50 !important;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data
def generate_sample_data():
    # Generate dates for the last 30 days
    dates = [datetime.now().date() - timedelta(days=i) for i in range(30, 0, -1)]
    
    # Base score with some randomness
    base_score = 75
    scores = [base_score + np.random.normal(0, 2) for _ in range(30)]
    
    # Create some meaningful trends
    for i in range(10, 15):
        scores[i] = scores[i] - 8  # Simulate a drop
    for i in range(20, 30):
        scores[i] = scores[i] + 6  # Simulate recovery
    
    # Create events
    events = [
        {"date": dates[10], "title": "Exceptional Q2 Earnings Report", "impact": +3, "type": "positive"},
        {"date": dates[12], "title": "CEO Unexpected Resignation", "impact": -5, "type": "negative"},
        {"date": dates[15], "title": "Successful New Product Launch", "impact": +2, "type": "positive"},
        {"date": dates[25], "title": "Favorable Industry Regulation Changes", "impact": +4, "type": "positive"},
        {"date": dates[5], "title": "Major Contract Signed with Government", "impact": +3, "type": "positive"},
        {"date": dates[18], "title": "Supply Chain Disruption Announcement", "impact": -4, "type": "negative"}
    ]
    
    # Feature importance data
    features = [
        {"name": "Debt-to-Equity Ratio", "importance": 0.23, "impact": "negative", "current_value": "1.8", "trend": "improving"},
        {"name": "Operating Cash Flow", "importance": 0.19, "impact": "positive", "current_value": "$2.4B", "trend": "stable"},
        {"name": "Market Sentiment", "importance": 0.16, "impact": "positive", "current_value": "72/100", "trend": "improving"},
        {"name": "Industry Position", "importance": 0.14, "impact": "positive", "current_value": "Market Leader", "trend": "stable"},
        {"name": "Loan Default History", "importance": 0.12, "impact": "negative", "current_value": "0.8%", "trend": "worsening"},
        {"name": "Revenue Growth", "importance": 0.08, "impact": "positive", "current_value": "12.5%", "trend": "improving"}
    ]
    
    return dates, scores, events, features

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">CredIntel Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Explainable Credit Intelligence Platform</p>', unsafe_allow_html=True)
    
    # Generate sample data
    dates, scores, events, features = generate_sample_data()
    
    # Sidebar for company selection
    with st.sidebar:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏢 Company Selection")
        company = st.selectbox(
            "Choose Company to Analyze",
            ["TechCorp Inc.", "GlobalManufacturing Ltd.", "ServiceProvider Co.", "RetailGiant Group"],
            index=1,
            help="Select a company to view its credit score analysis"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Comparison Tools")
        comp_companies = st.multiselect(
            "Select companies to compare:",
            ["TechCorp Inc.", "GlobalManufacturing Ltd.", "ServiceProvider Co.", "RetailGiant Group"],
            default=["TechCorp Inc.", "GlobalManufacturing Ltd."],
            help="Choose multiple companies for side-by-side comparison"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("ℹ️ About This Platform")
        st.info("""
        **CredIntel** provides transparent, explainable credit scoring using:
        - Real-time data analysis
        - AI-powered risk assessment
        - Clear factor breakdowns
        - Event impact tracking
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content - two columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Current score card
        current_score = scores[-1]
        score_change = scores[-1] - scores[-2]
        
        st.markdown(f"""
        <div class="score-card">
            <h3>Current Credit Score</h3>
            <h1 style="font-size: 4rem; margin: 10px 0;">{current_score:.0f}</h1>
            <h4>/100 Rating</h4>
            <div style="margin: 15px 0;">
                <span style="font-size: 1.2rem;">Trend: </span>
                <span class={'up-trend' if score_change >= 0 else 'down-trend'} style="font-size: 1.2rem;">
                    {score_change:+.1f} 
                    {'↗' if score_change >= 0 else '↘'}
                </span>
            </div>
            <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Crisis alert
        if score_change <= -3:
            st.markdown(f"""
            <div class="alert alert-danger">
                <b>🚨 Significant Score Drop Detected</b><br>
                Score decreased by {abs(score_change):.1f} points. Possible crisis event requiring attention.
            </div>
            """, unsafe_allow_html=True)
        elif score_change >= 3:
            st.markdown(f"""
            <div class="alert alert-success">
                <b>📈 Significant Improvement Detected</b><br>
                Score increased by {score_change:.1f} points. Positive development detected.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert alert-info">
                <b>📊 Stable Performance</b><br>
                Minimal change ({score_change:+.1f} points) since last update.
            </div>
            """, unsafe_allow_html=True)
        
        # Feature importance
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📋 Key Score Drivers")
        st.caption("Factors influencing the current credit score")
        
        for feature in features:
            emoji = "✅" if feature["impact"] == "positive" else "⚠️"
            trend_emoji = "↗" if feature["trend"] == "improving" else "↘" if feature["trend"] == "worsening" else "→"
            feature_class = "feature-box feature-positive" if feature["impact"] == "positive" else "feature-box feature-negative"
            
            st.markdown(f"""
            <div class="{feature_class}">
                <b>{emoji} {feature['name']}</b> 
                <span style="float: right;">
                    Impact: <span class={'up-trend' if feature['impact'] == 'positive' else 'down-trend'}>
                    {feature['importance']*100:.1f}%</span>
                </span>
                <br>
                <span style="font-size: 0.9rem;">Current: {feature['current_value']} </span>
                <span class={'up-trend' if feature['trend'] == 'improving' else 'down-trend' if feature['trend'] == 'worsening' else ''}>
                    {trend_emoji}
                </span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Score history chart
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📈 Credit Score History")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=scores, 
            mode='lines+markers',
            name='Credit Score',
            line=dict(color='#3498db', width=4),
            marker=dict(size=6)
        ))
        
        # Add event markers
        for event in events:
            event_date = event["date"]
            event_idx = dates.index(event_date)
            event_color = '#27ae60' if event["type"] == "positive" else '#e74c3c'
            
            fig.add_trace(go.Scatter(
                x=[event_date], y=[scores[event_idx]],
                mode='markers',
                marker=dict(color=event_color, size=14, symbol='diamond', line=dict(width=2, color='white')),
                name=event["title"],
                hovertemplate=f"{event['title']}<br>Impact: {event['impact']} points<br>Date: %{{x}}"
            ))
        
        # Fixed the chart layout - removed the problematic update_xaxis/update_yaxis calls
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Credit Score",
            hovermode="closest",
            height=450,
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e0e0e0'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Event explanations
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📅 Recent Events & Impact")
        st.caption("How specific events affected the credit score")
        
        for event in sorted(events, key=lambda x: x["date"], reverse=True)[:5]:  # Show only 5 most recent
            event_class = "event-positive" if event["type"] == "positive" else "event-negative"
            impact_sign = "+" if event["impact"] > 0 else ""
            emoji = "📈" if event["type"] == "positive" else "📉"
            
            st.markdown(f"""
            <div class="{event_class}">
                <b>{emoji} {event['date'].strftime('%b %d')}: {event['title']}</b>
                <span style="float: right;">Impact: 
                    <span class={'up-trend' if event['type'] == 'positive' else 'down-trend'}>
                        {impact_sign}{event['impact']} points
                    </span>
                </span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Comparison tool
        if comp_companies and len(comp_companies) > 1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🔍 Company Comparison")
            
            comp_scores = [72, 68, 81, 65]  # Sample scores
            comp_data = pd.DataFrame({
                "Company": comp_companies,
                "Score": [comp_scores[i] for i in range(len(comp_companies))]
            })
            
            fig = px.bar(comp_data, x="Company", y="Score", 
                         title="Credit Score Comparison",
                         color="Score", color_continuous_scale="RdYlGn",
                         text="Score")
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            
            # Fixed the chart layout - removed the problematic update_xaxis/update_yaxis calls
            fig.update_layout(
                showlegend=False, 
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2c3e50'),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e0e0e0'),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()