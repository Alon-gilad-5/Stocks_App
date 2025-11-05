# Stocks_App: Database-Centric Financial Portfolio Simulator

## 🎯 Project Overview
The Stocks_App is a robust web application built using the **Django framework** with a strong focus on **direct SQL interaction**. This project serves as a **database-centric financial simulator**, allowing users to manage simulated portfolios and transactions against market data derived from a dedicated database.

It demonstrates proficiency in integrating web frameworks with **complex, pre-existing SQL schemas** and executing **raw SQL queries** directly from the application's backend.

## ✨ Key Features & Functionality

This application showcases the following capabilities, all implemented using raw SQL commands executed via the Django cursor:

### 1. Database-Focused Transactions (CRUD)
* **Cash Transactions (`/transaction`):** Allows investors to **deposit** (add) cash, which updates the `Amount` field in the **`Investor`** table and logs the transaction in the **`Transactions`** table.
* **Stock Buying (`/buy`):** Processes stock purchases by checking for sufficient available cash, verifying that the investor and company exist, and preventing duplicate purchases on the last available trading date. It updates the **`Buying`** and **`Investor`** tables.

### 2. Complex SQL Query Reporting (`/query_answers`)
The application executes and displays the results of three distinct reporting queries (views.py):
* **Query 1 (Total Spent):** Calculates the total amount spent by each **`diverse_investor`** and lists them in descending order.
* **Query 2 (Top Buyers):** Identifies the **top buyer** for each stock symbol based on quantity.
* **Query 3 (Profitable Company Buyers):** Counts the number of distinct buyers for each company classified as 'profitable'.

### 3. Database Architecture
* **Database First Approach:** The Django models (`models.py`) are configured with `managed = False`, reflecting a database structure that was defined externally and is managed directly via SQL.
* **Core Entities:** The application relies on core SQL tables: **`Investor`**, **`Company`**, **`Stock`**, **`Buying`**, and **`Transactions`**.
* **Technology:** Connects directly to an **Azure Microsoft SQL Server** instance.

## 🛠 Technology Stack

* **Backend Framework:** **Django** (Python 5.0.3)
* **Database:** **Microsoft SQL Server (MSSQL)** on Azure (using ODBC Driver 17)
* **Data Interaction:** **Raw SQL** execution via `django.db.connection.cursor()` (instead of the standard Django ORM).
* **Frontend:** HTML, Django Template Language (DTL).

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### Prerequisites
* Python 3.x
* `pip` (Python package installer)
* An ODBC Driver (e.g., ODBC Driver 17 for SQL Server) must be installed on your machine.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Alon-gilad-5/Stocks_App.git](https://github.com/Alon-gilad-5/Stocks_App.git)
    cd Stocks_App
    ```

2.  **Set up Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # .\venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**
    *(Note: The dependencies must include `django`, `pyodbc`, and any other necessary packages in a `requirements.txt` file.)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Configuration (CRITICAL):**
    You must update the database credentials in `settings.py` to match your local setup or a secure environment variable configuration:
    ```python
    # settings.py snippet (Must be updated/secured)
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': 'YOUR_DB_NAME',
            'USER': 'YOUR_DB_USER',
            'PASSWORD': 'YOUR_DB_PASSWORD',
            'HOST': 'YOUR_DB_HOST',
            'PORT': '1433',
            'OPTIONS': {"driver": "ODBC Driver 17 for SQL Server"}
        },
    }
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application will be accessible at `http://127.0.0.1:8000/`.

---
