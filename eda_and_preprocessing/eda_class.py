from utils.data_utils import get_entire_df

class EDA:
    def __init__(self):
        self.df = get_entire_df()

    def print_overview(self):
        print("\nDataset Overview:")
        print(self.df.info())
        print("\nSummary Statistics:")
        print(self.df.describe())
        print("\nMissing Values:")
        print(self.df.isnull().sum())

    def check_for_duplicates(self):
        print("\nNumber of Duplicates:", self.df.duplicated().sum())