import numpy as np
import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
electoral_votes = os.path.join(PROJECT_ROOT,"data/raw/electoral_votes.csv")

state_codes = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO',
               'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
               'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
               'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
               'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
               'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
               'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
               'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
               'Wisconsin': 'WI', 'Wyoming': 'WY'}

electoral_votes_df = pd.read_csv(electoral_votes)
def raw_data_processing():
    raw_data_path = os.path.join(PROJECT_ROOT,"data/raw/president_county_candidate.csv")
    processed_data_path = os.path.join(PROJECT_ROOT,"data/processed/official_results.csv")

    df = pd.read_csv(raw_data_path)
    df_grouped = df.groupby(['state', 'candidate'], as_index= False).agg({'total_votes':'sum'})

    df_grouped = df_grouped[(df_grouped['candidate'].isin(['Joe Biden',
                                                           'Donald Trump']))]

    df_grouped['candidate'] = df_grouped['candidate'].str.replace('Joe Biden', 'Democrat')
    df_grouped['candidate'] = df_grouped['candidate'].str.replace('Donald Trump', 'Republican')

    df_grouped.to_csv(processed_data_path, index=False)

    print(df_grouped.head())

def state_aggregation(df, file_name):

    df['preference'] = np.where(df['target'] == 'democrat fan', 'Democrat', 'Republican')
    df['created_at'] = pd.to_datetime(df['created_at'])

    grouped_sentiment = df.copy()
    grouped_sentiment_df = grouped_sentiment.groupby(['state', 'state_code', 'preference']).size().reset_index(name='count')
    pivot_sentiment_df = grouped_sentiment_df.pivot(index=['state', 'state_code'], columns='preference',
                                                    values='count').reset_index().fillna(0)

    if 'Republican' not in pivot_sentiment_df.columns:
        pivot_sentiment_df['Republican'] = 0
    if 'Democrat' not in pivot_sentiment_df.columns:
        pivot_sentiment_df['Democrat'] = 0

    pivot_sentiment_df = pivot_sentiment_df.merge(electoral_votes_df[['state_code', 'Electoral Votes']],
                                                  how='left',
                                                  on='state_code')

    pivot_sentiment_df['Republican_electoral_votes'] = np\
        .where(pivot_sentiment_df['Republican'] > pivot_sentiment_df['Democrat'], pivot_sentiment_df['Electoral Votes'],0)

    pivot_sentiment_df['Democrat_electoral_votes'] = np \
        .where(pivot_sentiment_df['Republican'] < pivot_sentiment_df['Democrat'], pivot_sentiment_df['Electoral Votes'],
               0)

    pivot_sentiment_df['Winning'] = np \
        .where(pivot_sentiment_df['Republican'] < pivot_sentiment_df['Democrat'],
               'Democrat',
               'Republican')

    pivot_sentiment_df['preference_ratio'] = pivot_sentiment_df['Republican_electoral_votes'] / pivot_sentiment_df['Electoral Votes']

    key_states_df = electoral_votes_df.copy()
    key_states_df = key_states_df[(key_states_df['Tendency'] == 'Unknown')]
    key_states_df = key_states_df.merge(pivot_sentiment_df[['state_code', 'Winning']],
                                        how='left',
                                        on='state_code')

    engagement_tracking = df.copy()
    engagement_tracking = engagement_tracking.groupby(['preference'],
                                                      as_index=False).agg({'likes':'sum',
                                                                           'retweet_count':'sum'})

    time_series = df.copy()
    time_series['created_at'] = time_series['created_at'].dt.date
    grouped_time_series = time_series.groupby(['created_at', 'preference']).agg(
        {'likes': 'sum', 'retweet_count': 'sum', 'tweet':'count'}).reset_index()

    pivot_time_series = grouped_time_series.pivot(index='created_at', columns='preference', values=['likes', 'retweet_count', 'tweet'])

    pivot_time_series.columns = ['_'.join(col).strip() for col in pivot_time_series.columns.values]
    pivot_time_series = pivot_time_series.reset_index()


    path = os.path.join(PROJECT_ROOT,f"data/processed/{file_name}.csv")
    pivot_sentiment_df.to_csv(path, index=False)
    key_states_df.to_csv('data/processed/key_states_tracking.csv',index=False)
    engagement_tracking.to_csv('data/processed/engagement_tracking.csv',index=False)
    pivot_time_series.to_csv('data/processed/time_series_tracking.csv',index=False)

def official_results_processing():
    official_results_path = os.path.join(PROJECT_ROOT, "data/processed/official_results.csv")
    official_df = pd.read_csv(official_results_path)

    grouped_official_df = official_df.groupby(['state', 'candidate'])[
        'total_votes'].sum().unstack().reset_index().fillna(0)

    if 'Republican' not in grouped_official_df.columns:
        grouped_official_df['Republican'] = 0
    if 'Democrat' not in grouped_official_df.columns:
        grouped_official_df['Democrat'] = 0

    grouped_official_df['state_code'] = grouped_official_df['state'].map(state_codes)
    grouped_official_df = grouped_official_df.merge(electoral_votes_df[['state_code', 'Electoral Votes']],
                                                  how='left',
                                                  on='state_code')

    grouped_official_df['Republican_electoral_votes'] = np \
        .where(grouped_official_df['Republican'] > grouped_official_df['Democrat'], grouped_official_df['Electoral Votes'],
               0)

    grouped_official_df['Democrat_electoral_votes'] = np \
        .where(grouped_official_df['Republican'] < grouped_official_df['Democrat'], grouped_official_df['Electoral Votes'],
               0)

    grouped_official_df['preference_ratio'] = grouped_official_df['Republican_electoral_votes'] / grouped_official_df['Electoral Votes']


    path = os.path.join(PROJECT_ROOT, f"data/processed/official_results_grouped.csv")
    grouped_official_df.to_csv(path, index=False)



