import os
import pandas as pd
import numpy as np

def load_data(date_filter=None):
    # Define the root directory and the processed-folder path
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the current file
    processed_folder = os.path.join(root_dir, '..', 'data', 'processed')  # Path to processed data folder

    # List all Parquet files in the processed folder
    parquet_files = [f for f in os.listdir(processed_folder) if f.endswith('.parquet')]

    # Read all Parquet files and combine them into one DataFrame
    combined_df = pd.concat(
        [pd.read_parquet(os.path.join(processed_folder, parquet_file)) for parquet_file in parquet_files],
        ignore_index=True
    )

    # ----------- preprocessing ----------------
    # Ensure the 'BaseDateTime' column is in datetime format after combining all files
    combined_df['BaseDateTime'] = pd.to_datetime(combined_df['BaseDateTime'], errors='coerce')  # Coerce invalid parsing to NaT

    # Filter data by specific date if the date_filter is provided
    if date_filter:
        combined_df = combined_df[combined_df['BaseDateTime'].dt.date == pd.to_datetime(date_filter).date()]

    # Sort the dataframe by MMSI and BaseDateTime
    combined_df = combined_df.sort_values(by=['MMSI', 'BaseDateTime']).reset_index(drop=True)

    # Assign a random number to the 'Duration Anchored' column
    combined_df['Duration Anchored'] = np.random.uniform(0, 100, size=len(combined_df))  # Assign random numbers between 0 and 100

    return combined_df

# Example usage
load_data()
