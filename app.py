# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import categorize_expenses, plot_expense_pie, plot_monthly_trends, generate_saving_tips

# ✨ Set Streamlit page configuration
st.set_page_config(page_title="BudgetBuddy - Personal Finance Analyzer", page_icon="💼", layout="wide")

# 🌍 App Title
st.title("💼 BudgetBuddy - Personal Finance Analyzer")
st.markdown("Manually enter your incomes and expenses to analyze your spending habits!")

# 📋 Manual Input Section
st.header("📝 Add Your Entries")

with st.form(key='entry_form'):
    entry_date = st.date_input("Date")
    description = st.text_input("Description")
    amount = st.number_input("Amount ($)", step=0.01, format="%.2f")
    entry_type = st.selectbox("Type", ["Income", "Expense"])
    submit_button = st.form_submit_button(label='Add Entry')

if 'data' not in st.session_state:
    st.session_state['data'] = pd.DataFrame(columns=['Date', 'Description', 'Amount', 'Type'])

if submit_button:
    new_entry = pd.DataFrame({
        'Date': [pd.to_datetime(entry_date)],
        'Description': [description],
        'Amount': [amount if entry_type == 'Income' else -amount],
        'Type': [entry_type]
    })
    st.session_state['data'] = pd.concat([st.session_state['data'], new_entry], ignore_index=True)

# 📊 Display Data
if not st.session_state['data'].empty:
    df = st.session_state['data']

    st.subheader("🔍 Your Entries")
    st.dataframe(df)

    st.subheader("📊 Financial Summary")
    total_income = df[df['Type'] == 'Income']['Amount'].sum()
    total_expense = df[df['Type'] == 'Expense']['Amount'].sum()
    balance = total_income + total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"$ {total_income:,.2f}")
    col2.metric("Total Expenses", f"$ {abs(total_expense):,.2f}")
    col3.metric("Net Balance", f"$ {balance:,.2f}", delta=f"{'+' if balance>=0 else ''}{balance:,.2f}")

    st.subheader("💼 Expense Categorization")
    df['Category'] = df['Description'].apply(categorize_expenses)

    st.subheader("📊 Expense Breakdown")
    plot_expense_pie(df)

    st.subheader("📊 Monthly Trends")
    plot_monthly_trends(df)

    st.subheader("🌟 Smart Saving Suggestions")
    generate_saving_tips(df)
else:
    st.info("Please add some entries to get started!")