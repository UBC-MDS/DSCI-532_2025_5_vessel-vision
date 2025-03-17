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
    
    # Sort by MMSI and time
    combined_df = combined_df.sort_values(by=['MMSI', 'BaseDateTime']).reset_index(drop=True)
    
    # Initialize Duration Anchored column
    combined_df['Duration Anchored'] = pd.NA
    
    # Extract only anchored vessels (SOG == 0)
    anchored_df = combined_df[combined_df['SOG'] == 0].copy()
    
    if not anchored_df.empty:
        # Sort anchored data by MMSI and time
        anchored_df = anchored_df.sort_values(by=['MMSI', 'BaseDateTime'])
        
        # Calculate time to next anchored observation for same vessel
        # This replicates the original loop behavior but in a vectorized way
        anchored_df['next_time'] = anchored_df.groupby('MMSI')['BaseDateTime'].shift(-1)
        anchored_df['Duration Anchored'] = anchored_df['next_time'] - anchored_df['BaseDateTime']
        
        # Create a mapping to update the original dataframe
        # We need to create a unique identifier combining MMSI and timestamp
        anchored_df['mmsi_time_key'] = anchored_df['MMSI'].astype(str) + '_' + anchored_df['BaseDateTime'].astype(str)
        combined_df['mmsi_time_key'] = combined_df['MMSI'].astype(str) + '_' + combined_df['BaseDateTime'].astype(str)
        
        # Create a dictionary mapping of keys to Duration Anchored values
        duration_dict = anchored_df.set_index('mmsi_time_key')['Duration Anchored'].to_dict()
        
        # Update only the relevant rows in the original dataframe
        combined_df['Duration Anchored'] = combined_df['mmsi_time_key'].map(duration_dict)
        
        # Remove the temporary key column
        combined_df = combined_df.drop(columns=['mmsi_time_key'])
    
    # Extract hour for trend analysis
    combined_df['Hour'] = combined_df['BaseDateTime'].dt.hour
    
    return combined_df
