import os
import pandas as pd
import numpy as np

def load_data(date_filter=None):
    # Define the root directory and the split-file folder path
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Absolute path of the current file
    split_file_dir = os.path.join(root_dir, '..', 'data', 'split-data')  # Path to the split-data folder

    # List all CSV files in the split-file folder
    csv_files = [f for f in os.listdir(split_file_dir) if f.endswith('.csv')]
    
    # Check for existing Parquet files, and if they don't exist, convert CSV to Parquet
    parquet_files = [f for f in os.listdir(split_file_dir) if f.endswith('.parquet')]
    
    if len(parquet_files) == 0:
        # Convert each CSV file to Parquet
        for csv_file in csv_files:
            csv_path = os.path.join(split_file_dir, csv_file)
            parquet_path = os.path.join(split_file_dir, f"{os.path.splitext(csv_file)[0]}.parquet")
            
            # Read CSV and write to Parquet
            df = pd.read_csv(csv_path, parse_dates=['BaseDateTime'])
            df.to_parquet(parquet_path, engine='pyarrow', compression='snappy')
            print(f"Converted {csv_file} to {parquet_path}")

    # Now read all the Parquet files and combine them into one DataFrame
    parquet_files = [f for f in os.listdir(split_file_dir) if f.endswith('.parquet')]

    # Read all Parquet files and combine them into one DataFrame
    combined_df = pd.concat(
        [pd.read_parquet(os.path.join(split_file_dir, parquet_file)) for parquet_file in parquet_files],
        ignore_index=True
    )

    # ----------- Preprocessing for maximum time anchored computation ----------------
    # Ensure the 'BaseDateTime' column is in datetime format after combining all files
    combined_df['BaseDateTime'] = pd.to_datetime(combined_df['BaseDateTime'], errors='coerce')

    # Filter data by specific date if the date_filter is provided
    if date_filter:
        combined_df = combined_df[combined_df['BaseDateTime'].dt.date == pd.to_datetime(date_filter).date()]

    # Filter the data to keep only rows where Status is 0 or 1
    combined_df = combined_df[combined_df['Status'].isin([0, 1])]

    # Sort the dataframe by MMSI and BaseDateTime
    combined_df = combined_df.sort_values(by=['MMSI', 'BaseDateTime']).reset_index(drop=True)

    # ----------- Find top 2 vessels per Nearest Port for Cargo and Passenger ----------------
    combined_df['visit_date'] = combined_df['BaseDateTime'].dt.date  # Extract date only

    # Count visits per day per MMSI, Nearest Port, and Vessel Type
    visit_counts = combined_df.groupby(['Nearest Port', 'visit_date', 'MMSI', 'Vessel Type Name']).size().reset_index(name='visit_count')

    # Find top 1 Cargo vessel and 1 Passenger vessel per Nearest Port
    top_vessels = visit_counts.groupby(['Nearest Port', 'Vessel Type Name']).apply(
        lambda x: x.sort_values('visit_count', ascending=False).head(1)
    ).reset_index(drop=True)

    # Get the list of top vessels (MMSI) for Cargo and Passenger types
    top_cargo_vessel_mmsis = top_vessels[top_vessels['Vessel Type Name'] == 'Cargo']['MMSI'].tolist()
    top_passenger_vessel_mmsis = top_vessels[top_vessels['Vessel Type Name'] == 'Passenger']['MMSI'].tolist()

    # ----------- Filter the data for the top vessels ----------------
    filtered_df = combined_df[
        combined_df['MMSI'].isin(top_cargo_vessel_mmsis + top_passenger_vessel_mmsis)
    ]

    # ----------- Calculate the 'Duration Anchored' for each vessel ----------------
    # Initialize 'Duration Anchored' as pd.NaT for time deltas
    filtered_df['Duration Anchored'] = pd.NaT  # Use pd.NaT for missing time values

    # Group by MMSI and calculate the difference for rows where Status is 1 (anchored)
    filtered_df['Duration Anchored'] = filtered_df.groupby('MMSI')['BaseDateTime'].diff().shift(-1)

    # Only keep the duration for rows where Status is 1 (anchored)
    filtered_df['Duration Anchored'] = np.where(filtered_df['Status'] == 1, filtered_df['Duration Anchored'], pd.NaT)

    # Return filtered dataframe
    return filtered_df

# Test the function
load_data()
