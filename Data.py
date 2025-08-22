#importing necessary package
import os #to moce into individual directory, to interact with operating system
import pandas as pd #to read the json file
import json
import pymysql

def create_table(cursor,connection,table_name,column_names):
    create_query=f"create table if not exists {table_name}({column_names})"
    cursor.execute(create_query)
    connection.commit()
    return f"Table {table_name} created Successfully"

def insert_values(cursor,connection,table_name,insert,values):
    insert_query=f"insert into {table_name} {insert};"
    cursor.execute(insert_query,values)
    connection.commit()
    # return f"Row {cursor.rowcount} is inserted successfully"


# ---------------------------------------------------------------------------------------------------------------------------------------

# Aggregate Transaction Data
# extracting state list from file
path="/Users/ggharish13/Data Science/Capstone Project/PhonePe Project/data/data/aggregated/transaction/country/india/state/"
aggr_state_list=os.listdir(path)
# print(aggr_state_list) #to check the state list

# extracting aggregated transaction datas using loops.
aggr_transaction_Dict={"state":[],"year":[],"quarter":[],"name":[],"count":[],"amount":[]}
for i in aggr_state_list:
    p_i=path+i+"/"
    aggr_transation_year=os.listdir(p_i)
    for j in aggr_transation_year:
        p_j=p_i+j+"/"
        aggr_transaction_quarter=os.listdir(p_j)
        for k in aggr_transaction_quarter:
            p_k=p_j+k
            data=open(p_k,"r")
            d=json.load(data)
            for z in d["data"]["transactionData"]:
                # print(z)
                Name=z["name"]
                count=z["paymentInstruments"][0]["count"]
                amount=z["paymentInstruments"][0]["amount"]
                aggr_transaction_Dict["state"].append(i)
                aggr_transaction_Dict["year"].append(int(j))
                aggr_transaction_Dict["quarter"].append(int(k.strip(".json")))
                aggr_transaction_Dict["name"].append(Name)
                aggr_transaction_Dict["count"].append(count)
                aggr_transaction_Dict["amount"].append(amount)

aggr_transation=pd.DataFrame(aggr_transaction_Dict)
# pd.set_option('display.float_format', '{:.15f}'.format)
print(aggr_transation)
# print(aggr_transation['amount'].head())

#extracting values from DF
# Aggr_Df_values = [tuple(x if not hasattr(x, 'item') else x.item() for x in row) for row in aggr_transation.values]
# print(Aggr_Df_values[1])
# print(type(Aggr_Df_values[1]))


aggr_transaction_values=aggr_transation.values
# print(type(aggr_transaction_values))
try:
    #establishing connection
    connection=pymysql.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="PhonePe"
    )
    cursor=connection.cursor()

    # create table
    create_table_name="Aggr_transation"
    attributes_for_table="State varchar(100),Year int, Quarter int,Name varchar(100),Count int, Amount float"
    # calling_create_table=create_table(cursor,connection,create_table_name,attributes_for_table)
    # print(calling_create_table)

    #altering the table data type
    # modify_query=f"alter table {create_table_name} modify amount decimal(20,2);"
    # cursor.execute(modify_query)
    # connection.commit()

    # insert Table
    for i in range(len(aggr_transaction_values)):
        values_from_df=tuple(aggr_transaction_values[i])
        insert_into_table="(State, Year, Quarter, Name, Count, Amount) values (%s,%s,%s,%s,%s,%s)"
        # print(values_from_df)
        # calling_insert=insert_values(cursor,connection,create_table_name,insert_into_table,values_from_df)

except Exception as e:
    print(str(e))



# --------------------------------------------------------------------------------------------------------------------------------------

# Aggregate Insurance Data
#redirecting the filepath again
path="/Users/ggharish13/Data Science/Capstone Project/PhonePe Project/data/data/aggregated/insurance/country/india/state/"
aggr_state_list=os.listdir(path)
# extracting aggregated insurance datas using loops.
aggr_insurance_Dict={"state":[],"year":[],"quarter":[],"count":[],"amount":[]}
for i in aggr_state_list:
    p_i=path+i+"/"
    aggr_insurance_year=os.listdir(p_i)
    for j in aggr_insurance_year:
        p_j=p_i+j+"/"
        aggr_insurance_quarter=os.listdir(p_j)
        for k in aggr_insurance_quarter:
            p_k=p_j+k
            data=open(p_k,"r")
            d=json.load(data)
            for z in d["data"]["transactionData"]:
                # print(z)
                count=z["paymentInstruments"][0]["count"]
                amount=z["paymentInstruments"][0]["amount"]
                aggr_insurance_Dict["state"].append(i)
                aggr_insurance_Dict["year"].append(int(j))
                aggr_insurance_Dict["quarter"].append(int(k.strip(".json")))
                aggr_insurance_Dict["count"].append(count)
                aggr_insurance_Dict["amount"].append(amount)
aggr_insurance=pd.DataFrame(aggr_insurance_Dict)
# print(aggr_insurance) #to check the insurance dataframe

aggr_Insurance_values=aggr_insurance.values
# print(type(aggr_transaction_values))
try:

    # create table
    create_table_name="Aggr_Insurance"
    attributes_for_table="State varchar(100),Year int, Quarter int,Count bigint, Amount decimal(20,2)"
    # calling_create_table=create_table(cursor,connection,create_table_name,attributes_for_table)
    # print(calling_create_table)

    #altering the table data type
    # modify_query=f"alter table {create_table_name} modify amount decimal(20,2);"
    # cursor.execute(modify_query)
    # connection.commit()

    # insert Table
    for i in range(len(aggr_Insurance_values)):
        values_from_df=tuple(aggr_Insurance_values[i])
        insert_into_table="(State, Year, Quarter, Count, Amount) values (%s,%s,%s,%s,%s)"
        # print(values_from_df)
        # calling_insert=insert_values(cursor,connection,create_table_name,insert_into_table,values_from_df)

except Exception as e:
    print(str(e))



# --------------------------------------------------------------------------------------------------------------------------------------

# Aggregate user Data
#redirecting the filepath again
path="/Users/ggharish13/Data Science/Capstone Project/PhonePe Project/data/data/aggregated/user/country/india/state/"
aggr_state_list=os.listdir(path)
# extracting aggregated user datas using loops.
aggr_user_Dict={"state":[],"year":[],"quarter":[],"registeredUsers":[],"appOpens":[]} # added app opens because, in past how many app open and present how many app opens, helps to predict the UI of the app.
aggr_user_device_Dict={"state":[],"year":[],"quarter":[],"Brand":[],"Count":[],"Percentage":[]}
for i in aggr_state_list:
    p_i=path+i+"/"
    aggr_user_year=os.listdir(p_i)
    for j in aggr_user_year:
        p_j=p_i+j+"/"
        aggr_user_quarter=os.listdir(p_j)
        for k in aggr_user_quarter:
            p_k=p_j+k
            Aggr_user_data=open(p_k,"r")
            d=json.load(Aggr_user_data)
            Reg_user=d["data"]["aggregated"]["registeredUsers"]
            app_open=d["data"]["aggregated"]["appOpens"]
            aggr_user_Dict["state"].append(i)
            aggr_user_Dict["year"].append(int(j))
            aggr_user_Dict["quarter"].append(int(k.strip(".json")))
            aggr_user_Dict["registeredUsers"].append(Reg_user)
            aggr_user_Dict["appOpens"].append(app_open)
            try:
                for z in d ["data"]["usersByDevice"]:
                    device=z["brand"]
                    count=z["count"]
                    per=z["percentage"]
                    aggr_user_device_Dict["state"].append(i)
                    aggr_user_device_Dict["year"].append(int(j))
                    aggr_user_device_Dict["quarter"].append(int(k.strip(".json")))
                    aggr_user_device_Dict["Brand"].append(device)
                    aggr_user_device_Dict["Count"].append(count)
                    aggr_user_device_Dict["Percentage"].append(per)

            except:
                pass
aggr_user_device=pd.DataFrame(aggr_user_device_Dict)
aggr_user_device_values=aggr_user_device.values

aggr_user=pd.DataFrame(aggr_user_Dict)
aggr_user_values=aggr_user.values

try:

    # create table
    create_table_name="Aggr_user_device"
    attributes_for_table="State varchar(100),Year int, Quarter int, registeredUsers bigint, appOpens bigint"
    # calling_create_table=create_table(cursor,connection,create_table_name,attributes_for_table)
    # print(calling_create_table)

    #altering the table data type
    # modify_query=f"alter table {create_table_name} modify amount decimal(20,2);"
    # cursor.execute(modify_query)
    # connection.commit()

    # insert Table
    for i in range(len(aggr_user_device_values)):
        values_from_df=tuple(aggr_user_device_values[i])
        insert_into_table="(State, Year, Quarter, Device, Count,Percentage) values (%s,%s,%s,%s,%s,%s)"
        # print(values_from_df)
        calling_insert=insert_values(cursor,connection,create_table_name,insert_into_table,values_from_df)

except Exception as e:
    print(str(e))

# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------

# Map

# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------

# map transaction
path="/Users/ggharish13/Data Science/Capstone Project/PhonePe Project/data/data/map/transaction/hover/country/india/state/"
map_state_list=os.listdir(path)
map_transaction_dict={"State":[],"Year":[],"quarter":[],"District_Name":[],"count":[],"amount":[]}

for i in map_state_list:
    p_i=path+i+"/"
    map_transaction_year=os.listdir(p_i)
    for j in map_transaction_year:
        p_j=p_i+j+"/"
        map_transaction_quarter=os.listdir(p_j)
        # print(aggr_transation_quarter)
        for k in map_transaction_quarter:
            p_k=p_j+k
            # print(p_k)
            map_transaction_data=open(p_k,"r")
            d=json.load(map_transaction_data)
            for z in d["data"]["hoverDataList"]:
                map_tran_name=z["name"]
                map_tran_count=z["metric"][0]["count"]
                map_tran_amount=z["metric"][0]["amount"]
                map_transaction_dict["State"].append(i)
                map_transaction_dict["Year"].append(int(j))
                map_transaction_dict["quarter"].append(int(k.strip(".json")))
                map_transaction_dict["District_Name"].append(map_tran_name)
                map_transaction_dict["count"].append(map_tran_count)
                map_transaction_dict["amount"].append(map_tran_amount)

map_transaction = pd.DataFrame(map_transaction_dict)
# print(map_transaction)
map_transaction_value=map_transaction.values

try:

    # create table
    create_table_name="Map_Transation"
    attributes_for_table="State varchar(100),Year int, Quarter int,District_Name varchar(100),Count bigint, Amount decimal(25,2)"
    # calling_create_table=create_table(cursor,connection,create_table_name,attributes_for_table)
    # print(calling_create_table)

    #altering the table data type
    # modify_query=f"alter table {create_table_name} modify amount decimal(20,2);"
    # cursor.execute(modify_query)
    # connection.commit()

    # insert Table
    for i in range(len(map_transaction_value)):
        values_from_df=tuple(map_transaction_value[i])
        insert_into_table="(State, Year, Quarter, District_Name, Count, Amount) values (%s,%s,%s,%s,%s,%s)"
        # print(values_from_df)
        # calling_insert=insert_values(cursor,connection,create_table_name,insert_into_table,values_from_df)

except Exception as e:
    print(str(e))
                
# --------------------------------------------------------------------------------------------------------------------------------------


# map insurance
path="/Users/ggharish13/Data Science/Capstone Project/PhonePe Project/data/data/map/insurance/hover/country/india/state/"
map_state_list=os.listdir(path)
map_insurance_dict={"State":[],"Year":[],"quarter":[],"District_Name":[],"count":[],"amount":[]}

for i in map_state_list:
    p_i=path+i+"/"
    map_insurance_year=os.listdir(p_i)
    for j in map_insurance_year:
        p_j=p_i+j+"/"
        map_insurance_quarter=os.listdir(p_j)
        # print(aggr_transation_quarter)
        for k in map_insurance_quarter:
            p_k=p_j+k
            # print(p_k)
            map_insurance_data=open(p_k,"r")
            d=json.load(map_insurance_data)
            for z in d["data"]["hoverDataList"]:
                map_tran_name=z["name"]
                map_tran_count=z["metric"][0]["count"]
                map_tran_amount=z["metric"][0]["amount"]
                map_insurance_dict["State"].append(i)
                map_insurance_dict["Year"].append(int(j))
                map_insurance_dict["quarter"].append(int(k.strip(".json")))
                map_insurance_dict["District_Name"].append(map_tran_name)
                map_insurance_dict["count"].append(map_tran_count)
                map_insurance_dict["amount"].append(map_tran_amount)

map_insurance = pd.DataFrame(map_insurance_dict)
# print(map_insurance)
map_insurance_value=map_insurance.values

try:

    # create table
    create_table_name="Map_Insurance"
    attributes_for_table="State varchar(100),Year int, Quarter int,District_Name varchar(100),Count bigint, Amount decimal(25,2)"
    # calling_create_table=create_table(cursor,connection,create_table_name,attributes_for_table)
    # print(calling_create_table)

    #altering the table data type
    # modify_query=f"alter table {create_table_name} modify amount decimal(20,2);"
    # cursor.execute(modify_query)
    # connection.commit()

    # insert Table
    for i in range(len(map_insurance_value)):
        values_from_df=tuple(map_insurance_value[i])
        insert_into_table="(State, Year, Quarter, District_Name, Count, Amount) values (%s,%s,%s,%s,%s,%s)"
        # print(values_from_df)
        # calling_insert=insert_values(cursor,connection,create_table_name,insert_into_table,values_from_df)

except Exception as e:
    print(str(e))


# --------------------------------------------------------------------------------------------------------------------------------------
# map user

path="/Users/ggharish13/Data Science/Capstone Project/PhonePe Project/data/data/map/user/hover/country/india/state/"
map_state_list=os.listdir(path)
map_user_dict={"State":[],"Year":[],"quarter":[],"District_Name":[],"registeredUsers":[],"appOpens":[]}

for i in map_state_list:
    p_i=path+i+"/"
    map_user_year=os.listdir(p_i)
    for j in map_user_year:
        p_j=p_i+j+"/"
        map_user_quarter=os.listdir(p_j)
        # print(aggr_transation_quarter)
        for k in map_user_quarter:
            p_k=p_j+k
            # print(p_k)
            map_user_data=open(p_k,"r")
            d=json.load(map_user_data)
            z = d["data"]["hoverData"]
            for x in z:
                map_user_reg_user=z[x]["registeredUsers"]
                map_user_app_open=z[x]["appOpens"]
                map_user_dict["State"].append(i)
                map_user_dict["Year"].append(int(j))
                map_user_dict["quarter"].append(int(k.strip(".json")))
                map_user_dict["District_Name"].append(x)
                map_user_dict["registeredUsers"].append(map_user_reg_user)
                map_user_dict["appOpens"].append(map_user_app_open)

map_user=pd.DataFrame(map_user_dict)
# print(map_user)
map_user_values=map_user.values

try:

    # create table
    create_table_name="Map_user"
    attributes_for_table="State varchar(100),Year int, Quarter int,District_Name varchar(100),registeredUsers bigint, appOpens bigint"
    # calling_create_table=create_table(cursor,connection,create_table_name,attributes_for_table)
    # print(calling_create_table)

    #altering the table data type
    # modify_query=f"alter table {create_table_name} modify amount decimal(20,2);"
    # cursor.execute(modify_query)
    # connection.commit()

    # insert Table
    for i in range(len(map_user_values)):
        values_from_df=tuple(map_user_values[i])
        insert_into_table="(State, Year, Quarter, District_Name, registeredUsers, appOpens) values (%s,%s,%s,%s,%s,%s)"
        # print(values_from_df)
        # calling_insert=insert_values(cursor,connection,create_table_name,insert_into_table,values_from_df)

except Exception as e:
    print(str(e))

# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------

# Top Pincode

# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------

# top transaction

path = "/Users/ggharish13/Data Science/Capstone Project/PhonePe Project/data/data/top/transaction/country/india/state/"
Top_state_list=os.listdir(path)
top_transaction_dict={"State":[],"Year":[],"quarter":[],
                      "Pincode":[],"count":[],"amount":[]}
top_transaction_district_dict={"State":[],"Year":[],"quarter":[],
                      "District":[],"count":[],"amount":[]}

for i in Top_state_list:
    p_i=path+i+"/"
    top_transaction_year=os.listdir(p_i)
    for j in top_transaction_year:
        p_j=p_i+j+"/"
        top_transaction_quarter=os.listdir(p_j)
        for k in top_transaction_quarter:
            p_k=p_j+k
            top_transaction_data=open(p_k,"r")
            d=json.load(top_transaction_data)
            for z in d["data"]["pincodes"]:
                # print(z)
                pincode=z["entityName"]
                count=z["metric"]["count"]
                amount=z["metric"]["amount"]
                top_transaction_dict["State"].append(i)
                top_transaction_dict["Year"].append(int(j))
                top_transaction_dict["quarter"].append(int(k.strip(".json")))
                top_transaction_dict["Pincode"].append(pincode)
                top_transaction_dict["amount"].append(amount)
                top_transaction_dict["count"].append(count)
            for x in d["data"]["districts"]:
                # print(z)
                Districts=x["entityName"]
                count=x["metric"]["count"]
                amount=x["metric"]["amount"]
                top_transaction_district_dict["State"].append(i)
                top_transaction_district_dict["Year"].append(int(j))
                top_transaction_district_dict["quarter"].append(int(k.strip(".json")))
                top_transaction_district_dict["District"].append(Districts)
                top_transaction_district_dict["amount"].append(amount)
                top_transaction_district_dict["count"].append(count)

top_transaction=pd.DataFrame(top_transaction_dict)
# print(top_transaction)
top_transaction_value=top_transaction.values

top_transaction_district=pd.DataFrame(top_transaction_district_dict)
# print(top_transaction_district)
top_transaction_district_value=top_transaction_district.values

try:

    # create table
    create_table_name="top_transaction_pincodes"
    attributes_for_table="State varchar(100),Year int, Quarter int,Pincode int,count bigint, amount decimal(30,2)"
    # calling_create_table=create_table(cursor,connection,create_table_name,attributes_for_table)
    # print(calling_create_table)

    #altering the table data type
    # modify_query=f"alter table {create_table_name} modify amount decimal(30,2);"
    # cursor.execute(modify_query)
    # connection.commit()

    # insert Table
    for i in range(len(top_transaction_value)):
        values_from_df=tuple(top_transaction_value[i])
        insert_into_table="(State, Year, Quarter, Pincode, count, amount) values (%s,%s,%s,%s,%s,%s)"
        # print(values_from_df)
        # calling_insert=insert_values(cursor,connection,create_table_name,insert_into_table,values_from_df)

except Exception as e:
    print(str(e))


# --------------------------------------------------------------------------------------------------------------------------------------

# top insurance

path = "/Users/ggharish13/Data Science/Capstone Project/PhonePe Project/data/data/top/insurance/country/india/state/"
Top_state_list=os.listdir(path)
top_insurance_dict={"State":[],"Year":[],"quarter":[],
                      "Pincode":[],"count":[],"amount":[]}
top_insurance_District_dict={"State":[],"Year":[],"quarter":[],
                      "District":[],"count":[],"amount":[]}


for i in Top_state_list:
    p_i=path+i+"/"
    top_insurance_year=os.listdir(p_i)
    for j in top_insurance_year:
        p_j=p_i+j+"/"
        top_insurance_quarter=os.listdir(p_j)
        for k in top_insurance_quarter:
            p_k=p_j+k
            top_insurance_data=open(p_k,"r")
            d=json.load(top_insurance_data)
            for z in d["data"]["pincodes"]:
                pincode=z["entityName"]
                count=z["metric"]["count"]
                amount=z["metric"]["amount"]
                top_insurance_dict["State"].append(i)
                top_insurance_dict["Year"].append(int(j))
                top_insurance_dict["quarter"].append(int(k.strip(".json")))
                top_insurance_dict["Pincode"].append(pincode)
                top_insurance_dict["amount"].append(amount)
                top_insurance_dict["count"].append(count)
            for x in d["data"]["districts"]:
                Districts=x["entityName"]
                count=x["metric"]["count"]
                amount=x["metric"]["amount"]
                top_insurance_District_dict["State"].append(i)
                top_insurance_District_dict["Year"].append(int(j))
                top_insurance_District_dict["quarter"].append(int(k.strip(".json")))
                top_insurance_District_dict["District"].append(Districts)
                top_insurance_District_dict["amount"].append(amount)
                top_insurance_District_dict["count"].append(count)


top_isurance=pd.DataFrame(top_insurance_dict)
# print(top_isurance)
top_insurance_value=top_isurance.values

top_isurance_district=pd.DataFrame(top_insurance_District_dict)
# print(top_isurance_district)
top_insurance_district_value=top_isurance_district.values

try:

    # create table
    create_table_name="top_insurance_pincodes"
    attributes_for_table="State varchar(100),Year int, Quarter int,Pincode int,count bigint, amount bigint"
    # calling_create_table=create_table(cursor,connection,create_table_name,attributes_for_table)
    # print(calling_create_table)

    #altering the table data type
    # modify_query=f"alter table {create_table_name} modify amount decimal(30,2);"
    # cursor.execute(modify_query)
    # connection.commit()

    # insert Table
    for i in range(len(top_insurance_value)):
        values_from_df=tuple(top_insurance_value[i])
        insert_into_table="(State, Year, Quarter, Pincode, count, amount) values (%s,%s,%s,%s,%s,%s)"
        # print(values_from_df)
        # calling_insert=insert_values(cursor,connection,create_table_name,insert_into_table,values_from_df)

except Exception as e:
    print(str(e))

# --------------------------------------------------------------------------------------------------------------------------------------

# top user

path = "/Users/ggharish13/Data Science/Capstone Project/PhonePe Project/data/data/top/user/country/india/state/"
Top_state_list=os.listdir(path)
top_user_dict={"State":[],"Year":[],"quarter":[],
                      "Pincode":[],"Registered_user":[]}
top_user_district_dict={"State":[],"Year":[],"quarter":[],
                      "District":[],"Registered_user":[]}


for i in Top_state_list:
    if i == ".DS_Store":
        continue
    p_i=path+i+"/"
    top_user_year=os.listdir(p_i)
    for j in top_user_year:
        if j == ".DS_Store":
            continue
        p_j=p_i+j+"/"
        top_user_quarter=os.listdir(p_j)
        for k in top_user_quarter:
            p_k=p_j+k
            top_user_data=open(p_k,"r")
            d=json.load(top_user_data)
            for z in d["data"]["pincodes"]:
                pincode=z["name"]
                Registered_u=z["registeredUsers"]
                top_user_dict["State"].append(i)
                top_user_dict["Year"].append(int(j))
                top_user_dict["quarter"].append(int(k.strip(".json")))
                top_user_dict["Pincode"].append(pincode)
                top_user_dict["Registered_user"].append(Registered_u)
            for x in d["data"]["districts"]:
                district=x["name"]
                Registered_u=x["registeredUsers"]
                top_user_district_dict["State"].append(i)
                top_user_district_dict["Year"].append(int(j))
                top_user_district_dict["quarter"].append(int(k.strip(".json")))
                top_user_district_dict["District"].append(district)
                top_user_district_dict["Registered_user"].append(Registered_u)


top_user=pd.DataFrame(top_user_dict)
# print(top_user)
top_user_value=top_user.values

top_user_district=pd.DataFrame(top_user_district_dict)
# print(top_user_district)
top_user_district_value=top_user_district.values



try:

    # create table
    create_table_name="Top_User"
    attributes_for_table="State varchar(100),Year int, Quarter int,Pincode int,Registered_user bigint"
    # calling_create_table=create_table(cursor,connection,create_table_name,attributes_for_table)
    # print(calling_create_table)

    #altering the table data type
    # modify_query=f"alter table {create_table_name} modify amount decimal(20,2);"
    # cursor.execute(modify_query)
    # connection.commit()

    # insert Table
    for i in range(len(top_user_value)):
        values_from_df=tuple(top_user_value[i])
        insert_into_table="(State, Year, Quarter, Pincode, Registered_user) values (%s,%s,%s,%s,%s)"
        # print(values_from_df)
        # calling_insert=insert_values(cursor,connection,create_table_name,insert_into_table,values_from_df)

except Exception as e:
    print(str(e))
