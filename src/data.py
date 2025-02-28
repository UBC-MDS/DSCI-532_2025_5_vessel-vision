import os
import pandas as pd

def load_data():
    # Define the root directory and the split-file folder path
    root_dir = os.path.dirname(os.path.abspath(__file__))  # This gets the absolute path of the current file (app.py is in src)
    split_file_dir = os.path.join(root_dir, '..', 'data', 'split-data')  # Navigate to data/split-file folder

    # List all CSV files in the split-file folder
    csv_files = [f for f in os.listdir(split_file_dir) if f.endswith('.csv')]

    # Read all CSV files and combine them into one DataFrame
    combined_df = pd.concat(
        [pd.read_csv(os.path.join(split_file_dir, csv_file)) for csv_file in csv_files],
        ignore_index=True
    )


    return combined_df

load_data()

