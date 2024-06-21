import pandas as pd
from data_processing_utils import state_aggregation, official_results_processing, PROJECT_ROOT
import os

sentiment_df = pd.read_csv('data/processed/data.csv',
                           sep=';',
                           lineterminator='\n')
state_aggregation(sentiment_df, 'tracked_data_processed')
official_results_processing()




