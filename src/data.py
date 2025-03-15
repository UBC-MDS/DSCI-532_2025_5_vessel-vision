
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

    # ----------- preprocessing for maximum time anchored computation ----------------
    # Ensure the 'BaseDateTime' column is in datetime format after combining all files
    combined_df['BaseDateTime'] = pd.to_datetime(combined_df['BaseDateTime'], errors='coerce')  # Coerce invalid parsing to NaT

    # Filter data by specific date if the date_filter is provided
    if date_filter:
        combined_df = combined_df[combined_df['BaseDateTime'].dt.date == pd.to_datetime(date_filter).date()]

    # Filter to keep only the three most famous ports
    famous_ports = [
        "Port of Los Angeles",
        "Port of San Francisco",
        "Port of Vancouver"
    ]
    combined_df = combined_df[combined_df['Nearest Port'].isin(famous_ports)]  # Assuming 'port' is the column name

    # Sort the dataframe by MMSI and BaseDateTime
    combined_df = combined_df.sort_values(by=['MMSI', 'BaseDateTime']).reset_index(drop=True)

    # Calculate the 'Duration Anchored' for each vessel (SOG == 0 means anchored)
    combined_df['Duration Anchored'] = np.nan  # Initialize an empty column for duration

    # Loop through each unique vessel
    # Calculate the duration for anchored vessels (SOG == 0)
    for mmsi in combined_df['MMSI'].unique():
        vessel_data = combined_df[combined_df['MMSI'] == mmsi]
        anchored_data = vessel_data[vessel_data['SOG'] == 0].copy()
        
        # Calculate the time difference for anchored rows
        anchored_data['Duration Anchored'] = anchored_data['BaseDateTime'].diff().shift(-1)
        
        # Update the original dataframe with the calculated duration
        combined_df.loc[anchored_data.index, 'Duration Anchored'] = anchored_data['Duration Anchored']
    
    return combined_df


load_data()
