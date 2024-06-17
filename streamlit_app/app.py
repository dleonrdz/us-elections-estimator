import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

image_path = os.path.join(PROJECT_ROOT,"streamlit_app/images/usa_image.jpeg")
official_results_path = os.path.join(PROJECT_ROOT,"data/processed/official_results.csv")
col1, col2 = st.columns([1, 5])

with col1:
    st.image(image_path, width=150)

with col2:
    st.title("US Campaigns Tracker")

sentiment_data = {
    'state': ['Alabama', 'Alabama', 'Alaska', 'Alaska', 'Arizona', 'Arizona', 'Arkansas', 'Arkansas', 'California', 'California'],
    'state_code': ['AL', 'AL', 'AK', 'AK', 'AZ', 'AZ', 'AR', 'AR', 'CA', 'CA'],
    'preference': ['Republican', 'Democrat', 'Republican', 'Democrat', 'Republican', 'Democrat', 'Republican', 'Democrat', 'Republican', 'Democrat']
}

sentiment_df = pd.DataFrame(sentiment_data)

additional_sentiment_data = [
    {'state': 'California', 'state_code': 'CA', 'preference': 'Democrat'},
    {'state': 'California', 'state_code': 'CA', 'preference': 'Democrat'},
    {'state': 'Texas', 'state_code': 'TX', 'preference': 'Republican'},
    {'state': 'Texas', 'state_code': 'TX', 'preference': 'Republican'},
    {'state': 'Texas', 'state_code': 'TX', 'preference': 'Republican'},
    {'state': 'Texas', 'state_code': 'TX', 'preference': 'Democrat'}
]

additional_sentiment_df = pd.DataFrame(additional_sentiment_data)
sentiment_df = pd.concat([sentiment_df, additional_sentiment_df], ignore_index=True)

grouped_sentiment_df = sentiment_df.groupby(['state', 'state_code', 'preference']).size().reset_index(name='count')
pivot_sentiment_df = grouped_sentiment_df.pivot(index=['state', 'state_code'], columns='preference', values='count').reset_index().fillna(0)

if 'Republican' not in pivot_sentiment_df.columns:
    pivot_sentiment_df['Republican'] = 0
if 'Democrat' not in pivot_sentiment_df.columns:
    pivot_sentiment_df['Democrat'] = 0

pivot_sentiment_df['total'] = pivot_sentiment_df['Republican'] + pivot_sentiment_df['Democrat']
pivot_sentiment_df['preference_ratio'] = pivot_sentiment_df['Republican'] / pivot_sentiment_df['total']

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
        'text': 'Sentiment Tracker by State',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    margin={"r":0,"t":50,"l":0,"b":0},
    width=600,
    height=400
)

official_df = pd.read_csv(official_results_path)

# Create a grouped dataframe to count total votes by state for each candidate
grouped_official_df = official_df.groupby(['state', 'candidate'])['total_votes'].sum().unstack().reset_index().fillna(0)

if 'Republican' not in grouped_official_df.columns:
    grouped_official_df['Republican'] = 0
if 'Democrat' not in grouped_official_df.columns:
    grouped_official_df['Democrat'] = 0

grouped_official_df['total'] = grouped_official_df['Republican'] + grouped_official_df['Democrat']
grouped_official_df['preference_ratio'] = grouped_official_df['Republican'] / grouped_official_df['total']

state_codes = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO',
               'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
               'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
               'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
               'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
               'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
               'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
               'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
               'Wisconsin': 'WI', 'Wyoming': 'WY'}

grouped_official_df['state_code'] = grouped_official_df['state'].map(state_codes)

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

total_sentiment_republican = pivot_sentiment_df['Republican'].sum()
total_sentiment_democrat = pivot_sentiment_df['Democrat'].sum()

sentiment_pie_fig = go.Figure(data=[go.Pie(
    labels=['Republican', 'Democrat'],
    values=[total_sentiment_republican, total_sentiment_democrat],
    marker=dict(colors=['red', 'blue'])
)])
sentiment_pie_fig.update_layout(
    title='Overall Sentiment Preference',
    margin=dict(l=0, r=0, t=50, b=0)
)

total_official_republican = grouped_official_df['Republican'].sum()
total_official_democrat = grouped_official_df['Democrat'].sum()

official_pie_fig = go.Figure(data=[go.Pie(
    labels=['Republican', 'Democrat'],
    values=[total_official_republican, total_official_democrat],
    marker=dict(colors=['red', 'blue'])
)])
official_pie_fig.update_layout(
    title='Overall Official Results Preference',
    margin=dict(l=0, r=0, t=50, b=0)
)

pie_col1, pie_col2 = st.columns([1, 1])

with pie_col1:
    st.plotly_chart(sentiment_pie_fig)

with pie_col2:
    st.plotly_chart(official_pie_fig)

custom_tweet = st.text_input("Test your tweet!")

col1, col2, col3 = st.columns([1, 2, 1])

response = ''
with col2:
    if st.button("Get political preference"):
        response = 'Work in progress'

