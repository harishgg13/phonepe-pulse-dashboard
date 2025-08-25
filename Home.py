import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
import json
import requests
from HTML_CSS import page1_home,page1_title,page1_footer,move_text

connection=pymysql.connect(
host="localhost",
user="root",
password="12345678",
database="PhonePe")
cursor=connection.cursor()

#--------------------------------------------------------------------------------------------------------------------------
#designing with html and css

# Inject custom CSS to hide Streamlit's default header
# --- Initialize session state for active page ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

page1_home()

# --------------------------------------------------------------------------------------------------------------------------------------

#state mapping
get_state="""select distinct(state) from aggr_transaction order by state asc;"""
df_case_1 = pd.read_sql(get_state, connection)
state_value=df_case_1.values
url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response = requests.get(url)
data_map=json.loads(response.text)
geo_list=[]
for j in data_map["features"]:
    geo_list.append(j["properties"]["ST_NM"])

state_mapping={}
geo_list_sorted=geo_list.sort()
for i in range(len(state_value)):
    state_str=state_value[i][0]
    state_mapping[state_str]=geo_list[i]
    
state_value_cap = []
for i in state_value:
    state_value_cap.append(i[0].capitalize())

# --------------------------------------------------------------------------------------------------------------------------------------

#case 1

query_case_1= """with ac as (SELECT 
  state,transaction_type,year,round(avg(count),2) as Avg_count
FROM 
  aggr_transaction where year=2024 group by state,transaction_type,year),
  cd as (select state,transaction_type,count from aggr_transaction where year = 2024 and quarter = 1)
  SELECT 
  ac.state,
  ac.transaction_type,
  ROUND(100*((ac.avg_count - cd.count)/cd.count), 2) AS diff_percentage
FROM 
  ac 
JOIN 
  cd ON ac.state = cd.state AND ac.transaction_type = cd.transaction_type 
  where ROUND(100 * ((ac.avg_count - cd.count) / cd.count), 2) < -10;"""

df_case_1 = pd.read_sql(query_case_1, connection)
# df_case_1['total_amount'] = df_case_1['total_amount'].map('{:.2f}'.format)
# df_case_1['total_count'] = df_case_1['total_count'].map('{:.0f}'.format)


# --------------------------------------------------------------------------------------------------------------------------------------

#Aggr Transacation Map

def map_change_transaction(tab_name, where_clause):
    if where_clause == "":
        Transaction_get = f"""
            SELECT State, SUM(amount) as Amount,
            sum(count) as Count
            FROM {tab_name}
            GROUP BY State;
        """

        top_10_district_query=f"""select district,sum(count) as Count ,sum(amount) as Amount 
        from top_transaction_districts 
        group by district 
        order by sum(amount) desc;"""

        top_type=f"""SELECT transaction_type, SUM(Amount) as Amount,sum(count) as Count 
        FROM {tab_name} 
        GROUP BY transaction_type 
        order by amount desc;"""

        top_pincode="""select pincode,state,sum(count) as Count ,sum(amount) as Amount 
        from top_transaction_pincodes 
        group by pincode,state 
        order by sum(count) desc;"""


    else:
        Transaction_get = f"""
            SELECT State, SUM(Amount) as Amount,
            sum(count) as Count
            FROM {tab_name} 
            WHERE {where_clause} 
            GROUP BY State;
        """

        top_10_district_query=f"""select district,sum(count) as Count ,sum(amount) as Amount 
        from top_transaction_districts 
        where {where_clause}
        group by district 
        order by sum(amount) desc limit 10;"""

        top_type=f"""SELECT transaction_type, SUM(Amount) as Amount,sum(count) as Count 
        FROM {tab_name} 
        where {where_clause}
        GROUP BY transaction_type 
        order by amount desc;"""

        top_pincode=f"""select pincode,state,sum(count) as Count ,sum(amount) as Amount 
        from top_transaction_pincodes 
        where {where_clause}
        group by pincode,state 
        order by sum(count) desc;"""

    df = pd.read_sql(Transaction_get, connection)
    top_10_district=pd.read_sql(top_10_district_query,connection)
    top_transaction_type=pd.read_sql(top_type,connection)
    top_10_pincode=pd.read_sql(top_pincode,connection)

    # Load GeoJSON locally instead of relying on Plotly fetching
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    geojson_data = json.loads(requests.get(url).text)

    # Make sure state names match exactly
    df["State"]=df["State"].replace(state_mapping)

    fig = px.choropleth(
        df,
        geojson=geojson_data,
        featureidkey='properties.ST_NM',
        locations='State',
        color="Amount",
        color_continuous_scale='purples',
        hover_name="State",
        hover_data={
            "State":False,
            "Amount": True,
            "Count": True}
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type='mercator',
        projection_scale=1.2,
        center={"lat": 22.5, "lon": 78.5}
    )

    fig.update_layout(
        width=1600,
        height=650,
        margin=dict(l=100, r=0, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        dragmode=False,
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        coloraxis_showscale=False
    )

    # Show the chart
    st.plotly_chart(fig, use_container_width=True)

    # Floating box
    top_transaction_type=top_transaction_type.sort_values(by="Amount",ascending=False,ignore_index=True).head(5)
    top_10_district=top_10_district.sort_values(by="Amount",ascending=False,ignore_index=True).head(5)
    top10 = df.sort_values(by="Amount", ascending=False,ignore_index=True).head(5)
    top_10_pincode=top_10_pincode.sort_values(by="Amount", ascending=False,ignore_index=True).head(5)

#     content_text = f"""
# <span style="color:#673AB7;">Total Transaction Value :</span> 
# <span style="color:#FFC107;">{df['Amount'].sum()}</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp
# <span style="color:#673AB7;">Total Count Of Transaction :</span> 
# <span style="color:#FFC107;">{int(df['Count'].sum())}</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp
# <span style="color:#673AB7;">Average Amount Per Transation :</span> 
# <span style="color:#FFC107;">{round(df['Amount'].sum()/int(df['Count'].sum()),2)}</span>
# """
#     move_text(content_text)
    return top10,top_10_district,top_transaction_type,top_10_pincode

#--------------------------------------------------------------------------------------------------------------

#Aggr insurance Map

def map_change_insurance(tab_name,where_clause):
    if where_clause == "":
        Insurance_get=f"""SELECT State, SUM(Amount) as Amount,sum(count) as Count FROM {tab_name} {where_clause} GROUP BY State;"""

        top_10_district_query=f"""select district,sum(count) as Count ,sum(amount) as Amount 
        from top_insurance_districts 
        group by district 
        order by sum(amount) desc;"""

        top_pincode="""select pincode,state,sum(count) as Count ,sum(amount) as Amount 
        from top_insurance_pincodes 
        group by pincode,state 
        order by sum(count) desc;"""

    else:
        Insurance_get=f"""SELECT State, SUM(Amount) as Amount,sum(count) as Count FROM {tab_name} where {where_clause} GROUP BY State;"""

        top_10_district_query=f"""select district,sum(count) as Count ,sum(amount) as Amount 
        from top_insurance_districts 
        where {where_clause}
        group by district 
        order by sum(amount) desc;"""

        top_pincode=f"""select pincode,state,sum(count) as Count ,sum(amount) as Amount 
        from top_insurance_pincodes 
        where {where_clause}
        group by pincode,state 
        order by sum(count) desc;"""


    df = pd.read_sql(Insurance_get, connection)
    top_10_district=pd.read_sql(top_10_district_query,connection)
    top_10_pincode=pd.read_sql(top_pincode,connection)

    # mapping
    df["State"]=df["State"].replace(state_mapping)
    Fig_insurance = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color="Amount",
        color_continuous_scale='Oranges',
        hover_name="State",
        hover_data={
            "State":False,
            "Amount": True,
            "Count": True}
    )
    Fig_insurance.update_geos(
        fitbounds="locations", 
        visible=False,
        projection_type='mercator',
        projection_scale=1.2,  # Moderate zoom
        center={"lat": 22.5, "lon": 78.5}  # Keep centered on India
    )

    Fig_insurance.update_layout(
        width=1600,
        height=650,
        margin=dict(l=100, r=0, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        dragmode=False,
        geo=dict(
        bgcolor='rgba(0,0,0,0)'
        ),
        coloraxis_showscale=False
    )
    st.plotly_chart(Fig_insurance, use_container_width=True)

    top10 = df.sort_values(by="Amount", ascending=False,ignore_index=True).head(10)
    top_district=top_10_district.sort_values(by="Amount", ascending=False,ignore_index=True).head(5)
    top_10_pin=top_10_pincode.sort_values(by="Amount", ascending=False,ignore_index=True).head(5)

    return top10,top_district,top_10_pin
#--------------------------------------------------------------------------------------------------------------
def box(position,heading,row1,row2,df):
    st.markdown(
        f"""
        <div style="position:absolute; 
        {position}
        background-color:transparent;
        padding:15px; 
        border-radius:10px; 
        box-shadow:2px 2px 10px rgba(0,0,0,0.2);
        width:200px; 
        font-size:14px; 
        z-index:999;">
        <h4 style="margin-top:0;
        font-size:20px;
        color:black;">{heading}</h4>
        """ +
        "".join([f"<p style = font-size:12px;color:#1A1A1A;><b>{i+1}. {str(row[f'{row1}']).capitalize()}</b> :</br> {row[f'{row2}']:,}</p>" for i, row in df.iterrows()]) + "</div>",
        unsafe_allow_html=True
    )
#--------------------------------------------------------------------------------------------------------------
# Home Page Code

# --- Detect menu click from form GET request ---
if "page" in st.query_params:
    st.session_state.page = st.query_params["page"]

# --- Render selected page ---
if st.session_state.page == "Home":
    call_home=page1_title(title="PhonePe Explorer",side="center")
    print(call_home)
    # Drop-down menu with default as Home

    col5,col1, col2 ,col3,col4= st.columns([0.5,1, 1, 1,0.5])  # You can adjust ratio, e.g. [1, 0.8]

    with col1:
        page = st.selectbox(
            "",
            ["Transaction", "Insurance"],
            index=0
        )

    sub_options_b = {
    "Transaction": ["OverAll Year",2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Insurance": ["OverAll Year",2020, 2021, 2022, 2023, 2024],
    }
    with col2:
        b_choice = st.selectbox(
            "",
            sub_options_b[page],index=0
        )

    # --- C: Depends on B ---
    quarter_list=["OverAll Quarter","Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"]
    sub_options_c = {
        "Transaction": {
            2018: quarter_list,
            2019: quarter_list,
            2020: quarter_list,
            2021: quarter_list,
            2022: quarter_list,
            2023: quarter_list,
            2024: quarter_list,
            "OverAll Year": quarter_list
        },
        "Insurance": {
                2020: ["OverAll Quarter", "Quarter 2", "Quarter 3", "Quarter 4"],
                2021: quarter_list,
                2022: quarter_list,
                2023: quarter_list,
                2024: quarter_list,
                "OverAll Year": quarter_list
        }
    }
    with col3:
        c_choice = st.selectbox(
            "",
            sub_options_c[page][b_choice],index=0
        )

    colors = {
    "Transaction": "#f3e8ff",  # purple
    "Insurance": "#F8E0DD"     # orange
    }

    st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {colors[page]};
    }}
    </style>
    """,
    unsafe_allow_html=True
)
    # Display content based on selection
    if page == "Transaction":
        tab = "aggr_transaction"
        where_parts = []
        if b_choice != "OverAll Year":
            where_parts.append(f"year = {b_choice}")
        if c_choice != "OverAll Quarter":
            quarter_num = int(c_choice.split()[-1])  # "1", "2", etc.
            where_parts.append(f"quarter = {quarter_num}")
        where_cla = " AND ".join(where_parts) if where_parts else ""
        call_map = map_change_transaction(tab, where_cla)

        Top_10_states,Top_10_districts,transaction_type_top,pincode_top=call_map

        with col4:
            position_snd="top:28px;" \
            "left:225px;"
            heading_snd="Top 5 States"
            row1_snd="State"
            row2_snd="Amount"
            calling_box1=box(position_snd,heading_snd,row1_snd,row2_snd,Top_10_states)
            
            position_snd="top:375px;" \
            "left:225px;"
            heading_snd="Top Transaction Types"
            row1_snd="transaction_type"
            row2_snd="Amount"
            calling_box4=box(position_snd,heading_snd,row1_snd,row2_snd,transaction_type_top)

            
        with col5:
            position_snd="top:28px;" \
            "right:225px;"
            heading_snd="Top 5 Districts"
            row1_snd="district"
            row2_snd="Amount"
            calling_box3=box(position_snd,heading_snd,row1_snd,row2_snd,Top_10_districts)

            st.markdown(
        f"""
        <div style="position:absolute; 
        top:375px;
        right:225px;
        background-color:transparent;
        padding:15px; 
        border-radius:10px; 
        box-shadow:2px 2px 10px rgba(0,0,0,0.2);
        width:200px; 
        font-size:14px; 
        z-index:999;">
        <h4 style="margin-top:0;
        font-size:20px;
        color:black;">Top 5 Pincodes</h4>
        """ +
        "".join([f"<p style = font-size:12px;color:#1A1A1A;><b>{i+1}.{int(row['pincode'])} ({str(row['state']).capitalize()})</b> :</br> {row['Amount']:,}</p>" for i, row in pincode_top.iterrows()]) + "</div>",
        unsafe_allow_html=True
    )

    elif page == "Insurance":
        tab = "aggr_insurance"
        where_parts = []
        if b_choice != "OverAll Year":
            where_parts.append(f"year = {b_choice}")
        if c_choice != "OverAll Quarter":
            quarter_num = int(c_choice.split()[-1])  # "1", "2", etc.
            where_parts.append(f"quarter = {quarter_num}")
        where_cla = " AND ".join(where_parts) if where_parts else ""
        call_map = map_change_insurance(tab, where_cla)

        top_10_insurance_state,top_10_insurance_district,top_10_insurance_pincode=call_map

        with col4:
            position_snd="top:28px;" \
            "left:225px;"
            heading_snd="Top 10 States"
            row1_snd="State"
            row2_snd="Amount"
            calling_box1=box(position_snd,heading_snd,row1_snd,row2_snd,top_10_insurance_state)

        with col5:
            position_snd="top:28px;" \
            "right:225px;"
            heading_snd="Top 5 District"
            row1_snd="district"
            row2_snd="Amount"
            calling_box1=box(position_snd,heading_snd,row1_snd,row2_snd,top_10_insurance_district)
            
            st.markdown(
        f"""
        <div style="position:absolute; 
        top:375px;
        right:225px;
        background-color:transparent;
        padding:15px; 
        border-radius:10px; 
        box-shadow:2px 2px 10px rgba(0,0,0,0.2);
        width:200px; 
        font-size:14px; 
        z-index:999;">
        <h4 style="margin-top:0;
        font-size:20px;
        color:black;">Top 5 Pincodes</h4>
        """ +
        "".join([f"<p style = font-size:12px;color:#1A1A1A;><b>{i+1}.{int(row['pincode'])} ({str(row['state']).capitalize()})</b> :</br> {row['Amount']:,}</p>" for i, row in top_10_insurance_pincode.iterrows()]) + "</div>",
        unsafe_allow_html=True
    )
    page1_footer()

#above code is for home page


#-----------------------------------------------------------------------------------------------------------------------

if st.session_state.page == "Reports":
    exec(open("AnalysePage.py").read())

if st.session_state.page == "User-Analyse":
    exec(open("UserAnalyse.py").read())

if st.session_state.page == "About":
    exec(open("About.py").read())

