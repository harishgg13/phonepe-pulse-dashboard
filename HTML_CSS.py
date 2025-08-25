import streamlit as st

def page2():
    st.markdown(f"""
        <style>
            /* Hide default Streamlit header and footer */
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}
                
            .custom-header {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: #2A0A5E;
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 10px 20px;
                border-bottom: 1px solid #31333F;
                display: flex;
                align-items: center;
                justify-content: space-between;
                z-index: 1000;
            }}
            .custom-header img {{
                height: 50px;
                vertical-align: middle;
            }}
            .title-group {{
                display: flex;
                align-items: baseline;
                gap: 5px;
            }}
            .beta-text {{
                position: fixed;
                padding: 7px 280px;
                font-size: 15px;
                font-weight: normal;
                color: #9370DB;
                font-style: italic;
            }}
            .menu {{
                display: flex;
                gap: 20px;
            }}
            .menu button {{
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
            }}
            .menu button:hover {{
                text-decoration: underline;
            }}
            /* Push content below fixed header */
            .block-container {{
                padding-top: 25px;
            }}
        </style>

        <div class="custom-header">
            <div style="display:flex;align-items:center;gap:10px;">
                <img src="https://static.vecteezy.com/system/resources/previews/049/116/753/non_2x/phonepe-app-icon-transparent-background-free-png.png" alt="Logo">
                <div class="title-group">
                    PhonePe Pulse Dashboard
                    <span class="beta-text">| Capestone Project One</span>
                </div>
            </div>
            <div class="menu">
                <form action="" method="get">
                    <button name="page" value="Home">Home</button>
                    <button name="page" value="Reports">Reports</button>
                    <button name="page" value="User-Analyse">User-Analyse</button>
                    <button name="page" value="About">About</button>
                </form>
            </div>
        </div>
    """, unsafe_allow_html=True)


    st.markdown("""
        <style>
            html, body {
                background-color: #000000 !important;
            }
            .stApp {
                background-color: #000000;
            }
            .block-container {
                background-color: transparent;
            }
        </style>
    """, True)

    st.markdown("""
    <style>
        /* Move entire sidebar down */
        section[data-testid="stSidebar"] {
            position:fixed;
            background: linear-gradient(#3b0a45,#1e1e2f);
            display: sidebar;
            margin-top: 71.5px;
            margin-bottom: 29.5px;
            border-right: 2px solid #333333;
        }
    </style>
    """, unsafe_allow_html=True)

def analyse_title(title):
    return st.markdown("""
        <style>
            .custom-title {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center; 
                font-size: 30px;
                color: #FFFFFF;
                font-weight: bold;
                margin-bottom: 20px;
            }
        </style>
        <div class="custom-title">"""
                       f"""{title}"""
                       """
                </div>
    """,True)


# --------------------------------------------------------------------------------------------------------------------------------------

def page2_footer():
    
    st.markdown(
        """
        
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                left: 0rem; 
                right:0rem;
                width: calc(100%); /* Adjust width */
                background-color: #0e1117; /* Match dark theme */
                text-align: center;
                font-size: 12px;
                color: #aaaaaa;
                padding: 4px 0;
                border-top: 2px solid #333333;
            }
            .footer a {
                color: #6a5acd; /* Purple links */
                text-decoration: none;
                font-weight: 500;
            }
            .footer a:hover {
                color: #ffffff;
                text-decoration: underline;
            }
            
        </style>
        <div class="footer">
            <b>PhonePe Pulse Dashboard</b> | Developed by <b>G G Harish</b> | E-Mail: 
            <a href="mailto:harishgg03@gmail.com" target="_blank">Harishgg03@gamil.com</a> 
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------------------------------------------------------------------------------------------

def page2_content(text,side_text,color):
    st.markdown(
        f"""
        <style>
            .dashboard-content {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: {side_text};
                font-size: 14px;
                color: {color};
                font-weight: normal;
                line-height: 1.6;
                margin-bottom: 5px;
            }}
        </style>
        <div class="dashboard-content">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------------------------------------------------------------------------------------------

def page2_tab_color():
    st.markdown("""
            <style>
            /* Change the first tab's text color */
            div[data-baseweb="tab-list"] button:nth-child(1) {
                color: #3B82F6 !important;
                font-weight: bold;
                font-size: 22px;
            }

            /* Change the second tab's text color */
            div[data-baseweb="tab-list"] button:nth-child(2) {
                color: #10B981 !important;
                font-weight: bold;
                font-size: 22px;
            }
            </style>
        """, unsafe_allow_html=True)
    

# --------------------------------------------------------------------------------------------------------------------------------------

def page2_analyse_title(title):
    return st.markdown("""
        <style>
            .custom-title {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center; 
                font-size: 30px;
                color: #FFFFFF;
                font-weight: bold;
                margin-bottom: 20px;
            }
        </style>
        <div class="custom-title">"""
                       f"""{title}"""
                       """
                </div>
    """,True)


# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------

def page1_title(title,side):
    return st.markdown(f"""
        <style>
            .custom-title {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: {side};
                font-size: 30px;
                color: #6a1b9a;
                font-weight: bold;
                margin-bottom: 5px;
            }}
        </style>
        <div class="custom-title">
                {title}
                </div>
    """,True)

# --------------------------------------------------------------------------------------------------------------------------------------

def page1_home():

    st.markdown(f"""
        <style>
            /* Hide default Streamlit header and footer */
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}
                
            .custom-header {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: #2A0A5E;
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 5px 20px;
                border-bottom: 1px solid #31333F;
                display: flex;
                align-items: center;
                justify-content: space-between;
                z-index: 1000;
            }}
            .custom-header img {{
                height: 50px;
                vertical-align: middle;
            }}
            .title-group {{
                display: flex;
                align-items: baseline;
                gap: 5px;
            }}
            .beta-text {{
                position: fixed;
                padding: 7px 280px;
                font-size: 15px;
                font-weight: normal;
                color: #9370DB;
                font-style: italic;
            }}
            .menu {{
                display: flex;
                gap: 20px;
            }}
            .menu button {{
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
            }}
            .menu button:hover {{
                text-decoration: underline;
            }}
            /* Push content below fixed header */
            .block-container {{
                padding-top: 75px;
            }}
        </style>

        <div class="custom-header">
            <div style="display:flex;align-items:center;gap:10px;">
                <img src="https://static.vecteezy.com/system/resources/previews/049/116/753/non_2x/phonepe-app-icon-transparent-background-free-png.png" alt="Logo">
                <div class="title-group">
                    PhonePe Pulse Dashboard
                    <span class="beta-text">| Capestone Project One</span>
                </div>
            </div>
            <div class="menu">
                <form action="" method="get">
                    <button name="page" value="Home">Home</button>
                    <button name="page" value="Reports">Reports</button>
                    <button name="page" value="User-Analyse">User-Analyse</button>
                    <button name="page" value="About">About</button>
                </form>
            </div>
        </div>
    """, unsafe_allow_html=True)


    st.markdown("""
        <style>
            html, body {
                background-color: #f3e8ff !important;
            }
            .stApp {
                background-color: #f3e8ff;
            }
            .block-container {
                background-color: transparent;
            }
        </style>
    """, True)

# --------------------------------------------------------------------------------------------------------------------------------------

def page1_footer():
    
    st.markdown(
        """
        
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                left: 0rem; 
                right:0rem;
                width: calc(100%); /* Adjust width */
                background-color: #2A0A5E; /* Match dark theme */
                text-align: center;
                font-size: 12px;
                color: #ffffff;
                padding: 4px 0;
                border-top: 1px solid #333333;
            }
            .footer a {
                color: #aaaaaa; /* links */
                text-decoration: none;
                font-weight: 500;
            }
            .footer a:hover {
                color: #ffffff;
                text-decoration: underline;
            }
            
        </style>
        <div class="footer">
            <b>PhonePe Pulse Dashboard</b> | Developed by <b>G G Harish</b> | E-Mail: 
            <a href="mailto:harishgg03@gmail.com" target="_blank">Harishgg03@gamil.com</a> 
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------------------------------------------------------------------------------------------
def move_text(content):
    moving_text = """
    <div style="position:fixed; top:75px; left:50%; transform:translateX(-50%); width:100%;">
        <marquee behavior="scroll" direction="left" scrollamount="10" style="color:#2A0A5E;
        font-size:20px; font-weight:1000;
        -webkit-text-stroke: 0.1px black;">"""f"""{content}""" 
    """</marquee>
    </div>"""


    st.markdown(moving_text, unsafe_allow_html=True)
    