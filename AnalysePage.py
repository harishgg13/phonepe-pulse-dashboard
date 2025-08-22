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
#designing with html and css
page2()

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
def Analyse_chart(table_name,column_name,choice,var,choose,where):
        if where=="":
            where_clause=""
        else:
            where_clause=f"where {where}"
        if choose!="Average per Transaction":
            if column_name =="pincode":
                query=f"""SELECT {column_name},state, round(SUM({choose}),2) as {choose} FROM {table_name} 
                {where_clause}
            GROUP BY {column_name},state
            ORDER BY SUM({choose}) desc;"""
                
            else:
                query=f"""SELECT {column_name}, round(SUM({choose}),2) as {choose} FROM {table_name} 
                {where_clause}
                GROUP BY {column_name}
                ORDER BY SUM({choose}) desc;"""
            
        if choose=="Average_Per_Transaction":
            if column_name =="pincode":
                query=f"""SELECT {column_name},state, round(SUM(Amount),2) as Amount, round(SUM(Count),2) as Count,
                round(SUM(Amount)/SUM(Count),2) as {choose} FROM {table_name} 
                {where_clause}
            GROUP BY {column_name},state
            ORDER BY round(SUM(Amount)/SUM(Count),2) desc;"""
                
            else:
                query=f"""SELECT {column_name}, round(SUM(Amount),2) as Amount, round(SUM(Count),2) as Count,
                round(SUM(Amount)/SUM(Count),2) as {choose} FROM {table_name} 
                {where_clause}
                GROUP BY {column_name}
                ORDER BY round(SUM(Amount)/SUM(Count),2) desc;"""

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
        
        if choose!="Count":
            df_top_df["Amount"] = df_top_df["Amount"].map("{:.2f}".format)

        fig = px.bar(df_top_graph, x=f"{choose}", y=f"{column_name}", color=f"{choose}",title=f"{choice}",
                    labels={f"{column_name}":f"{str(column_name).capitalize()}"},
                    text_auto=True,
             color_continuous_scale=['#d0e6f5','#a5d8f3','#74c7ec','#4bb7d8','#38b2ac','#7bc96f','#c2e59c','#f9d976','#f6a365','#f7797d'])
        
        fig.update_layout(
            title_font_family="Gravitas One",
            title_font_lineposition='under',
            margin_l=150, # y axis margin. the text state comes away from corner
            plot_bgcolor='rgba(0,0,0,0)', # bar graph box
            paper_bgcolor='rgba(0,0,0,0.75)', #whole box
            font=dict(color='white')
        )
        fig.update_layout(title="")
        
        call_tab_color=page2_tab_color()
        print(call_tab_color)

        df_top_df=df_top_df.reset_index(drop=True)
        df_top_df.index += 1

        tab1, tab2 = st.tabs(["Chart", "Data"])
        pd.set_option('display.float_format', '{:.2f}'.format)
        with tab1:
            st.plotly_chart(fig)
        tab2.write(df_top_df)

# --------------------------------------------------------------------------------------------------------------------------------------


def recent_transaction_count():
    for i in ["<",">"]:
        query_q_3=f"""with ac as (SELECT 
    state,transaction_type,year,round(avg(count),2) as Avg_count
    FROM 
    aggr_transaction where year=2024 group by state,transaction_type,year),
    cd as (select state,transaction_type,count from aggr_transaction where year = 2023 and quarter = 4)
    SELECT 
    ac.state,
    ac.transaction_type,
    ROUND(100*((ac.avg_count-cd.count)/cd.count), 2) AS percentage
    FROM 
    ac 
    JOIN 
    cd ON ac.state = cd.state AND ac.transaction_type = cd.transaction_type 
    where ROUND(100 * ((ac.avg_count-cd.count) / cd.count), 2) {i} 0 order by percentage;"""
        cursor.execute(query_q_3)
        q_3 = pd.read_sql(query_q_3, connection)
        df_q_3=pd.DataFrame(q_3)
        st.write(df_q_3)

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

def district_analyse_chart(State_name,table_name):
    query_q_4=f"""with q23_4 as
(select state,year,district_name,count as count_23,amount as AMT_23 from {table_name} where year=2023 and quarter =4
and state="{State_name}"
order by state,year),
avg_24 as(
select state,year,district_name,round(avg(count),2) as count_24 ,round(avg(amount),2) as AMT_24 from {table_name} where year=2024
and state="{State_name}"
group by district_name,state,year order by state,year)
select q23_4.state,q23_4.district_name,q23_4.count_23,avg_24.count_24,
round((100*((avg_24.count_24-q23_4.count_23)/q23_4.count_23)),2) as Count_percent,
q23_4.AMT_23,avg_24.AMT_24,
round((100*((avg_24.AMT_24-q23_4.AMT_23)/q23_4.AMT_23)),2) as Amount_percent
from q23_4 join avg_24 on q23_4.district_name=avg_24.district_name;"""
    
    df_convert=pd.read_sql(query_q_4,connection)
    fig3 = px.bar(df_convert, 
                 x="district_name", 
                 y=["Count_percent","Amount_percent"],
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
    calling_layout_update=update_layout(fig3)
    print(calling_layout_update)
    st.plotly_chart(fig3)

        
# --------------------------------------------------------------------------------------------------------------------------------------

with st.sidebar:
    add_radio1 = st.radio(label="Transaction and Insurance Analysis",
                          options=("Top/Least performing", 
                                   "Transaction_Type Trends",
                                   "Transaction Trends State_Wise",
                                   "Insurance-Transaction Trends",
                                   "Recent Trends")
    )

if add_radio1=="Top/Least performing":
    call_home=page2_analyse_title("Performance Insights")
    col1,col2,col3=st.columns([1,1,1])
    with col1:
        first_choice=st.selectbox("",["Transaction","Insurance"])
        second_option=["Amount","Count","Average per Transaction"]
        second_dict={"Transaction":second_option,"Insurance":second_option}
    with col2:
        b_choice=st.selectbox("",second_dict[first_choice],index=0)
    with col3:
        a_option = ["Top performing 10 States","Top performing 10 Districts", "Top performing 10 Pincodes", 
                    "Least performing 10 States", "Least performing 10 Districts", "Least performing 10 Pincodes"]
        a_dict={"Amount":a_option,"Count":a_option,"Average per Transaction":a_option}
        a_choice = st.selectbox("", a_dict[b_choice], index=0)

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
    where_cla = " AND ".join(where_parts) if where_parts else ""

    if b_choice == "Amount":
        Choose="Amount"
        if a_choice == "Top performing 10 States" or a_choice=="Least performing 10 States":
            tab_name="aggr_transaction" if first_choice=="Transaction" else "aggr_Insurance"
            column="state"
            a="a" if a_choice =="Top performing 10 States" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_cla)

        elif a_choice == "Top performing 10 Districts" or a_choice=="Least performing 10 Districts":
            tab_name="top_transaction_districts" if first_choice=="Transaction" else "top_insurance_districts"
            column="district"
            a="a" if a_choice =="Top performing 10 Districts" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_cla)

        elif a_choice == "Top performing 10 Pincodes" or a_choice=="Least performing 10 Pincodes":
            tab_name="top_transaction_pincodes" if first_choice=="Transaction" else "top_insurance_pincodes"
            column="pincode"
            a="a" if a_choice =="Top performing 10 Pincodes" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_cla)

    if b_choice == "Count":
        Choose="Count"
        if a_choice == "Top performing 10 States" or a_choice=="Least performing 10 States":
            tab_name="aggr_transaction" if first_choice=="Transaction" else "aggr_Insurance"
            column="state"
            a="a" if a_choice =="Top performing 10 States" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_cla)
        elif a_choice == "Top performing 10 Districts" or a_choice=="Least performing 10 Districts":
            tab_name="top_transaction_districts" if first_choice=="Transaction" else "top_insurance_districts"
            column="district"
            a="a" if a_choice =="Top performing 10 Districts" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_cla)
        elif a_choice == "Top performing 10 Pincodes" or a_choice=="Least performing 10 Pincodes":
            tab_name="top_transaction_pincodes" if first_choice=="Transaction" else "top_insurance_pincodes"
            column="pincode"
            a="a" if a_choice =="Top performing 10 Pincodes" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_cla)

    if b_choice == "Average per Transaction":
        Choose="Average_Per_Transaction"
        if a_choice == "Top performing 10 States" or a_choice=="Least performing 10 States":
            tab_name="aggr_transaction" if first_choice=="Transaction" else "aggr_Insurance"
            column="state"
            a="a" if a_choice =="Top performing 10 States" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_cla)
        elif a_choice == "Top performing 10 Districts" or a_choice=="Least performing 10 Districts":
            tab_name="top_transaction_districts" if first_choice=="Transaction" else "top_insurance_districts"
            column="district"
            a="a" if a_choice =="Top performing 10 Districts" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_cla)
        elif a_choice == "Top performing 10 Pincodes" or a_choice=="Least performing 10 Pincodes":
            tab_name="top_transaction_pincodes" if first_choice=="Transaction" else "top_insurance_pincodes"
            column="pincode"
            a="a" if a_choice =="Top performing 10 Pincodes" else "b"
            call_chart=Analyse_chart(tab_name,column,a_choice,a,Choose,where_cla)


#----------------------------------------------------------------------------------------------------------------------

if add_radio1=="Transaction_Type Trends":
        state_value_cap_AOI=state_value_cap
        state_value_cap_AOI.insert(0,"ALL OVER INDIA")

        cate1s=st.selectbox("",state_value_cap_AOI,index=0)
        col1,col2,col3=st.columns([1,1,1])
        year1=[2018,2019,2020,2021,2022,2023,2024]
        with col1:
            cate=st.selectbox("",["Amount","Count","Average"],index=0)
        with col2:
            Y1_choice=st.selectbox("",year1,index=0,key="A")
        if Y1_choice:
            year2get = year1[year1.index(Y1_choice):]
        with col3:
            Y2_choice=st.selectbox("",year2get,index=0,key="B")

        if cate1s=="ALL OVER INDIA":
            if cate!="Average":
                query_q_7=f"""select Transaction_type,Year,Quarter,sum(amount) as Amount,sum(count) as Count from aggr_transaction 
                            where year>={Y1_choice} and year<={Y2_choice} 
                            group by transaction_type,year,quarter 
                            order by Year,Quarter;"""
            else:
                query_q_7=f"""select Transaction_type,Year,Quarter,sum(amount)/sum(count) as Average from aggr_transaction 
                            where year>={Y1_choice} and year<={Y2_choice} 
                            group by transaction_type,year,quarter 
                            order by Year,Quarter;"""
        else:
            if cate!="Average":
                query_q_7=f"""select Transaction_type,Year,Quarter,sum(amount) as Amount,sum(count) as Count from aggr_transaction 
                            where year>={Y1_choice} and year<={Y2_choice} and state="{cate1s}"
                            group by transaction_type,year,quarter 
                            order by Year,Quarter;"""
            else:
                query_q_7=f"""select Transaction_type,Year,Quarter,sum(amount)/sum(count) as Average from aggr_transaction 
                            where year>={Y1_choice} and year<={Y2_choice} and state="{cate1s}"
                            group by transaction_type,year,quarter 
                            order by Year,Quarter;"""
                

        
        cursor.execute(query_q_7)
        q_7 = pd.read_sql(query_q_7, connection)
        df=pd.DataFrame(q_7)
        df["Quarter"]=df["Year"].astype(str)+"q"+df["Quarter"].astype(str)
        if cate:
            fig7=px.line(df,
                        x="Quarter",
                        y=f"{cate}",
                        color="Transaction_type",
                        markers=False)

        call_tab_color=page2_tab_color()
        print(call_tab_color)
        tab1, tab2 = st.tabs(["Chart", "Data"])
        pd.set_option('display.float_format', '{:.2f}'.format)
        with tab1:
            st.plotly_chart(fig7)
        tab2.write(df)

#----------------------------------------------------------------------------------------------------------------------

if add_radio1=="Insurance-Transaction Trends":
    call_home=page2_analyse_title("Insurance-Transaction Trends")
    b_choice=st.selectbox("",["Amount","Count","Average"],index=0)
    query_q_2="""with A_I as
    (select year,sum(amount) as Insurance_amt,sum(count) as Insurance_count,
    sum(amount)/sum(count) as Avg_Insurance from aggr_insurance group by year order by year
    ),
    A_T as
    (select year,sum(amount) as Transaction_amt,sum(count) as Transaction_count,
    sum(amount)/sum(count) as Avg_Transaction from aggr_transaction group by year order by year)
    select A_T.year,A_I.Insurance_amt,A_I.Insurance_count,A_I.Avg_Insurance,
    A_T.Transaction_amt,A_T.Transaction_count,A_T.Avg_Transaction
    from A_T
    left join A_I on A_T.year=A_I.year;"""
    cursor.execute(query_q_2)
    q_2 = pd.read_sql(query_q_2, connection)
    df_q2 = pd.DataFrame(q_2)
    scaler = MinMaxScaler()
    cols_to_scale = ['Insurance_amt', 'Insurance_count','Transaction_amt', 'Transaction_count']
    df_q2[cols_to_scale] = scaler.fit_transform(df_q2[cols_to_scale])

    if b_choice=="Amount":
        fig2=px.line(df_q2,x="year",y=["Insurance_amt","Transaction_amt"],
                     markers=True)
        calling_layout_update=update_layout(fig2)
        st.plotly_chart(fig2)
    if b_choice=="Count":
        fig2=px.line(df_q2,x="year",y=["Insurance_count","Transaction_count"],
                     markers=True)
        calling_layout_update=update_layout(fig2)
        st.plotly_chart(fig2)
    if b_choice=="Average":
        fig2=px.line(df_q2,x="year",y=["Avg_Insurance","Avg_Transaction"],markers=True)
        calling_layout_update=update_layout(fig2)
        st.plotly_chart(fig2)

#----------------------------------------------------------------------------------------------------------------------

if add_radio1=="Recent Trends":
    call_home=page2_analyse_title("PhonePe Recent Trends")
    Content_text="In the recent trend analysis, we calculate the average value for 2024 and compare it with the 4th quarter of 2023 by taking the difference."
    page2_content(Content_text,side_text="left",color="#ffffff")
    a_choice=st.selectbox("",["Recent Market Performance",
                              "District Trends",
                              "Transaction_Type Trends"
                              ],
                              index=0)

    if a_choice=="Recent Market Performance":
        calling_transaction_count=recent_transaction_count()
#------x------     

    if a_choice=="District Trends":
        col1,col2=st.columns([1,1])

        with col1:
            a_choice=st.selectbox("",["Transaction","Insurance"])
            option_2={"Transaction":state_value_cap,"Insurance":state_value_cap}

        with col2:
            b_choice=st.selectbox("",option_2[a_choice],index=0)



        table="Map_transaction" if a_choice=="Transaction" else "Map_insurance"
        calling_district_analyse=district_analyse_chart(b_choice,table)

#------x------  

    if a_choice=="Transaction_Type Trends":
        query_9="""with q23_4 as
(select transaction_type,sum(count) as CNT_23,sum(amount) as AMT_23 from aggr_transaction where year=2023 and quarter =4
group by transaction_type),
avg_24 as(select transaction_type,sum(count)/4 as CNT_24,sum(amount)/4 as AMT_24 from aggr_transaction where year=2024
group by transaction_type)
select q23_4.transaction_type,q23_4.CNT_23,avg_24.CNT_24,
round((100*((avg_24.CNT_24-q23_4.CNT_23)/q23_4.CNT_23)),2) as Percent
from q23_4 join avg_24 on q23_4.transaction_type=avg_24.transaction_type;"""
        q_9 = pd.read_sql(query_9, connection)    
        df=pd.DataFrame(q_9)
        st.write(df)
            
#----------------------------------------------------------------------------------------------------------------------

if add_radio1=="Transaction Trends State_Wise":
        state_select=st.selectbox("",state_value_cap,index=0)
        col1,col2,col3=st.columns([1,1,1])
        year1=[2018,2019,2020,2021,2022,2023,2024]

        with col1:
            cate2=st.selectbox("",["Amount","Count","Average"],index=0)
        with col2:
            Y1_choice=st.selectbox("",year1,index=0,key="A")
        if Y1_choice:
            year2get = year1[year1.index(Y1_choice):]
        with col3:
            Y2_choice=st.selectbox("",year2get,index=0,key="B")

        if cate2!="Average":
            query_q_10=f"""select Year,Quarter,sum(amount) as Amount,sum(count) as Count from aggr_transaction 
                        where year>={Y1_choice} and year<={Y2_choice} and State="{state_select}"
                        group by Year,Quarter 
                        order by Year,Quarter;"""
        else:
            query_q_10=f"""select Year,Quarter,sum(amount)/sum(count) as Average from aggr_transaction 
                        where year>={Y1_choice} and year<={Y2_choice} and State="{state_select}"
                        group by Year,Quarter 
                        order by Year,Quarter;"""
            
        cursor.execute(query_q_10)
        q_10 = pd.read_sql(query_q_10, connection)
        df_10=pd.DataFrame(q_10)
        df_10["Quarter"]=df_10["Year"].astype(str)+"q"+df_10["Quarter"].astype(str)
        if cate2:
            fig10=px.line(df_10,
                        x="Quarter",
                        y=f"{cate2}",
                        markers=False)

        call_tab_color=page2_tab_color()
        tab1, tab2 = st.tabs(["Chart", "Data"])
        pd.set_option('display.float_format', '{:.2f}'.format)
        with tab1:
            st.plotly_chart(fig10)
        tab2.write(df_10)

#----------------------------------------------------------------------------------------------------------------------

page2_footer()