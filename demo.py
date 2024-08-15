import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title = "Dashboard Loans Analysis",
    layout = 'wide'
)

st.title("Financial Insights Dashboard Loans Performance and Trends")

st.sidebar.header("Dashboard Filters and Features")

st.sidebar.markdown(
'''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
'''
)

loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] = loan['purpose'].str.replace("_", " ")
loan_date_count = loan.groupby('issue_date')['loan_amount'].count()
loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()
loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()
grade = loan['grade'].value_counts().sort_index()

with st.container(border = True):
    #membuat 2 kolom pada baris pertama
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Loans", f"{loan['id'].count() : ,.0f}", help = "Total Numbers of Loans")
        st.metric("Total Loans Amounts", f"${loan['loan_amount'].sum() :,.0f}", help = "Total of all loans amount")
    with col2:
        st.metric("Average Interest Rate", f"${loan['interest_rate'].mean() :,.0f}%", help = "Percetage Peminjam")
        st.metric("Average Interest Rate", f"${loan['loan_amount'].mean() :,.0f}", help = "Percentage interest rate")


with st.container(border = True):
    tab1, tab2, tab3 = st.tabs(["loans issued overtime", "loans date overtime", "loans date analysis"])
    with tab1:
        fig_line1 = px.line(
            loan_date_count,
            markers=True,
            title= "Number of Loans Issued Over Time",
            labels={
                'value':'Number of Loans',
                'issue_date':'Issue Date'
	            }
        ).update_layout(showlegend = False)
        st.plotly_chart(fig_line1, use_container_width=True)

    with tab2:
        fig_line2 = px.line(
            loan_date_sum,
            markers=True,
            title= "Number of Loans Amount Overtime",
            labels={
                'value':'Number of Loans',
                'issue_date':'Issue Date'
	            },
            template='seaborn'
        ).update_layout(showlegend = False)
        st.plotly_chart(fig_line2, use_container_width=True)

    with tab3:
        fig_bar1 =px.bar(
            loan_day_count,
            category_orders= {
                'issue_weekday' : ["Monday", "Tuesday", "Wednesday", 
                           "Thursday", "Friday", "Saturday", "Sunday"]
                }, #mengatur urutan kategori (hari) 
            title='Distribution of Loans by Day of the Week',
            labels={
                'value':'Number of Loans',
                'issue_weekday':'Day of the Week'
	            },
            template='seaborn'
        ).update_layout(showlegend = False) #menghilangkan legend pada dashboard
        st.plotly_chart(fig_bar1, use_container_width=True)

st.header("Loans Performance")
with st.container(border = True):
    with st.expander("Click here to Expand Visualization"):
        col3, col4 = st.columns(2)
        with col3:
            fig_pie = px.pie(
                loan,
                names= 'loan_condition',
                hole= 0.4,
                title= "Distribution of Loans by Condition",
                template='seaborn'
            ).update_layout()
            #st.plotly_chart(fig_pie, use_container_width=True)
            st.write(fig_pie) #dapat menggunakan sintax ini
        with col4:
            fig_bar2 = px.bar(
                grade,
                title= "Distribution of Loans by Grade",
                template='seaborn',
                labels={
                    'grade' : "Grade",
                    'value' : "Number of Loans"
                    }
            ).update_layout(showlegend = False)
            st.plotly_chart(fig_bar2, use_container_width=True)

st.header("Financial Analysis")
    
option = st.selectbox("Select loan condition", ["Good Loan", "Bad Loan"])
    
loan_condition = loan[loan['loan_condition'] == option]
with st.container(border = True):
        tab4, tab5 = st.tabs(["loans amount distribution", "loans date overtime"])
        with tab4:
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

        with tab5:
            fig_box =px.box(
                loan_condition,
                x = 'purpose',
                y = 'loan_amount',
                color= 'term',
                title="Loan Amount Distribution by Purpose",
                template='seaborn',
                labels={
                    'purpose':'Loan Purpose',
                    'loan_amount':'Loan Amount'
                }
            )
            st.plotly_chart(fig_box, use_container_width=True)

#st.subheader("Hello World")

#st.text_input()