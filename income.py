import mysql.connector
from datetime import date
import streamlit as st
import pandas as pd

cnx = mysql.connector.connect(host='127.0.0.1',user='root',password='sHj@6378#jw',database="finances")


cursor = cnx.cursor()

# cursor.execute('CREATE DATABASE finances')
cursor.execute("USE finances")
# cursor.execute("CREATE TABLE daily_finances (id INT AUTO_INCREMENT PRIMARY KEY,date DATE,income FLOAT,expense FLOAT,comment TEXT)")






# # Get today's date
# today = date.today()

# # Ask user for income and expense amounts
# income = float(input("Enter income for today: "))
# expense = float(input("Enter expense for today: "))

# # Ask user for comment on expense
# comment = input("Enter comment for expense (optional): ")

# # Insert data into the database
# cursor = cnx.cursor()
# sql = "INSERT INTO daily_finances (date, income, expense, comment) VALUES (%s, %s, %s, %s)"
# val = (today, income, expense, comment)
# cursor.execute(sql, val)
# cnx.commit()

# # Print confirmation message
# print("Data saved successfully!")







# Define function to insert data into the database
def insert_data(date, income, expense, comment):
    cursor = cnx.cursor()
    sql = "INSERT INTO daily_finances (date, income, expense, comment) VALUES (%s, %s, %s, %s)"
    val = (date, income, expense, comment)
    cursor.execute(sql, val)
    cnx.commit()

# Define function to display data from the database
def display_data():
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM daily_finances")
    rows = cursor.fetchall()
    if len(rows) == 0:
        st.warning("No data found.")
    else:
        df = pd.DataFrame(rows, columns=["ID", "Date", "Income", "Expense", "Comment"])
        df = df.set_index("ID")
        st.dataframe(df)

        total_income = df["Income"].sum()
        total_expense = df["Expense"].sum()
        profit = total_income - total_expense

        st.write(f"Total income: {total_income:.2f}")
        st.write(f"Total expense: {total_expense:.2f}")
        st.write(f"Profit: {profit:.2f}")

# Define Streamlit app
def app():
    st.title("Daily Finances Tracker")

    # Get today's date
    today = date.today().strftime("%Y-%m-%d")

    # Ask user for income and expense amounts
    income = st.number_input("Enter income for today:", step=0.01)
    expense = st.number_input("Enter expense for today:", step=0.01)

    # Ask user for comment on expense
    comment = st.text_input("Enter comment for expense (optional):")

    # Insert data into the database when the user clicks the "Save" button
    if st.button("Save"):
        insert_data(today, income, expense, comment)
        st.success("Data saved successfully!")

    # Display data from the database when the user clicks the "Show data" button
    if st.button("Show data"):
        display_data()

# Define Streamlit login page
def login():
    st.title("Login")

    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if username == "Skifter" and password == "Murati":
        app()
    elif username != "" and password != "":
        st.error("Invalid username or password.")

# Run the Streamlit app
if __name__ == '__main__':
    login()