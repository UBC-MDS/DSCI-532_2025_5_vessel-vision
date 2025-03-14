import os
import pandas as pd
import numpy as np

def load_data(date_filter=None):
    """
    Load and preprocess vessel data with completely vectorized anchored duration calculation.
    """
    # Define the root directory and the split-file folder path
    root_dir = os.path.dirname(os.path.abspath(__file__))
    split_file_dir = os.path.join(root_dir, '..', 'data', 'split-data')
    
    # List all CSV files in the split-file folder
    csv_files = [f for f in os.listdir(split_file_dir) if f.endswith('.csv')]
    
    # Read all CSV files and combine them into one DataFrame
    combined_df = pd.concat(
        [pd.read_csv(os.path.join(split_file_dir, csv_file)) for csv_file in csv_files],
        ignore_index=True
    )
    
    # Ensure the 'BaseDateTime' is in datetime format
    combined_df['BaseDateTime'] = pd.to_datetime(combined_df['BaseDateTime'], errors='coerce')
    
    # Filter data by specific date if the date_filter is provided
    if date_filter:
        combined_df = combined_df[combined_df['BaseDateTime'].dt.date == pd.to_datetime(date_filter).date()]
    
    # ----------- Vectorized Duration Anchored Calculation ----------------
    
    # Sort by MMSI and time for consistent results
    combined_df = combined_df.sort_values(by=['MMSI', 'BaseDateTime']).reset_index(drop=True)
    
    # Initialize Duration Anchored column
    combined_df['Duration Anchored'] = pd.NA
    
    # Create a mask for anchored vessels (SOG == 0)
    anchored_mask = combined_df['SOG'] == 0
    
    # Create MMSI groups for vectorized operations
    combined_df['mmsi_group'] = (combined_df['MMSI'] != combined_df['MMSI'].shift()).cumsum()
    
    # Calculate the time difference between consecutive timestamps for the same vessel
    combined_df['time_diff'] = combined_df.groupby('MMSI')['BaseDateTime'].diff().shift(-1)
    
    # Only assign duration where vessel is anchored (SOG == 0)
    combined_df.loc[anchored_mask, 'Duration Anchored'] = combined_df.loc[anchored_mask, 'time_diff']
    
    # Drop the temporary columns we created
    combined_df = combined_df.drop(columns=['mmsi_group', 'time_diff'])
    
    # Extract hour for trend analysis
    combined_df['Hour'] = combined_df['BaseDateTime'].dt.hour
    
    return combined_df