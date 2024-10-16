import pandas as pd
from utils.data_utils import get_entire_df

class Preprocessing:
    def __init__(self):
        self.df = get_entire_df()
        self.organizations_df = pd.DataFrame()
        self.locations_df = pd.DataFrame()
        self.industries_df = pd.DataFrame()
        self.industry_mapping_df = pd.DataFrame()
        self.investors_df = pd.DataFrame()
        self.investor_mapping_df = pd.DataFrame()
        self.ensure_data_consistency()
        self.process_all()

    def ensure_data_consistency(self):
        self.df['Transaction Name'] = self.df['Transaction Name'].astype(str)
        self.df['Transaction Name URL'] = self.df['Transaction Name URL'].astype(str)
        self.df['Organization Industries'] = self.df['Organization Industries'].astype(str)
        self.df['Lead Investors'] = self.df['Lead Investors'].astype(str)
        self.df['Investor Names'] = self.df['Investor Names'].astype(str)
        self.df['Money Raised'] = pd.to_numeric(self.df['Money Raised'], errors='coerce')
        self.df['Money Raised Currency'] = self.df['Money Raised Currency'].astype(str)
        self.df['Money Raised (in USD)'] = pd.to_numeric(self.df['Money Raised (in USD)'], errors='coerce')
        self.df['Funding Type'] = self.df['Funding Type'].astype(str)
        self.df['Announced Date'] = pd.to_datetime(self.df['Announced Date'], errors='coerce')
        self.df['Pre-Money Valuation'] = pd.to_numeric(self.df['Pre-Money Valuation'], errors='coerce')
        self.df['Pre-Money Valuation Currency'] = self.df['Pre-Money Valuation Currency'].astype(str)
        self.df['Pre-Money Valuation (in USD)'] = pd.to_numeric(self.df['Pre-Money Valuation (in USD)'], errors='coerce')
        self.df['Organization Name'] = self.df['Organization Name'].astype(str)
        self.df['Organization Name URL'] = self.df['Organization Name URL'].astype(str)
        self.df['Organization Location'] = self.df['Organization Location'].astype(str)
        self.df['Organization Description'] = self.df['Organization Description'].astype(str)
        self.df['Organization Website'] = self.df['Organization Website'].astype(str)
        self.df['Funding Stage'] = self.df['Funding Stage'].astype(str)
        self.df['Number of Funding Rounds'] = pd.to_numeric(self.df['Number of Funding Rounds'], errors='coerce')
        self.df['Total Funding Amount'] = pd.to_numeric(self.df['Total Funding Amount'], errors='coerce')
        self.df['Total Funding Amount Currency'] = self.df['Total Funding Amount Currency'].astype(str)
        self.df['Total Funding Amount (in USD)'] = pd.to_numeric(self.df['Total Funding Amount (in USD)'], errors='coerce')
        self.df['Equity Only Funding'] = self.df['Equity Only Funding'].apply(lambda x: True if x == 'Yes' else False)
        self.df['Equity Only Funding'] = self.df['Equity Only Funding'].astype(str)
        self.df['Funding Status'] = self.df['Funding Status'].astype(str)
        self.df['Number of Investors'] = pd.to_numeric(self.df['Number of Investors'], errors='coerce')

    def process_all(self):
        self.process_organizations()
        self.process_locations()
        self.process_industries()
        self.process_investors()

    def process_organizations(self):
        self.df['Organization Name'] = self.df['Transaction Name'].str.split('-').str[1].str.strip()
        self.organizations_df = self.df[['Organization Name', 'Organization Location', 'Organization Industries', 'Organization Website', 'Organization Name URL', 'Organization Description']].copy()
        self.organizations_df.drop_duplicates(subset='Organization Name', inplace=True)
        self.organizations_df['OrganizationID'] = self.organizations_df.index + 1
        self.organizations_df.reset_index(drop=True, inplace=True)
        self.df = self.df.merge(self.organizations_df[['Organization Name', 'OrganizationID']],
                                              left_on='Organization Name', right_on='Organization Name')
        self.df.drop(columns=['Organization Name', 'Organization Location', 'Organization Industries', 'Organization Website', 'Organization Name URL', 'Organization Description'], inplace=True)

    def process_locations(self):
        self.locations_df['Location'] = self.organizations_df['Organization Location']
        self.locations_df = self.locations_df.drop_duplicates().reset_index(drop=True)
        self.locations_df['LocationID'] = self.locations_df.index + 1
        
        self.organizations_df = pd.merge(self.organizations_df, self.locations_df, how='left', left_on='Organization Location', right_on='Location')
        self.organizations_df.drop(columns=['Location', 'Organization Location'], inplace=True)

        location_split = self.locations_df['Location'].str.split(',', expand=True)
        self.locations_df['City'] = location_split[0]
        self.locations_df['Region'] = location_split[1]
        self.locations_df['Country'] = location_split[2]
        self.locations_df['Continent'] = location_split[3]
        self.locations_df = self.locations_df.drop(columns=['Location'])

    def process_industries(self):
        industries_series = self.organizations_df['Organization Industries'].dropna().str.split(',').explode().str.strip()
        self.industries_df = pd.DataFrame(industries_series.unique(), columns=['Industry'])        
        self.industries_df['IndustryID'] = self.industries_df.index + 1

        industry_mapping = self.organizations_df[['OrganizationID', 'Organization Industries']].copy()
        industry_mapping = industry_mapping.dropna().set_index('OrganizationID')['Organization Industries'].str.split(',').explode().str.strip().reset_index()

        self.industry_mapping_df = industry_mapping.merge(self.industries_df, how='left', left_on='Organization Industries', right_on='Industry')
        self.industry_mapping_df = self.industry_mapping_df[['OrganizationID', 'IndustryID']]
        self.organizations_df.drop(columns=['Organization Industries'], inplace=True)

    def process_investors(self):
        self.df['TransactionID'] = self.df.index + 1

        investors_series = self.df['Investor Names'].dropna().str.split(',').explode().str.strip()
        self.investors_df = pd.DataFrame(investors_series.unique(), columns=['Investor'])
        self.investors_df['InvestorID'] = self.investors_df.index + 1

        investor_mapping = self.df[['TransactionID', 'Investor Names']].copy()
        investor_mapping = investor_mapping.dropna().set_index('TransactionID')['Investor Names'].str.split(',').explode().str.strip().reset_index()

        self.investor_mapping_df = investor_mapping.merge(self.investors_df, how='left', left_on='Investor Names', right_on='Investor')

        lead_investors_series = self.df['Lead Investors'].dropna().str.split(',').explode().str.strip()
        lead_investor_ids = self.investors_df[self.investors_df['Investor'].isin(lead_investors_series)]['InvestorID'].tolist()

        self.investor_mapping_df['IsLeadInvestor'] = self.investor_mapping_df['InvestorID'].apply(lambda x: x in lead_investor_ids)

        self.investor_mapping_df = self.investor_mapping_df[['TransactionID', 'InvestorID', 'IsLeadInvestor']]
        self.df.drop(columns=['Investor Names', 'Lead Investors'], inplace=True)