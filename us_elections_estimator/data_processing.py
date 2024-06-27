import pandas as pd
from data_processing_utils import state_aggregation, official_results_processing, raw_data_processing,PROJECT_ROOT
import os

print('Processing official data...')
raw_data_processing()
official_results_processing()

print('Processing estimation data...')
sentiment_df = pd.read_csv('data/processed/merged_tweets_with_predictions_v3.csv',
                           sep=',',
                           lineterminator='\n')

state_aggregation(sentiment_df, 'tracked_data_processed')

print('Processing done.')





