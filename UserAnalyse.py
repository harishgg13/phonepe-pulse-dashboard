import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
import json
import requests
from sklearn.preprocessing import MinMaxScaler
from HTML_CSS import page2,page2_content,page2_footer,page2_tab_color,page2_analyse_title


connection=pymysql.connect(
host="localhost",
user="root",
password="12345678",
database="PhonePe")
cursor=connection.cursor()

#--------------------------------------------------------------------------------------------------------------------------
page2()

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

# main page code starts here. if you copy to main file, select the code after this.
def Analyse_chart(table_name,column_name,choice,var,choose,where_cla):
        if where_cla == "":
            where_clause=""
        else:
            where_clause=f"where {where_cla}"

        if choose!="Registered_User":
            if column_name =="pincode":
                query=f"""SELECT {column_name},state, round(SUM(appopens),2) as appopens, 
                round(SUM(registered_user),2) as registered_user,
                round(SUM(appopens)/SUM(registered_user),2) as {choose} FROM {table_name} 
            {where_clause}
            GROUP BY {column_name},state
            ORDER BY round(SUM(appopens)/SUM(registered_user),2) desc;"""
                
            else:
                query=f"""SELECT {column_name}, round(SUM(appopens),2) as appopens, 
                round(SUM(registered_user),2) as registered_user,
                round(SUM(appopens)/SUM(registered_user),2) as {choose} FROM {table_name} 
                {where_clause}
                GROUP BY {column_name}
                ORDER BY round(SUM(appopens)/SUM(registered_user),2) desc;"""
            
        if choose=="Registered_User":
            if column_name =="pincode":
                query=f"""SELECT state,{column_name}, round(SUM({choose}),2) as {choose} FROM {table_name} 
            {where_clause}
            GROUP BY {column_name},state
            ORDER BY SUM({choose}) desc;"""
                
            else:
                query=f"""SELECT {column_name}, round(SUM({choose}),2) as {choose} FROM {table_name} 
                {where_clause}
                GROUP BY {column_name}
                ORDER BY SUM({choose}) desc;"""

        df_convert=pd.read_sql(query,connection)

        if column_name.lower() == "pincode":
            df_convert["pincode"]=df_convert['state'].str.capitalize()+" "+df_convert["pincode"].map("{:.0f}".format)

        elif df_convert[f"{column_name}"].dtype == object:
            df_convert[f"{column_name}"] = df_convert[f"{column_name}"].str.capitalize()

        if var=="a":
            df_top_graph=df_convert.head(10).sort_values(f"{choose}",ascending=True)
            df_top_df=df_convert.head(10).sort_values(f"{choose}",ascending=False)

        elif var=="b":
            df_top_graph=df_convert.tail(10).sort_values(f"{choose}",ascending=False)
            df_top_df=df_convert.tail(10).sort_values(f"{choose}",ascending=True)

        fig = px.bar(df_top_graph, x=f"{choose}", y=f"{column_name}", color=f"{choose}",title=f"{choice}",
                    labels={f"{column_name}":f"{str(column_name).capitalize()}"},
                    text_auto=True,
             color_continuous_scale=['#d0e6f5','#a5d8f3','#74c7ec','#4bb7d8','#38b2ac','#7bc96f','#c2e59c','#f9d976','#f6a365','#f7797d'])
        
        fig.update_layout(
            title_font_family="Gravitas One",
            title_font_lineposition='under',
            title_font_size=30,
            title_pad_l=175,
            legend_title_font_size=20,
            margin_l=150, # y axis margin. the text state comes away from corner
            plot_bgcolor='rgba(0,0,0,0)', # bar graph box
            paper_bgcolor='rgba(0,0,0,0.75)', #whole box
            font=dict(color='white')
        )

        page2_tab_color()
        df_top_df=df_top_df.reset_index(drop=True)
        df_top_df.index += 1

        tab1,tab2=st.tabs(["Chart","Tabular Data"])
        pd.set_option('display.float_format', '{:.2f}'.format)
        with tab1:
            st.plotly_chart(fig)
        tab2.write(df_top_df)

# --------------------------------------------------------------------------------------------------------------------------------------

def update_layout(fig_input):
    return fig_input.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),  # text color
        xaxis=dict(
            color="white",   # x-axis labels
            showgrid=False   # remove x grid if needed
        ),
        yaxis=dict(
            color="white",   # y-axis labels (500, 1000, etc.)
            gridcolor="gray" # make grid gray/white for visibility
        )
    )

# --------------------------------------------------------------------------------------------------------------------------------------

def count_vs_appopens():
    query_6="""with ao as 
(select year,sum(appopens) as App_Opens from Aggr_user group by year),
cnt as (select year,sum(count) as Transaction_Count from Aggr_transaction group by year)
select ao.year,ao.App_Opens,cnt.Transaction_Count from ao join cnt on ao.year=cnt.year where ao.year > 2018 order by year;"""
    q_6=pd.read_sql(query_6,connection)
    fig=px.line(q_6,x="year",y=["App_Opens","Transaction_Count"],markers=True)
    st.plotly_chart(fig)

# --------------------------------------------------------------------------------------------------------------------------------------

def device_trend_state(state):
    if state!="ALL OVER INDIA":
        query_6=f"""SELECT 
        a.state,
        a.device,
        a.year,
        SUM(a.count) AS total_count
    FROM Aggr_user_device a
    JOIN (
        SELECT device
        FROM Aggr_user_device
        WHERE state = '{state}'
        GROUP BY device
        ORDER BY SUM(count) DESC limit 15
    ) b ON a.device = b.device
    WHERE a.state = '{state}'
    GROUP BY a.device, a.year
    ORDER BY a.year,a.device;"""

    else:
        query_6="""SELECT 
        a.device,
        a.year,
        SUM(a.count) AS total_count,
        SUM(a.percentage) AS total_percentage
        FROM Aggr_user_device a
        JOIN (
        SELECT device
        FROM Aggr_user_device
        GROUP BY device
        ORDER BY SUM(count) DESC
        LIMIT 10
        ) b ON a.device = b.device
        GROUP BY a.device, a.year
        ORDER BY a.device, a.year;"""

    colors=["#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
            "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
            "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000"]
    q_6=pd.read_sql(query_6,connection)
    df=q_6.copy()
    Dataframe_ = df.groupby("device")["total_count"].sum().reset_index()

    fig=px.line(q_6,x="year",y="total_count",
                color="device",
                color_discrete_sequence=colors,
                markers=True)
    
    page2_tab_color()
    tab1,tab2=st.tabs(["Chart","Tabular Data"])
    pd.set_option('display.float_format', '{:.2f}'.format)
    with tab1:
        st.plotly_chart(fig)
    tab2.write(Dataframe_)
    
# --------------------------------------------------------------------------------------------------------------------------------------
def district_analyse_chart(State_name):
    query_q_4=f"""with q23_4 as
(select state,year,district_name,registeredUsers as RU_23,appOpens as AO_23 from map_user where year=2023 and quarter =4
and state="{State_name}"
order by state,year),
avg_24 as(
select state,year,district_name,round(avg(registeredUsers),2) as RU_24 ,round(avg(appOpens),2) as AO_24 from map_user where year=2024
and state="{State_name}"
group by district_name,state,year order by state,year)
select q23_4.district_name,q23_4.RU_23 as RU_Y23_Q4,avg_24.RU_24 as RU_AVG_2024,
round((100*((avg_24.RU_24-q23_4.RU_23)/q23_4.RU_23)),2) as Registered_User_Dynamics,
q23_4.AO_23 as AO_Y23_Q4,avg_24.AO_24 as AO_AVG_2024,
round((100*((avg_24.AO_24-q23_4.AO_23)/q23_4.AO_23)),2) as App_Opens_Dynamics
from q23_4 join avg_24 on q23_4.district_name=avg_24.district_name;"""
    
    df_convert=pd.read_sql(query_q_4,connection)
    fig3 = px.bar(df_convert, 
                 x="district_name", 
                 y=["Registered_User_Dynamics","App_Opens_Dynamics"],
                 barmode='group',
                 width=10,
                 text_auto=True)
    
    fig3.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=True),
        type="category"
    ),
    height=600
)
    update_layout(fig3)
    page2_tab_color()
    tab1,tab2=st.tabs(["Chart","Tabular Data"])
    with tab1:
        st.plotly_chart(fig3)
    tab2.write(df_convert)

        
# --------------------------------------------------------------------------------------------------------------------------------------

with st.sidebar:
    add_radio1 = st.radio(label="User Analysing",
                          options=("Top/Least User Performance", 
                                   "Device Usage State-wise",
                                   "Recent User-Engagement Analyse District-Wise",
                                   "AppOpens vs Transaction Count"
                                   )
    )

if add_radio1=="Top/Least User Performance":
    call_home=page2_analyse_title("Top/Least performing")
    col1,col2=st.columns([1,1])

    with col1:
        first_choice=st.selectbox("",["Registered Users","Avg App-Opens per Registered-User"])
    with col2:
        a_option = ["Top performing 10 States","Top performing 10 Districts", "Top performing 10 Pincodes", 
                    "Least performing 10 States", "Least performing 10 Districts", "Least performing 10 Pincodes"]
        b_option=["Top performing 10 States",
                    "Least performing 10 States"]
        a_dict={"Registered Users":a_option,"App Opens":a_option,"Avg App-Opens per Registered-User":b_option}
        a_choice = st.selectbox("", a_dict[first_choice], index=0)

    col4,col5=st.columns([1,1])
    quarter_list=[1,2,3,4]
    year_list=["OverAll Year",2018, 2019, 2020, 2021, 2022, 2023, 2024]

    with col4:
        c_choice=st.select_slider(
        "Choose a year",
        options=["ALL", 2018, 2019, 2021, 2022, 2023, 2024],
        value="ALL")

    with col5:
        d_choice = st.select_slider(
        "Choose a Quarter",
        options=["ALL", 1, 2, 3, 4],
        value="ALL")

    where_parts = []
    if c_choice != "ALL":
        where_parts.append(f"year = {c_choice}")
    if d_choice != "ALL":
        quarter_num = d_choice
        where_parts.append(f"quarter = {quarter_num}")
    where_ = " AND ".join(where_parts) if where_parts else ""


    if first_choice == "Registered Users":
        Choose="Registered_User"
        if a_choice == "Top performing 10 States" or a_choice=="Least performing 10 States":
            tab_name="aggr_user"
            column="state"
            a="a" if a_choice =="Top performing 10 States" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_)
        elif a_choice == "Top performing 10 Districts" or a_choice=="Least performing 10 Districts":
            tab_name="top_user_districts"
            column="district"
            a="a" if a_choice =="Top performing 10 Districts" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_)
        elif a_choice == "Top performing 10 Pincodes" or a_choice=="Least performing 10 Pincodes":
            tab_name="top_user_pincode"
            column="pincode"
            a="a" if a_choice =="Top performing 10 Pincodes" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_)

    if first_choice == "Avg App-Opens per Registered-User":
        Choose="Avg"
        if a_choice == "Top performing 10 States" or a_choice=="Least performing 10 States":
            tab_name="aggr_user"
            column="state"
            a="a" if a_choice =="Top performing 10 States" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_)
        elif a_choice == "Top performing 10 Districts" or a_choice=="Least performing 10 Districts":
            tab_name="top_user_districts"
            column="district"
            a="a" if a_choice =="Top performing 10 Districts" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_)
        elif a_choice == "Top performing 10 Pincodes" or a_choice=="Least performing 10 Pincodes":
            tab_name="top_user_pincodes"
            column="pincode"
            a="a" if a_choice =="Top performing 10 Pincodes" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_)

#----------------------------------------------------------------------------------------------------------------------

state_value_cap_AOI=state_value_cap.copy()
state_value_cap_AOI.insert(0,"ALL OVER INDIA")

if add_radio1=="Device Usage State-wise":
    call_home=page2_analyse_title("State-wise Device Usage in Phonepe")
    state=st.selectbox("",state_value_cap_AOI)
    calling_appopens_vs_count=device_trend_state(state)
    
#----------------------------------------------------------------------------------------------------------------------

if add_radio1=="AppOpens vs Transaction Count":
    call_home=page2_analyse_title("App Opens vs Transaction Count trends")
    calling_appopens_vs_count=count_vs_appopens()

#----------------------------------------------------------------------------------------------------------------------
if add_radio1=="Recent User-Engagement Analyse District-Wise":
    call_home=page2_analyse_title("Recent Trend in User Engagement")
    Content_text="In the recent trend analysis, we calculate the average value for 2024 and compare it with the 4th quarter of 2023 by taking the difference."
    page2_content(Content_text,side_text="left",color="#ffffff")
    a_choice=st.selectbox("",state_value_cap)
    calling_district_analyse=district_analyse_chart(a_choice)

page2_footer()