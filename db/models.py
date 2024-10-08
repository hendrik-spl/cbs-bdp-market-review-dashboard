from sqlalchemy import Column, Integer, String, Date, Float
from db_conn import Base

class Full_Record(Base):
    __tablename__ = 'full_records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_name = Column(String)
    transaction_name_url = Column(String)
    organization_industries = Column(String)
    lead_investors = Column(String)
    investor_names = Column(String)
    money_raised = Column(Float)
    money_raised_currency = Column(String)
    money_raised_in_usd = Column(Float)
    funding_type = Column(String)
    announced_date = Column(Date)
    pre_money_valuation = Column(Float)
    pre_money_valuation_currency = Column(String)
    pre_money_valuation_in_usd = Column(Float)
    organization_name = Column(String)
    organization_name_url = Column(String)
    organization_location = Column(String)
    organization_description = Column(String)
    organization_website = Column(String)
    funding_stage = Column(String)
    number_of_funding_rounds = Column(Integer)
    total_funding_amount = Column(Float)
    total_funding_amount_currency = Column(String)
    total_funding_amount_in_usd = Column(Float)
    equity_only_funding = Column(String)
    funding_status = Column(String)
    number_of_investors = Column(Float)