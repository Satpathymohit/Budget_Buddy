# utils.py
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def categorize_expenses(description):
    description = str(description).lower()
    if any(word in description for word in ['grocery', 'supermarket', 'mart']):
        return 'Groceries'
    elif any(word in description for word in ['uber', 'ola', 'taxi', 'fuel', 'gas']):
        return 'Transport'
    elif any(word in description for word in ['rent', 'apartment']):
        return 'Rent'
    elif any(word in description for word in ['restaurant', 'cafe', 'food', 'dining']):
        return 'Dining'
    elif any(word in description for word in ['shopping', 'store', 'amazon', 'flipkart']):
        return 'Shopping'
    elif any(word in description for word in ['salary', 'income', 'pay']):
        return 'Salary'
    else:
        return 'Others'

def plot_expense_pie(df):
    expense_df = df[df['Type'] == 'Expense']
    if not expense_df.empty:
        fig1, ax1 = plt.subplots()
        expense_df.groupby('Category')['Amount'].sum().abs().plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax1)
        ax1.set_ylabel('')
        st.pyplot(fig1)

def plot_monthly_trends(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    monthly_summary = df.groupby(['Month', 'Type'])['Amount'].sum().unstack().fillna(0)
    if not monthly_summary.empty:
        fig2, ax2 = plt.subplots(figsize=(10,5))
        if 'Income' in monthly_summary.columns:
            monthly_summary['Income'].plot(ax=ax2, label='Income')
        if 'Expense' in monthly_summary.columns:
            monthly_summary['Expense'].abs().plot(ax=ax2, label='Expenses')
        ax2.legend()
        ax2.set_ylabel('Amount ($)')
        st.pyplot(fig2)

def generate_saving_tips(df):
    expense_df = df[df['Type'] == 'Expense']
    if not expense_df.empty:
        biggest_category = expense_df.groupby('Category')['Amount'].sum().abs().idxmax()
        st.markdown(f"- Your highest spending is on **{biggest_category}**. Consider setting a budget limit for this.")
        st.markdown(f"- Try to automate savings by transferring a portion of your income to a savings account as soon as you receive it.")
        st.markdown(f"- Review subscription services regularly to cancel unused ones.")
