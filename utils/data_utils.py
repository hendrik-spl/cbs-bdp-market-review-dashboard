import os
import pandas as pd

def get_entire_df():
    data_folder = '../data'

    # Read the first file to get the column names
    first_file = os.path.join(data_folder, os.listdir(data_folder)[0])
    columns = pd.read_csv(first_file, nrows=0).columns

    # Read the first file completely and ensure that its first row is set as the column names
    df = pd.read_csv(first_file)

    # Read the remaining files while skipping the first row
    for filename in os.listdir(data_folder)[1:]:
        file_path = os.path.join(data_folder, filename)
        file_data = pd.read_csv(file_path, skiprows=1, names=columns)
        df = pd.concat([df, file_data], ignore_index=True)

    print(f"Created dataframe with shape: {df.shape}")
    return df