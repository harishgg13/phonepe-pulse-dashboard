import streamlit as st
from HTML_CSS import page1_footer,page1_home,page1_title,page2_content

#----------------------------------------------------------------------------------------------------------------------

# Inject custom CSS to hide Streamlit's default header
# --- Initialize session state for active page ---
if "page" not in st.session_state:
    st.session_state.page = "Home"
page1_home()

#----------------------------------------------------------------------------------------------------------------------

def content(text,side_text):
    st.markdown(
        f"""
        <style>
            .dashboard-content {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: {side_text};
                font-size: 14px;
                color: #000000;
                font-weight: normal;
                line-height: 1.6;
                margin-bottom: 30px;
            }}
        </style>
        <div class="dashboard-content">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )
    
#----------------------------------------------------------------------------------------------------------------------

tit="About the Dashboard"
page1_title(tit,side="left")
side="left"
content_text="Welcome to the PhonePe Pulse Data Visualization Dashboard.This dashboard has been designed to provide interactive insights into digital payment trends in India using the PhonePe Pulse dataset. The data is aggregated and anonymized to reflect user engagement and transaction behavior across different states and districts."
page2_content(content_text,side,color="#000000")

tit="Data Source"
page1_title(tit,side="left")
side="left"
content_text="The dataset is sourced from the PhonePe Pulse GitHub repository, which publishes open data on digital transactions and user activity."
page2_content(content_text,side,color="#000000")

tit="Key Features"
page1_title(tit,side="left")
side="left"
content_text=f"📊 Track top and least performing states based on registered users and transactions <br> 📱 Analyze device brand usage and its influence on user registrations <br> 🌍 Explore district-level user distribution across India <br> 🔄 Compare app opens, transactions, and growth trends <br> 📈 Gain insights into user engagement patterns over the years and quarters"
page2_content(content_text,side,color="#000000")

tit="Technology Stack"
page1_title(tit,side="left")
side="left"
content_text=f"This project is built using: <br> • Python (Core programming for data processing & analysis) <br> • MySQL (Data storage & querying) <br> • Pandas (Data transformation, and manipulation) <br> • Plotly (Interactive visualizations) <br> • Streamlit (Dashboard deployment) "
page2_content(content_text,side,color="#000000")

page1_footer()