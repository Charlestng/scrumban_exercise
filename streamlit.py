import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
import os

import plotly.graph_objects as go  # pip install plotly
import streamlit as st  # pip install streamlit

# -- create csv file if not exist
import pandas as pd
if "finance.csv" not in os.listdir():
    pd.DataFrame(columns=["amount", "date", "type", "comment", "category"]).to_csv("finance.csv",index=False)

finance = pd.read_csv("finance.csv")
if len(finance.index) == 0:
    last_index = -1
else:
    last_index = finance.index[-1]

# -------------- SETTINGS --------------
incomes = ["Salary", "Blog", "Other Income"]
expenses = ["Rent", "Utilities", "Groceries", "Car", "Other Expenses", "Saving"]
currency = "USD"
page_title = "Income and Expense Tracker"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])


# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# --- INPUT & SAVE PERIODS ---
with st.form("entry_form", clear_on_submit=True):
    amount = st.number_input("enter amount",min_value=0, format="%i", step=10)
    date = st.date_input("enter date")
    type = st.selectbox("choose expense or revenue", ["expense", "revenue"])
    comment = st.text_input("enter comment")
    category = st.selectbox("select category", ["salary", "tranportation",
                                                "grocery",
                                                "other expenses"])

    "---"
    submitted = st.form_submit_button("Save Data")
    if submitted:
        newline = pd.DataFrame({"amount" : amount,
                                    "date": date, 
                                    "type": type, 
                                    "comment": comment, 
                                    "category": category},index=[last_index+1])
        finance = pd.concat([finance,
                                newline])
        finance.to_csv("finance.csv", index=False)
        st.success("Data saved!")

with st.form("budget", clear_on_submit=True):
    budget_grocery = st.number_input("grocery budget", min_value=0)
    tranportation_grocery = st.number_input("transportation budget", min_value=0)
    budget_total = st.number_input("Total budget", min_value=0)
    "---"
    submitted = st.form_submit_button("Save Budget Data")
    if submitted:
        budget = pd.DataFrame({"budget_grocery" : budget_grocery,
                                    "tranportation_grocery": tranportation_grocery,
                                    "budget_total":budget_total},
                                    index=[0])
    
        budget.to_csv("budget.csv", index=False)
        st.success("Data saved!")