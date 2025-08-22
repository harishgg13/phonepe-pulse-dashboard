# PhonePe Pulse Dashboard -- Capstone Project

## 📌 Overview

This project is a **Streamlit-based interactive dashboard** built using
**PhonePe Pulse dataset**.
It allows users to explore insights on **transactions, insurance, and
user engagement trends** across India.

The dashboard integrates:
- **Data Processing & Storage**: Extracts and transforms JSON datasets.
  **cleaning the dataset** and pushing the datas to 
into MySQL tables (`Data.py`).
- **Interactive Visualizations**: Choropleth maps, bar/line charts, and
tabular insights with **Plotly**.
- **Multi-page Navigation**: Home, Reports, User Analysis, and About
sections with custom HTML/CSS.

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Frontend**: [Streamlit](https://streamlit.io/)
    **HTML/CSS**
-   **Backend/DB**: MySQL (via `pymysql`)
-   **Data Processing**: Python, Pandas, JSON
-   **Visualization**: Plotly Express
-   Used **Scikit-learn** (MinMaxScaler in
    `UserAnalyse.py` to compare two individual columns that has huge numeric difference in simple form)

------------------------------------------------------------------------

## 📂 Project Structure

    ├── Data.py            # Extracts PhonePe JSON data → Processes into Pandas → Inserts into MySQL
    ├── Home.py            # Streamlit Home Page (Transaction & Insurance Maps + Top States/Districts/Pincodes in  
                             interactive year and quarter changing option)
    ├── AnalysePage.py     # Streamlit Reports/Analysis page
    ├── UserAnalyse.py     # Streamlit User-Analysis page (Device usage, AppOpens vs Transactions, etc.)
    ├── HTML_CSS.py        # Custom styling (Header, Footer, Layout, Tabs)

------------------------------------------------------------------------

## 🚀 Features

### 🔹 Data Processing (`Data.py`)

-   Reads **aggregated**, **map**, and **top-level** JSON datasets.\
-   Creates structured **MySQL tables** 
    **Aggregated** - (`Aggr_transaction`,`Aggr_insurance`, `Aggr_user`,`Aggr_user_device`,).\
    **Map**(`Map_transaction`, `Map_insurance`, `Map_user`).\
    **Top**(`Top_insurance_districts`, `top_insurance_pincodes`, `top_transaction_districts`,
            `top_transaction_pincodes`, `top_user_districts`, `top_user_pincode`).\
-   Supports **insert/update sql query using python and automated**.

### 🔹 Home Page (`Home.py`)

-   Choropleth maps for **transactions** & **insurance** across Indian
    states.\
-   Top **states, districts, transaction types, and pincodes** by
    volume.\
-   Interactive filters by **Year** and **Quarter**.

### 🔹 Analysis Page (`AnalysisPage.py`) for report

-   **Top/Least performing** states/districts/pincodes (Amount,Count
    & Avg-amount-per-count).\
-   **Transaction Type trends** (Between each transaction type).\
-   **Transaction Trend State_wise** (time-series).\
-   **Recent trends** (2024 vs Q4 2023).

### 🔹 User Analysis (`UserAnalyse.py`) for user insights

-   **Top/Least performing** states/districts/pincodes (Registered Users
    & Avg-App-Opens-per-registered-user).\
-   **Device usage trends** (state-wise & nationwide).\
-   **App Opens vs Transaction Count** (time-series).\
-   **Recent District-wise Analysis** (2024 vs Q4 2023 of recent market performance, transaction trend and district).

### 🔹 UI/UX Enhancements (`HTML_CSS.py`)

-   Custom header & footer with **branding**.\
-   Dynamic background colors (based on selected analysis).\
-   Styled tabs & responsive layout.

------------------------------------------------------------------------

## ⚙️ Setup & Installation

### 1️⃣ Clone Repository

``` bash
git clone https://github.com/harishgg13/phonepe-pulse-dashboard.git
cd phonepe-pulse-dashboard
```

### 2️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

**requirements.txt** should include:

    streamlit
    pandas
    pymysql
    plotly
    requests
    scikit-learn

### 3️⃣ Setup MySQL Database

-   Create a database named `PhonePe`.\
-   Update MySQL credentials in `Data.py`, `Home.py`, and
    `UserAnalyse.py`:\

``` python
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="PhonePe"
)
```

-   Run `Data.py` to populate tables.

### 4️⃣ Run Streamlit App

``` bash
streamlit run Home.py
```

------------------------------------------------------------------------

## 📊 Example Dashboard

-   **Home Page** → Transaction/Insurance trends with choropleth map\
-   **Reports Page** → Deep dive into transaction datasets\
-   **User Analysis Page** → Device usage, engagement dynamics,
    top/least performing regions

------------------------------------------------------------------------

## 👨‍💻 Author

**G G Harish**\
- 📧 Email: <harishgg03@gmail.com>\
- 💼 LinkedIn: [harishgg13](https://www.linkedin.com/in/ggharish13)
