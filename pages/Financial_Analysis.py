import streamlit as st
import pandas as pd
import plotly.express as px

loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] = loan['purpose'].str.replace("_", " ")
loan_date_count = loan.groupby('issue_date')['loan_amount'].count()
loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()
loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()
grade = loan['grade'].value_counts().sort_index()

option = st.selectbox("Select loan condition", ["Good Loan", "Bad Loan"])
    
loan_condition = loan[loan['loan_condition'] == option]
fig_hist = px.histogram(
                loan_condition,
                x= 'loan_amount',
                color = 'term', # kolom di dtaframe untuk menentukan perbedaan warna
                #template = 'ggplot2',
                nbins = 20,
                title='Loan Amount Distribution by condition',
                labels={
                    'loan_amount':'Loan Amount',
                    'term':'Loan Term'},
                template = 'seaborn'
            )
st.plotly_chart(fig_hist, use_container_width=True)