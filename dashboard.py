import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Add src to path
sys.path.insert(0, 'src')

from ai_models.application_analyzer import ApplicationAnalyzer

st.set_page_config(
    page_title="AI Migration Platform", 
    page_icon="🤖", 
    layout="wide"
)

st.title("🤖 AI-Powered Azure Migration Platform")
st.markdown("*Revolutionizing cloud migration with artificial intelligence - Portfolio Demo*")

# Initialize
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = ApplicationAnalyzer()
if 'portfolio_results' not in st.session_state:
    st.session_state.portfolio_results = []

# Sidebar
st.sidebar.header("🚀 Navigation")
page = st.sidebar.selectbox("Select Feature:", [
    "🏠 Overview", 
    "📊 Application Analysis", 
    "📈 Portfolio Dashboard",
    "💰 ROI Calculator"
])

if page == "🏠 Overview":
    st.header("🎯 AI Migration Platform Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("⏱️ Time Reduction", "77%", "vs Traditional Methods")
    with col2:
        st.metric("💰 Cost Savings", "$27.6M", "Portfolio Average")  
    with col3:
        st.metric("🎯 AI Accuracy", "95%", "Prediction Confidence")
    with col4:
        st.metric("⚡ Automation", "90%", "Tasks Automated")
    
    st.subheader("🤖 AI-Powered Migration Advantages")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔍 Intelligent Analysis:**
        - Automated code complexity assessment
        - Smart dependency mapping  
        - Predictive resource sizing
        - Risk identification and mitigation
        
        **⚡ Accelerated Timeline:**
        - 77% faster than traditional methods
        - Automated infrastructure provisioning
        - AI-guided testing and validation
        - Predictive issue resolution
        """)
    
    with col2:
        st.markdown("""
        **💡 Smart Optimization:**
        - Cost-optimized architecture recommendations
        - Intelligent containerization strategies
        - Automated scaling configurations
        - Performance optimization suggestions
        
        **🛡️ Risk Reduction:**
        - AI-powered compatibility checking
        - Automated backup and rollback strategies
        - Continuous monitoring and alerting
        - Predictive maintenance insights
        """)
    
    # Demo comparison chart
    st.subheader("📊 Traditional vs AI-Optimized Comparison")
    
    comparison_data = {
        'Metric': ['Timeline (months)', 'Cost ($M)', 'Team Size', 'Success Rate %', 'Automation %'],
        'Traditional': [24, 35.5, 45, 70, 20],
        'AI-Optimized': [6, 7.9, 18, 95, 90]
    }
    
    df = pd.DataFrame(comparison_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Traditional', x=df['Metric'], y=df['Traditional'], marker_color='lightcoral'))
    fig.add_trace(go.Bar(name='AI-Optimized', x=df['Metric'], y=df['AI-Optimized'], marker_color='lightgreen'))
    
    fig.update_layout(title="Migration Approach Comparison", barmode='group')
    st.plotly_chart(fig, use_container_width=True)

elif page == "📊 Application Analysis":
    st.header("📊 AI Application Analysis")
    st.markdown("Enter an application name to get AI-powered migration analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        app_name = st.text_input(
            "Application Name:",
            placeholder="e.g., Banking Core System, E-commerce API, Customer Portal"
        )
    
    with col2:
        analyze_btn = st.button("🔍 Analyze", type="primary")
    
    # Sample applications
    st.markdown("**Quick Start - Try these samples:**")
    sample_apps = [
        "Legacy Banking Core System",
        "E-commerce Payment API", 
        "Customer Portal Web App",
        "Trading Platform Middleware",
        "Insurance Claims System",
        "Healthcare Management Portal"
    ]
    
    selected_sample = st.selectbox("Select sample application:", [""] + sample_apps)
    
    if selected_sample:
        app_name = selected_sample
    
    if (analyze_btn or selected_sample) and app_name:
        with st.spinner(f"🤖 AI analyzing {app_name}..."):
            result = st.session_state.analyzer.analyze_application(app_name)
            
            st.success(f"✅ Analysis complete for {app_name}")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Complexity", f"{result['complexity_score']}/5", help="AI-calculated complexity")
            with col2:
                st.metric("Time Savings", f"{result['time_savings_weeks']:.1f} weeks", 
                         f"{result['time_savings_percentage']:.1f}% reduction")
            with col3:
                st.metric("Cost Savings", f"${result['cost_savings']:,}", 
                         f"{result['cost_savings_percentage']:.1f}% reduction")
            with col4:
                st.metric("Team Size", f"{result['ai_team_size']} developers", 
                         f"-{result['traditional_team_size'] - result['ai_team_size']} vs traditional")
            
            # Detailed comparison
            st.subheader("📈 Detailed Migration Comparison")
            
            comparison_df = pd.DataFrame({
                'Approach': ['Traditional', 'AI-Optimized', 'Improvement'],
                'Timeline (weeks)': [
                    result['traditional_effort_weeks'],
                    result['ai_effort_weeks'], 
                    f"-{result['time_savings_weeks']:.1f}"
                ],
                'Total Cost': [
                    f"${result['traditional_cost']:,}",
                    f"${result['ai_cost']:,}",
                    f"-${result['cost_savings']:,}"
                ],
                'Team Size': [
                    result['traditional_team_size'],
                    result['ai_team_size'],
                    f"-{result['traditional_team_size'] - result['ai_team_size']}"
                ]
            })
            
            st.table(comparison_df)
            
            # Migration details
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎯 Migration Strategy")
                st.info(f"**{result['migration_approach']}**")
                
                st.subheader("🤖 AI Benefits")
                for benefit in result['ai_benefits']:
                    st.write(f"✅ {benefit}")
            
            with col2:
                st.subheader("📋 Action Plan")
                for rec in result['recommendations']:
                    st.write(f"• {rec}")
            
            # Visual comparison
            st.subheader("📊 Visual Comparison")
            
            fig = go.Figure()
            categories = ['Timeline', 'Cost (÷1000)', 'Team Size']
            traditional_vals = [result['traditional_effort_weeks'], result['traditional_cost']/1000, result['traditional_team_size']]
            ai_vals = [result['ai_effort_weeks'], result['ai_cost']/1000, result['ai_team_size']]
            
            fig.add_trace(go.Bar(name='Traditional', x=categories, y=traditional_vals, marker_color='lightcoral'))
            fig.add_trace(go.Bar(name='AI-Optimized', x=categories, y=ai_vals, marker_color='lightgreen'))
            
            fig.update_layout(title=f"Migration Analysis: {app_name}", barmode='group')
            st.plotly_chart(fig, use_container_width=True)

elif page == "📈 Portfolio Dashboard":
    st.header("📈 Portfolio Migration Dashboard")
    
    if st.button("🚀 Generate Portfolio Analysis", type="primary"):
        portfolio_apps = [
            "Legacy Banking Core System",
            "Payment Processing API",
            "Customer Portal Web Application", 
            "Trading Platform Middleware",
            "Mobile Banking Service",
            "Credit Card Processing System",
            "Insurance Claims Portal",
            "Investment Management Platform"
        ]
        
        st.session_state.portfolio_results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, app in enumerate(portfolio_apps):
            status_text.text(f"Analyzing {app}...")
            result = st.session_state.analyzer.analyze_application(app)
            st.session_state.portfolio_results.append(result)
            progress_bar.progress((i + 1) / len(portfolio_apps))
        
        status_text.text("✅ Portfolio analysis complete!")
        
    if st.session_state.portfolio_results:
        results = st.session_state.portfolio_results
        
        # Portfolio summary metrics
        total_traditional_cost = sum(r['traditional_cost'] for r in results)
        total_ai_cost = sum(r['ai_cost'] for r in results)
        total_savings = total_traditional_cost - total_ai_cost
        
        total_traditional_weeks = sum(r['traditional_effort_weeks'] for r in results)
        total_ai_weeks = sum(r['ai_effort_weeks'] for r in results)
        total_time_saved = total_traditional_weeks - total_ai_weeks
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Applications", len(results))
        with col2:
            st.metric("Total Cost Savings", f"${total_savings:,}")
        with col3:
            st.metric("Total Time Saved", f"{total_time_saved:.1f} weeks")
        with col4:
            st.metric("Average Complexity", f"{sum(r['complexity_score'] for r in results)/len(results):.1f}/5")
        
        # Portfolio visualization
        df = pd.DataFrame(results)
        
        fig = px.scatter(df, 
                        x='traditional_effort_weeks', 
                        y='cost_savings',
                        size='complexity_score',
                        color='app_type',
                        hover_name='application_name',
                        title="Portfolio Analysis: Traditional Effort vs Cost Savings",
                        labels={'traditional_effort_weeks': 'Traditional Effort (weeks)',
                               'cost_savings': 'Cost Savings ($)'})
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Portfolio details table
        st.subheader("📋 Portfolio Details")
        
        portfolio_df = pd.DataFrame([{
            'Application': r['application_name'],
            'Type': r['app_type'].title(),
            'Complexity': f"{r['complexity_score']}/5",
            'Traditional (weeks)': f"{r['traditional_effort_weeks']:.1f}",
            'AI-Optimized (weeks)': f"{r['ai_effort_weeks']:.1f}",
            'Time Savings': f"{r['time_savings_percentage']:.1f}%",
            'Cost Savings': f"${r['cost_savings']:,}",
            'Approach': r['migration_approach']
        } for r in results])
        
        st.dataframe(portfolio_df, use_container_width=True)

elif page == "💰 ROI Calculator":
    st.header("💰 Migration ROI Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Project Parameters")
        num_apps = st.slider("Number of Applications:", 1, 20, 8)
        avg_complexity = st.select_slider("Average Complexity:", [1, 2, 3, 4, 5], 3)
        current_budget = st.number_input("Traditional Budget Estimate ($):", 100000, 50000000, 5000000, step=100000)
        timeline_months = st.slider("Traditional Timeline (months):", 6, 60, 24)
        
        calculate_btn = st.button("💡 Calculate ROI", type="primary")
    
    with col2:
        if calculate_btn:
            # AI optimization factors
            complexity_factor = 0.6 + (avg_complexity * 0.05)  # Higher complexity = more AI benefit
            scale_factor = 0.7 + (num_apps * 0.02)  # More apps = better economies of scale
            
            ai_cost_reduction = min(0.85, complexity_factor * scale_factor)
            ai_time_reduction = min(0.80, complexity_factor * 0.9)
            
            ai_cost = current_budget * (1 - ai_cost_reduction) + 50000  # AI tools cost
            cost_savings = current_budget - ai_cost
            time_savings = timeline_months * ai_time_reduction
            
            roi = cost_savings / 50000 if cost_savings > 0 else 0
            
            st.subheader("📊 ROI Analysis")
            
            st.metric("Total Cost Savings", f"${cost_savings:,}", f"{ai_cost_reduction*100:.1f}% reduction")
            st.metric("Time Savings", f"{time_savings:.1f} months", f"{ai_time_reduction*100:.1f}% faster")
            st.metric("ROI", f"{roi:.1f}x", "Return on AI Investment")
            st.metric("Payback Period", f"{(50000/cost_savings*12):.1f} months" if cost_savings > 0 else "N/A")
            
            # ROI breakdown chart
            fig = go.Figure(data=[
                go.Bar(name='Traditional Cost', x=['Development', 'Infrastructure', 'Testing', 'Management'], 
                      y=[current_budget*0.5, current_budget*0.2, current_budget*0.2, current_budget*0.1],
                      marker_color='lightcoral'),
                go.Bar(name='AI-Optimized Cost', x=['Development', 'Infrastructure', 'Testing', 'Management'], 
                      y=[ai_cost*0.4, ai_cost*0.3, ai_cost*0.2, ai_cost*0.1],
                      marker_color='lightgreen')
            ])
            
            fig.update_layout(title="Cost Breakdown Comparison", barmode='group') 
