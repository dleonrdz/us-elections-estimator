import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

