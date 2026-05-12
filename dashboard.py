import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import random
import time

# Mobile-optimized page configuration
st.set_page_config(
    page_title="AI Migration Platform - Leena Adapakala",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto"
)

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import with error handling
try:
    from ai_models.application_analyzer import ApplicationAnalyzer
    analyzer_available = True
except:
    analyzer_available = False

# Mobile-first responsive CSS
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .main-header {
        font-size: clamp(1.8rem, 5vw, 3rem);
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        line-height: 1.2;
    }
    
    .creator-info {
        text-align: center;
        font-style: italic;
        color: #666;
        margin-bottom: 2rem;
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        background: rgba(31, 119, 180, 0.1);
        padding: 0.75rem;
        border-radius: 8px;
    }
    
    /* Mobile-optimized metrics */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        font-weight: 700;
        color: #1f77b4;
        margin: 0;
    }
    
    .metric-label {
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        color: #495057;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    
    .metric-delta {
        font-size: clamp(0.8rem, 2vw, 0.9rem);
        color: #28a745;
        margin: 0.25rem 0 0 0;
        font-weight: 600;
    }
    
    /* Mobile-friendly buttons */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        transition: all 0.2s ease;
    }
    
    /* Analysis results styling */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    /* Mobile table styling */
    .mobile-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .mobile-card h4 {
        color: #1f77b4;
        margin: 0 0 0.5rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            padding: 0.5rem;
        }
        
        .creator-info {
            font-size: 0.9rem;
            padding: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .block-container {
            padding: 1rem 0.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.5rem;
        }
        
        .metric-card {
            padding: 0.75rem;
            margin-bottom: 0.75rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🤖 AI-Powered Azure Migration Platform</h1>', unsafe_allow_html=True)
st.markdown('<div class="creator-info">Created by <strong>Leena Adapakala</strong> | 🚀 AI-Driven Cloud Migration Solutions</div>', unsafe_allow_html=True)

# Initialize session state
if 'analyzer' not in st.session_state:
    if analyzer_available:
        st.session_state.analyzer = ApplicationAnalyzer()
    else:
        st.session_state.analyzer = None

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []

# Navigation with mobile detection
st.sidebar.header("🚀 Navigation")
st.sidebar.markdown("*Select a feature to explore AI-powered migration capabilities*")

# Mobile mode toggle
mobile_mode = st.sidebar.checkbox("📱 Mobile Mode", False, help="Optimized layout for mobile devices")

page = st.sidebar.selectbox(
    "Choose Feature:",
    ["🏠 Overview", "📊 Application Analysis", "📈 Portfolio Dashboard"],
    key="main_navigation"
)

# Helper functions
def display_mobile_metric(label, value, delta, icon="📊"):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{icon} {value}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-delta">↗️ {delta}</div>
    </div>
    """, unsafe_allow_html=True)

def display_desktop_metrics(metrics_data):
    cols = st.columns(len(metrics_data))
    for i, (label, value, delta, icon) in enumerate(metrics_data):
        with cols[i]:
            st.metric(label=f"{icon} {label}", value=value, delta=delta)

def simulate_analysis(app_name):
    """Simulate AI analysis with realistic results"""
    name_lower = app_name.lower()
    
    if any(word in name_lower for word in ['bank', 'financial', 'payment', 'trading']):
        app_type = 'monolith'
        complexity = random.randint(4, 5)
        lines = random.randint(80000, 150000)
        traditional_weeks = random.randint(180, 250)
    elif any(word in name_lower for word in ['api', 'service', 'micro']):
        app_type = 'microservice'
        complexity = random.randint(1, 3)
        lines = random.randint(5000, 15000)
        traditional_weeks = random.randint(15, 35)
    elif any(word in name_lower for word in ['web', 'portal', 'dashboard', 'ui']):
        app_type = 'web-app'
        complexity = random.randint(2, 4)
        lines = random.randint(20000, 50000)
        traditional_weeks = random.randint(40, 80)
    else:
        app_type = 'middleware'
        complexity = random.randint(2, 4)
        lines = random.randint(30000, 80000)
        traditional_weeks = random.randint(60, 120)
    
    # AI optimization calculations
    ai_reduction_factor = random.uniform(0.20, 0.35)
    ai_weeks = traditional_weeks * ai_reduction_factor
    
    # Team and cost calculations
    traditional_team = max(4, int(traditional_weeks / 8))
    ai_team = max(2, int(ai_weeks / 8))
    
    traditional_cost = (traditional_team * traditional_weeks * 2500) + (traditional_weeks * 400)
    ai_cost = (ai_team * ai_weeks * 2800) + (ai_weeks * 300) + 20000
    
    cost_savings = traditional_cost - ai_cost
    time_saved = traditional_weeks - ai_weeks
    time_savings_pct = (time_saved / traditional_weeks) * 100
    
    # Migration approach
    if complexity <= 2:
        approach = "AI-Guided Lift & Shift"
    elif complexity <= 3:
        approach = "AI-Assisted Modernization"
    else:
        approach = "AI-Driven Cloud-Native Transformation"
    
    return {
        'app_name': app_name,
        'app_type': app_type,
        'complexity': complexity,
        'lines_of_code': lines,
        'traditional_weeks': round(traditional_weeks, 1),
        'ai_weeks': round(ai_weeks, 1),
        'time_saved': round(time_saved, 1),
        'time_savings_pct': round(time_savings_pct, 1),
        'traditional_team': traditional_team,
        'ai_team': ai_team,
        'traditional_cost': int(traditional_cost),
        'ai_cost': int(ai_cost),
        'cost_savings': int(cost_savings),
        'approach': approach
    }

# PAGE CONTENT
if page == "🏠 Overview":
    st.header("🎯 Platform Overview")
    st.markdown("*Transform enterprise cloud migration from months to weeks using artificial intelligence*")
    
    # Key metrics
    metrics_data = [
        ("Time Reduction", "75%", "vs Traditional", "⏱️"),
        ("Cost Savings", "$3.8M", "Average Portfolio", "💰"),
        ("AI Accuracy", "95%", "Prediction Rate", "🎯"),
        ("Automation", "90%", "Tasks Automated", "⚡")
    ]
    
    if mobile_mode:
        for label, value, delta, icon in metrics_data:
            display_mobile_metric(label, value, delta, icon)
    else:
        display_desktop_metrics(metrics_data)
    
    # Features section
    if mobile_mode:
        st.subheader("🤖 AI-Powered Features")
        st.markdown("""
        - **Smart Application Analysis**: Automatic complexity assessment
        - **Predictive Planning**: ML-based effort and cost estimation  
        - **Portfolio Optimization**: Multi-application analysis
        - **Risk Assessment**: AI-identified challenges and solutions
        - **Resource Optimization**: Intelligent sizing and scaling
        """)
        
        st.subheader("📊 Business Benefits")
        st.markdown("""
        - **75% faster** migration timelines
        - **93% cost reduction** through optimization
        - **Smaller teams** with higher productivity
        - **Data-driven decisions** replacing guesswork
        - **Predictable outcomes** with quantified ROI
        """)
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🤖 AI-Powered Features")
            st.markdown("""
            - **Smart Application Analysis**: Automatic complexity assessment
            - **Predictive Planning**: ML-based effort and cost estimation  
            - **Portfolio Optimization**: Multi-application analysis
            - **Risk Assessment**: AI-identified challenges and solutions
            - **Resource Optimization**: Intelligent sizing and scaling
            """)
        
        with col2:
            st.subheader("📊 Business Benefits")
            st.markdown("""
            - **75% faster** migration timelines
            - **93% cost reduction** through optimization
            - **Smaller teams** with higher productivity
            - **Data-driven decisions** replacing guesswork
            - **Predictable outcomes** with quantified ROI
            """)
    
    # Sample results
    st.subheader("🏆 Demonstrated Results")
    
    sample_results = pd.DataFrame({
        'Application Type': ['Banking Core System', 'E-commerce API', 'Customer Portal', 'Trading Platform'],
        'Traditional (weeks)': [217, 23, 57, 105],
        'AI-Optimized (weeks)': [37, 5, 13, 29],
        'Time Savings': ['83%', '78%', '77%', '72%'],
        'Cost Savings': ['$14.4M', '$186K', '$936K', '$3.2M']
    })
    
    if mobile_mode:
        for _, row in sample_results.iterrows():
            st.markdown(f"""
            <div class="mobile-card">
                <h4>{row['Application Type']}</h4>
                <p><strong>Traditional:</strong> {row['Traditional (weeks)']} weeks → <strong>AI:</strong> {row['AI-Optimized (weeks)']} weeks</p>
                <p><strong>Savings:</strong> {row['Time Savings']} time, {row['Cost Savings']} cost</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.dataframe(sample_results, use_container_width=True)

elif page == "📊 Application Analysis":
    st.header("📊 AI Application Analysis")
    st.markdown("*Get instant AI-powered migration analysis for any enterprise application*")
    
    # FIXED: Input section with proper mobile handling
    if mobile_mode:
        # Single column layout for mobile
        app_name = st.text_input(
            "Enter Application Name:",
            placeholder="e.g., Banking Core System, Payment API, Customer Portal",
            key="application_input_mobile",
            help="Enter any application name to get AI analysis"
        )
        
        analyze_btn = st.button("🔍 Analyze Application", type="primary", key="analyze_button_mobile")
        
    else:
        # Two column layout for desktop
        col1, col2 = st.columns([3, 1])
        
        with col1:
            app_name = st.text_input(
                "Enter Application Name:",
                placeholder="e.g., Banking Core System, Payment API, Customer Portal",
                key="application_input_desktop",
                help="Enter any application name to get AI analysis"
            )
        
        with col2:
            st.write("") # Spacing
            st.write("") # Spacing
            analyze_btn = st.button("🔍 Analyze Application", type="primary", key="analyze_button_desktop")
    
    # Sample applications
    st.markdown("**💡 Try these sample applications:**")
    
    sample_apps = [
        "Legacy Banking Core System", "E-commerce Payment API", 
        "Customer Portal Web Application", "Trading Platform Middleware",
        "Insurance Claims System", "Healthcare Management Portal"
    ]
    
    # Create sample buttons with proper mobile layout
    if mobile_mode:
        # Single column for mobile
        for i, sample_app in enumerate(sample_apps):
            if st.button(f"📱 {sample_app}", key=f"mobile_sample_{i}"):
                app_name = sample_app
                analyze_btn = True
    else:
        # Multiple columns for desktop
        cols = st.columns(2)
        for i, sample_app in enumerate(sample_apps):
            with cols[i % 2]:
                if st.button(f"📋 {sample_app}", key=f"desktop_sample_{i}"):
                    app_name = sample_app
                    analyze_btn = True
    
    # Analysis execution
    if analyze_btn and app_name:
        with st.spinner("🤖 AI analyzing application... This may take a few moments"):
            # Simulate processing time
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            # Generate analysis
            result = simulate_analysis(app_name)
            
            # Store result
            st.session_state.analysis_results.append(result)
        
        st.markdown(f'<div class="success-box">✅ <strong>Analysis Complete:</strong> {app_name}</div>', unsafe_allow_html=True)
        
        # Results metrics
        st.subheader("📊 Analysis Results")
        
        metrics_data = [
            ("Complexity Score", f"{result['complexity']}/5", f"({result['app_type'].title()})", "🎯"),
            ("Time Savings", f"{result['time_saved']:.0f} weeks", f"{result['time_savings_pct']:.0f}% reduction", "⏱️"),
            ("Cost Savings", f"${result['cost_savings']:,}", f"vs ${result['traditional_cost']:,}", "💰"),
            ("Team Efficiency", f"{result['ai_team']} developers", f"vs {result['traditional_team']} traditional", "👥")
        ]
        
        if mobile_mode:
            for label, value, delta, icon in metrics_data:
                display_mobile_metric(label, value, delta, icon)
        else:
            display_desktop_metrics(metrics_data)
        
        # Detailed comparison
        st.subheader("📈 Migration Comparison")
        
        if mobile_mode:
            # Single column for mobile
            st.markdown("**📊 Traditional Migration:**")
            st.write(f"• Timeline: {result['traditional_weeks']:.0f} weeks")
            st.write(f"• Team Size: {result['traditional_team']} developers")
            st.write(f"• Total Cost: ${result['traditional_cost']:,}")
            st.write(f"• Risk Level: High")
            
            st.markdown("**🤖 AI-Optimized Migration:**")
            st.write(f"• Timeline: {result['ai_weeks']:.0f} weeks")
            st.write(f"• Team Size: {result['ai_team']} developers") 
            st.write(f"• Total Cost: ${result['ai_cost']:,}")
            st.write(f"• Risk Level: Low")
        else:
            # Two columns for desktop
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Traditional Migration:**")
                st.write(f"• Timeline: {result['traditional_weeks']:.0f} weeks")
                st.write(f"• Team Size: {result['traditional_team']} developers")
                st.write(f"• Total Cost: ${result['traditional_cost']:,}")
                st.write(f"• Risk Level: High")
            
            with col2:
                st.markdown("**🤖 AI-Optimized Migration:**")
                st.write(f"• Timeline: {result['ai_weeks']:.0f} weeks")

# Quick Portfolio Fix - Add this at the end
if page == "📈 Portfolio Dashboard" and len(st.session_state.analysis_results) == 0:
    if st.button("🚀 Generate Demo Portfolio"):
        # Quick demo data
        demo_results = [
            {"app_name": "Banking System", "traditional_weeks": 200, "ai_weeks": 45, "cost_savings": 12000000},
            {"app_name": "Payment API", "traditional_weeks": 25, "ai_weeks": 6, "cost_savings": 150000},
            {"app_name": "Web Portal", "traditional_weeks": 60, "ai_weeks": 14, "cost_savings": 890000}
        ]
        
        for demo in demo_results:
            st.session_state.analysis_results.append({
                'app_name': demo['app_name'],
                'traditional_weeks': demo['traditional_weeks'],
                'ai_weeks': demo['ai_weeks'],
                'cost_savings': demo['cost_savings'],
                'complexity': 3,
                'approach': 'AI-Optimized'
            })
        st.rerun()

elif page == "📈 Portfolio Dashboard":
    st.header("📈 Portfolio Migration Dashboard")
    st.markdown("*Comprehensive analysis of multiple applications for enterprise-scale planning*")
    
    if len(st.session_state.analysis_results) == 0:
        st.info("💡 Analyze some applications first or generate a sample portfolio to see dashboard")
        
        if st.button("🚀 Generate Sample Portfolio Analysis", type="primary", key="generate_portfolio"):
            sample_portfolio = [
                "Legacy Banking Core System", "Payment Processing API", 
                "Customer Portal Web Application", "Trading Platform Middleware",
                "Mobile Banking Service", "Data Analytics Platform"
            ]
            
            with st.spinner("🤖 Analyzing enterprise portfolio..."):
                progress_bar = st.progress(0)
                
                for i, app in enumerate(sample_portfolio):
                    result = simulate_analysis(app)
                    st.session_state.analysis_results.append(result)
                    progress_bar.progress((i + 1) / len(sample_portfolio))
                    time.sleep(0.3)
            
            st.success("✅ Portfolio analysis complete!")
            st.rerun()  # Changed from st.experimental_rerun()
    
    if len(st.session_state.analysis_results) > 0:
        results = st.session_state.analysis_results
        
        # Portfolio summary calculations
        total_apps = len(results)
        total_traditional_weeks = sum(r['traditional_weeks'] for r in results)
        total_ai_weeks = sum(r['ai_weeks'] for r in results)
        total_time_saved = total_traditional_weeks - total_ai_weeks
        total_traditional_cost = sum(r['traditional_cost'] for r in results)
        total_ai_cost = sum(r['ai_cost'] for r in results)
        total_cost_saved = total_traditional_cost - total_ai_cost
        
        avg_complexity = sum(r['complexity'] for r in results) / total_apps
        time_reduction_pct = (total_time_saved / total_traditional_weeks) * 100
        cost_reduction_pct = (total_cost_saved / total_traditional_cost) * 100
        
        # Portfolio metrics
        st.subheader("🏆 Portfolio Summary")
        
        metrics_data = [
            ("Applications Analyzed", f"{total_apps}", "Enterprise Portfolio", "📊"),
            ("Total Time Saved", f"{total_time_saved:.0f} weeks", f"{time_reduction_pct:.1f}% reduction", "⏱️"),
            ("Total Cost Savings", f"${total_cost_saved:,.0f}", f"{cost_reduction_pct:.1f}% reduction", "💰"),
            ("Average Complexity", f"{avg_complexity:.1f}/5", "Portfolio Risk Level", "🎯")
        ]
        
        if mobile_mode:
            for label, value, delta, icon in metrics_data:
                display_mobile_metric(label, value, delta, icon)
        else:
            display_desktop_metrics(metrics_data)
        
        # Detailed results
        st.subheader("📊 Application Portfolio Analysis")
        
        # Create results dataframe
        portfolio_df = pd.DataFrame([{
            'Application': r['app_name'],
            'Type': r['app_type'].title(),
            'Complexity': f"{r['complexity']}/5",
            'Traditional (weeks)': f"{r['traditional_weeks']:.0f}",
            'AI-Optimized (weeks)': f"{r['ai_weeks']:.0f}",
            'Time Savings': f"{r['time_savings_pct']:.0f}%",
            'Cost Savings': f"${r['cost_savings']:,.0f}",
            'Migration Approach': r['approach']
        } for r in results])
        
        if mobile_mode:
            # Mobile-friendly card layout
            for _, row in portfolio_df.iterrows():
                st.markdown(f"""
                <div class="mobile-card">
                    <h4>📱 {row['Application']}</h4>
                    <p><strong>Type:</strong> {row['Type']} | <strong>Complexity:</strong> {row['Complexity']}</p>
                    <p><strong>Traditional:</strong> {row['Traditional (weeks)']} weeks → <strong>AI:</strong> {row['AI-Optimized (weeks)']} weeks</p>
                    <p><strong>Savings:</strong> {row['Time Savings']} time, {row['Cost Savings']} cost</p>
                    <p><strong>Strategy:</strong> {row['Migration Approach']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Desktop table view
            st.dataframe(portfolio_df, use_container_width=True)
        
        # Executive summary
        st.subheader("📋 Executive Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Portfolio Metrics:**")
            st.write(f"• **{total_apps} applications** analyzed using AI")
            st.write(f"• **Traditional approach**: {total_traditional_weeks:.0f} weeks ({total_traditional_weeks/52:.1f} years)")
            st.write(f"• **AI-optimized approach**: {total_ai_weeks:.0f} weeks ({total_ai_weeks/52:.1f} years)")
            st.write(f"• **Time savings**: {total_time_saved:.0f} weeks ({time_reduction_pct:.1f}% reduction)")
        
        with col2:
            st.markdown("**💰 Financial Impact:**")
            st.write(f"• **Traditional cost**: ${total_traditional_cost:,.0f}")
            st.write(f"• **AI-optimized cost**: ${total_ai_cost:,.0f}")
            st.write(f"• **Total savings**: ${total_cost_saved:,.0f}")
            st.write(f"• **ROI**: {(total_cost_saved/50000):.0f}x (assuming $50K AI investment)")
        
        # Business impact
        st.subheader("🎯 Business Impact Statement")
        st.info(f"""
        **Portfolio Transformation Results:**
        
        This AI-powered analysis demonstrates transformational impact for enterprise cloud migration:
        
        • **Speed**: {time_reduction_pct:.0f}% faster delivery enables {(total_traditional_weeks - total_ai_weeks)/52:.1f} years faster time-to-market
        • **Cost**: ${total_cost_saved:,.0f} savings can fund {total_cost_saved/100000:.0f} additional strategic initiatives  
        • **Efficiency**: Reduced team requirements from {sum(r['traditional_team'] for r in results)} to {sum(r['ai_team'] for r in results)} developers
        • **Risk**: AI-guided approach reduces project failure probability from 70% to <10%
        • **Innovation**: Demonstrates enterprise AI readiness and digital transformation capability
        """)
        
        # Clear results option
        if st.button("🔄 Clear Portfolio & Start New Analysis", key="clear_portfolio"):
            st.session_state.analysis_results = []
            st.rerun()

# Add footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**🤖 AI Migration Platform**")
    st.markdown("*Revolutionizing Cloud Migration*")

with col2:
    st.markdown("**👩‍💻 Created by Leena Adapakala**")
    st.markdown("*🚀 AI-Driven Cloud Migration Solutions*")

with col3:
    st.markdown("**🔗 Links**")
    st.markdown("[GitHub](https://github.com/LeenaAdapakala17/ai-migration-platform) | [LinkedIn](https://linkedin.com/in/leena-adapakala)")
