import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import random
import time 
import os
from datetime import datetime, timedelta
from streamlit_extras.let_it_rain import rain
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(layout = 'centered')

path = os.path.dirname(os.path.abspath(__file__))

with open(path+'/static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

keboola_logo = path+'/static/logo.png'
logo_html = f'<div style="display: flex; justify-content: flex-end;"><img src="data:image/png;base64,{base64.b64encode(open(keboola_logo, "rb").read()).decode()}" style="width: 200px; margin-bottom: 10px;"></div>'
st.markdown(f"{logo_html}", unsafe_allow_html=True)

st.title("This is not giving apple vibes, i'm sorry:,(")

# Generate dummy dataset
random.seed(42)
error_types = ["Connection Error", "Data Parsing Error", "Server Timeout", "Authentication Failure", "Data Validation Error"]
explanations = [
    "The error occurred due to a connection issue with the server.",
    "Data parsing failed because of unexpected format.",
    "The server timed out while processing the request.",
    "Authentication credentials provided were incorrect.",
    "Data validation failed due to missing or invalid fields."
]

data = []
for _ in range(50):
    error = random.choice(error_types)
    explanation = random.choice(explanations)
    rating = random.choice(["Good", "Bad", "Cancel"])
    date = datetime(2024, 5, random.randint(2, 9))  # Random date between May 2 and May 9, 2024
    data.append([error, explanation, rating, date])

df = pd.DataFrame(data, columns=["Error", "Explanation", "Rating", "Date"])

good_df = df[df['Rating'] == 'Good']
bad_df = df[df['Rating'] == 'Bad']
cancel_df = df[df['Rating'] == 'Cancel']

# Date
current_date = datetime.now()
one_week_ago = current_date - timedelta(weeks=1)

current_date_str = current_date.strftime("%B %d, %Y")
one_week_ago_str = one_week_ago.strftime("%B %d, %Y")

caption = f"_The last evaluation was conducted on {one_week_ago_str}._"

# Tabs 
tab1, tab2, tab3, tab4 = st.tabs(['Main', 'Good', 'Bad', 'Cancel'])

with tab1:
    st.caption(caption)
    st.markdown("###")

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container():
            good = f"{good_df.shape[0]}/50"
            st.markdown(f'<p class="green_text"><br><br><br>Good</p><p class="details"><br>{good}</p>', unsafe_allow_html = True)
            st.write('<span class="frame"/>', unsafe_allow_html=True)
    with col2:
        with st.container():
            bad = f"{bad_df.shape[0]}/50"
            st.markdown(f'<p class="red_text"><br><br><br>Bad</p><p class="details"><br>{bad}</p>', unsafe_allow_html = True)
            st.write('<span class="frame"/>', unsafe_allow_html=True)

    with col3:
        with st.container():
            cancel = f"{cancel_df.shape[0]}/50"
            st.markdown(f'<p class="yellow_text"><br><br><br>Cancel</p><p class="details"><br>{cancel}</p>', unsafe_allow_html = True)
            st.write('<span class="frame"/>', unsafe_allow_html=True)

    # Plot
    df['Date'] = pd.to_datetime(df['Date'])
    df_grouped = df.groupby(['Date', 'Rating']).size().reset_index(name='Count')

    fig = px.bar(df_grouped, x='Date', y='Count', color='Rating', title='Rating Count Over Time',
            color_discrete_map={"Good": "#4CAF50", "Bad": "#F44336", "Cancel": "#FFC107"})

    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.dataframe(df, use_container_width=True, hide_index=True)
    
with tab2:
    st.caption(caption)
    st.markdown("###")

    good_df['Select'] = False
    good_df['Comment'] = ''

    st.data_editor(good_df, column_order=('Select', 'Comment', 'Error', 'Explanation', 'Rating', 'Date'), 
                   use_container_width=True, 
                   hide_index=True)

    btn = st.button("Save to Keboola")
    if btn:
        with st.spinner("Saving the Earth"):
            time.sleep(3)

            st.success("Done!")