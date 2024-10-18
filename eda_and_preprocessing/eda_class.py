import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    def check_distributions(self):
        """Check the distribution of numeric columns with larger x-axis labels."""
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        self.df[numeric_cols].hist(figsize=(15, 10), bins=40)
        
        # Set larger font size for x and y ticks
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
        plt.suptitle('Distribution of Numeric Columns', fontsize=16)
        plt.tight_layout()
        plt.show()

    def plot_boxplots(self):
        """Plot box plots to visualize outliers in numeric columns."""
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        plt.figure(figsize=(15, 10))
        for i, col in enumerate(numeric_cols, 1):
            plt.subplot(len(numeric_cols) // 2 + 1, 2, i)
            sns.boxplot(x=self.df[col])
            plt.title(f'Boxplot of {col}')
        plt.tight_layout()
        plt.show()

    def check_for_outliers(self):
        """Check for outliers using IQR method."""
        print(f"Number of Outliers according to the IQR Method.")
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[(self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))]
            print(f"\nNumber of outliers in {col}: {len(outliers)}")

    def correlation_matrix(self):
        """Plot correlation matrix of numeric columns."""
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        corr_matrix = self.df[numeric_cols].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix of Numeric Columns')
        plt.show()

    def run_eda(self):
        """Run the complete EDA process."""
        self.print_overview()
        self.check_for_duplicates()
        self.check_distributions()
        self.plot_boxplots()
        self.check_for_outliers()
        self.correlation_matrix()
