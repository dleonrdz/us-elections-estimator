import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from transformers import pipeline
import numpy as np

classifier = pipeline("text-classification", model="juliovp/distilbert_republican_democrat_tweets")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

image_path = os.path.join(PROJECT_ROOT,"streamlit_app/images/usa_image.jpeg")
#logo_path = os.path.join(PROJECT_ROOT,"streamlit_app/images/logo.jpg")
official_results_path = os.path.join(PROJECT_ROOT,"data/processed/official_results_grouped.csv")
tracked_data_path = os.path.join(PROJECT_ROOT,"data/processed/tracked_data_processed.csv")
key_states_path = os.path.join(PROJECT_ROOT,"data/processed/key_states_tracking.csv")
time_series_path = os.path.join(PROJECT_ROOT,"data/processed/time_series_tracking.csv")
engagement_path = os.path.join(PROJECT_ROOT,"data/processed/engagement_tracking.csv")
col1, col2 = st.columns([1, 5])

grouped_official_df = pd.read_csv(official_results_path)
pivot_sentiment_df = pd.read_csv(tracked_data_path)
key_states_df = pd.read_csv(key_states_path)
time_series_df = pd.read_csv(time_series_path)
engagement_df = pd.read_csv(engagement_path)


with col1:
    st.image(image_path, width=150)

with col2:
    st.title("US Campaigns Tracker")


# Sidebar with navigation instructions and estimation methodology
st.sidebar.title("How to Navigate")
#st.sidebar.image(logo_path, use_column_width=True)
st.sidebar.write("""
    Welcome to the US Campaigns Tracker! Here’s a quick guide to help you navigate through the app:

    - **GeoPreferences**: Visualize the distribution of electoral votes across different states, with detailed insights into the Key States Battle.
    - **Who's Winning?**: Compare the overall electoral votes each party has according to our sentiment estimation versus the official polls.
    - **Tweets Wars**: Track the engagement metrics over time to see which party generates more buzz on social media.
    - **Tweet-o-Meter**: Analyze the political inclination of your custom tweet and see how it aligns with current sentiment.

    Each section provides insights into the current political landscape, helping you understand trends and sentiments across the nation.

    ### Estimation Methodology
    Our estimations are derived from a fine-tuned version of DistilBERT, applied to Twitter (now X) data focusing on political tweets. 
    The model analyzes the sentiment of each tweet and categorizes support based on the political figure or party the tweet references.
""")

#st.sidebar.image(logo_path, use_column_width=True)

st.markdown("""
    <h2 style="text-align: center; font-family: 'Source Sans Pro', sans-serif; font-weight: bold;">
        <span style="color: blue;">Democrats</span> vs 
        <span style="color: red;">Republicans</span>
    </h2>
    """, unsafe_allow_html=True)

st.markdown("""
    <h2 style="text-align: center; font-family: 'Source Sans Pro', sans-serif; font-weight: bold;">
        GeoPreferences    
    </h2>
    """, unsafe_allow_html=True)

sentiment_fig = px.choropleth(
    pivot_sentiment_df,
    locations='state_code',
    locationmode="USA-states",
    color='preference_ratio',
    color_continuous_scale=[
        (0.0, "blue"),
        (0.5, "white"),
        (1.0, "red")
    ],
    scope="usa",
    labels={'preference_ratio': 'Republican Preference Ratio'},
)
sentiment_fig.update_layout(coloraxis_showscale=False)
sentiment_fig.update_layout(
    title={
        'text': 'Estimation by State',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    margin={"r":0,"t":50,"l":0,"b":0},
    width=600,
    height=400
)

# Create the official results map
official_fig = px.choropleth(
    grouped_official_df,
    locations='state_code',
    locationmode="USA-states",
    color='preference_ratio',
    color_continuous_scale=[
        (0.0, "blue"),
        (0.5, "white"),
        (1.0, "red")
    ],
    scope="usa",
    labels={'preference_ratio': 'Republican Preference Ratio'},
)
official_fig.update_layout(coloraxis_showscale=False)
official_fig.update_layout(
    title={
        'text': 'Official Polls by State',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    margin={"r":0,"t":50,"l":0,"b":0},
    width=600,
    height=400
)


map_col1, map_col2 = st.columns([1, 1])

with map_col1:
    st.plotly_chart(sentiment_fig)

with map_col2:
    st.plotly_chart(official_fig)

# Sort key states dataframe by Electoral Votes in descending order
key_states_df_sorted = key_states_df.sort_values(by='Electoral Votes', ascending=False)

# Create the bar plot for key states
colors = {'Republican': 'red', 'Democrat': 'blue'}
key_states_fig = px.bar(
    key_states_df_sorted,
    x='state_code',
    y='Electoral Votes',
    color='Winning',
    color_discrete_map=colors,
    title='The Key States Battle'
)

# Update the layout to ensure the bars are ordered by Electoral Votes regardless of color
key_states_fig.update_layout(
    showlegend=False,
    title={
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    margin={"r":0,"t":50,"l":0,"b":0},
    width=1200,
    height=400,
    xaxis={'categoryorder': 'total descending', 'title':'State'}
)

# Display the bar plot below the maps
st.plotly_chart(key_states_fig)

st.markdown("""
    <h2 style="text-align: center; font-family: 'Source Sans Pro', sans-serif; font-weight: bold;">
        Who’s Winning?   
    </h2>
    """, unsafe_allow_html=True)

total_sentiment_republican = pivot_sentiment_df['Republican_electoral_votes'].sum()
total_sentiment_democrat = pivot_sentiment_df['Democrat_electoral_votes'].sum()

# Create bar chart for sentiment
sentiment_bar_fig = go.Figure(data=[go.Bar(
    x=['Democrat', 'Republican'],
    y=[total_sentiment_democrat,total_sentiment_republican],
    marker_color=['blue','red'],
    text=[total_sentiment_democrat,total_sentiment_republican],
    textposition='auto'
)])
sentiment_bar_fig.update_layout(
    title='Electoral Votes Estimation',
    xaxis_title='',
    yaxis_title='Total Electoral Votes',
    margin=dict(l=0, r=0, t=50, b=0)
)
sentiment_bar_fig.update_traces(texttemplate='%{text:.0f}')

# Calculate overall preference for official results
total_official_republican = grouped_official_df['Republican_electoral_votes'].sum()
total_official_democrat = grouped_official_df['Democrat_electoral_votes'].sum()

# Create bar chart for official results
official_bar_fig = go.Figure(data=[go.Bar(
    x=['Democrat','Republican'],
    y=[total_official_democrat,total_official_republican],
    marker_color=['blue','red'],
    text=[total_official_democrat,total_official_republican],
    textposition='auto'
)])
official_bar_fig.update_layout(
    title='Official Electoral Votes Count',
    xaxis_title='',
    yaxis_title='Total Electoral Votes',
    margin=dict(l=0, r=0, t=50, b=0)
)
official_bar_fig.update_traces(texttemplate='%{text:.0f}')

# Create two columns for the bar charts
bar_col1, bar_col2 = st.columns([1, 1])

with bar_col1:
    st.plotly_chart(sentiment_bar_fig)

with bar_col2:
    st.plotly_chart(official_bar_fig)

st.markdown("""
    <h2 style="text-align: center; font-family: 'Source Sans Pro', sans-serif; font-weight: bold;">
        Tweets Wars  
    </h2>
    """, unsafe_allow_html=True)

time_series_fig = px.line(
    time_series_df,
    x='created_at',
    y=['tweet_Democrat', 'tweet_Republican'],
    title='Twitter Activity Evolution',
    labels={'created_at': 'Date', 'value': 'Number of Tweets'},
    color_discrete_map={
        'tweet_Democrat': 'blue',
        'tweet_Republican': 'red'
    }
)
time_series_fig.update_layout(
    showlegend=False,
    title={
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    margin={"r":0,"t":50,"l":0,"b":0},
    xaxis_title='Date',
    yaxis_title='Number of Tweets'
)

# Display the time series plot below the bar charts and above the tweet test section
st.plotly_chart(time_series_fig)

# Create bar charts for engagement metrics
likes_bar_fig = go.Figure(data=[go.Bar(
    x=engagement_df['preference'],
    y=engagement_df['likes'],
    marker_color=['blue', 'red'],
    text=engagement_df['likes'],
    textposition='auto'
)])
likes_bar_fig.update_layout(
    title='Total Likes',
    xaxis_title='',
    yaxis_title='Total Likes',
    margin=dict(l=0, r=0, t=50, b=0)
)
likes_bar_fig.update_traces(texttemplate='%{text:,.0f}')

retweets_bar_fig = go.Figure(data=[go.Bar(
    x=engagement_df['preference'],
    y=engagement_df['retweet_count'],
    marker_color=['blue', 'red'],
    text=engagement_df['retweet_count'],
    textposition='auto'
)])
retweets_bar_fig.update_layout(
    title='Total Retweets',
    xaxis_title='',
    yaxis_title='Total Retweets',
    margin=dict(l=0, r=0, t=50, b=0)
)
retweets_bar_fig.update_traces(texttemplate='%{text:,.0f}')

# Create two columns for the engagement bar charts
engagement_col1, engagement_col2 = st.columns([1, 1])

with engagement_col1:
    st.plotly_chart(likes_bar_fig)

with engagement_col2:
    st.plotly_chart(retweets_bar_fig)

st.markdown("""
    <h2 style="text-align: center; font-family: 'Source Sans Pro', sans-serif; font-weight: bold;">
        Tweet-o-Meter 
    </h2>
    """, unsafe_allow_html=True)
custom_tweet = st.text_input("Test your tweet!")

col1, col2, col3 = st.columns([1, 2, 1])

response = ''
with col2:
    if st.button("Get political preference"):
        response = classifier(custom_tweet)[0]['label']
        st.write(f"You are a **{response}!!!**")

