import os
import pandas as pd
import numpy as np

def load_data(date_filter=None):
    """
    Load and preprocess vessel data with optimized anchored duration calculation.
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
    
    # ----------- Optimized Duration Anchored Calculation ----------------
    
    # Sort by MMSI and time for efficient groupby operations
    combined_df = combined_df.sort_values(by=['MMSI', 'BaseDateTime']).reset_index(drop=True)
    
    # Create a mask for anchored vessels (SOG == 0)
    is_anchored = combined_df['SOG'] == 0
    
    # Initialize duration column
    combined_df['Duration Anchored'] = pd.NA
    
    # Compute next timestamp for each MMSI group where vessel is anchored
    # This vectorized operation replaces the loop over each vessel's MMSI
    def calculate_anchored_duration(group):
        # Only calculate for anchored rows
        anchored = group[group['SOG'] == 0].copy()
        if len(anchored) > 0:
            # Calculate time to next observation
            anchored['Duration Anchored'] = anchored['BaseDateTime'].diff().shift(-1)
            return anchored[['Duration Anchored']]
        return pd.DataFrame(index=group.index)
    
    # Apply the function to each MMSI group
    duration_data = combined_df.groupby('MMSI').apply(calculate_anchored_duration)
    
    # Merge the duration data back to the main dataframe where indices match
    if not duration_data.empty:
        # Handle multi-index from groupby
        if isinstance(duration_data.index, pd.MultiIndex):
            duration_data = duration_data.reset_index(level=0, drop=True)
        
        # Update the main dataframe with calculated durations
        combined_df.update(duration_data)
    
    # Extract hour for trend analysis
    combined_df['Hour'] = combined_df['BaseDateTime'].dt.hour
    
    return combined_df