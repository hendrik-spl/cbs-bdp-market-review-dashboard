from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.db_conn import Base

class FactFunding(Base):
    __tablename__ = 'fact_funding'
    
    transaction_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('dimension_organization.organization_id'))
    transaction_name = Column(String)
    transaction_name_url = Column(String)
    money_raised = Column(Float)
    money_raised_currency = Column(String)
    money_raised_usd = Column(Float)
    funding_type = Column(String)
    announced_date = Column(Date)
    pre_money_valuation = Column(Float)
    pre_money_valuation_currency = Column(String)
    pre_money_valuation_usd = Column(Float)
    funding_stage = Column(String)
    number_of_funding_rounds = Column(Integer)
    total_funding_amount = Column(Float)
    total_funding_currency = Column(String)
    total_funding_amount_usd = Column(Float)
    equity_only = Column(Boolean)
    funding_status = Column(String)
    number_of_investors = Column(Float)
    funding_amount_cluster = Column(Integer)
    money_raised_cluster = Column(Integer)
    transaction_cluster = Column(Integer)

    organization = relationship('DimensionOrganization', back_populates='fundings')
    investors = relationship('InvestorMapping', back_populates='funding')

class DimensionNews(Base):
    __tablename__ = 'dimension_news'
    
    news_id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('dimension_organization.organization_id'))
    uuid = Column(String, unique=True)
    title = Column(String)
    description = Column(String)
    keywords = Column(String)
    snippet = Column(String)
    url = Column(String)
    image_url = Column(String)
    language = Column(String)
    published_at = Column(Date)
    source = Column(String)
    categories = Column(String)

    organization = relationship('DimensionOrganization', back_populates='news')

class DimensionOrganization(Base):
    __tablename__ = 'dimension_organization'
    
    organization_id = Column(Integer, primary_key=True)
    organization_name = Column(String)
    organization_website = Column(String)
    organization_name_url = Column(String)
    organization_description = Column(String)
    location_id = Column(Integer, ForeignKey('dimension_location.location_id'))
    industry_cluster_id = Column(Integer, ForeignKey('dimension_industry_cluster.industry_cluster_id'))
    
    location = relationship('DimensionLocation', back_populates='organizations')
    fundings = relationship('FactFunding', back_populates='organization')
    industries = relationship('IndustryMapping', back_populates='organization')
    industry_cluster = relationship('DimensionIndustryCluster', back_populates='organizations')
    news = relationship('DimensionNews', back_populates='organization')

class DimensionLocation(Base):
    __tablename__ = 'dimension_location'
    
    location_id = Column(Integer, primary_key=True)
    city = Column(String)
    country_id = Column(Integer, ForeignKey('dimension_country.country_id'))
    longitude = Column(String)
    latitude = Column(String)

    organizations = relationship('DimensionOrganization', back_populates='location')
    country = relationship('DimensionCountry', back_populates='locations')

class DimensionIndustryCluster(Base):
    __tablename__ = 'dimension_industry_cluster'
    
    industry_cluster_id = Column(Integer, primary_key=True, autoincrement=True)
    industry_cluster = Column(String)

    organizations = relationship('DimensionOrganization', back_populates='industry_cluster')

class DimensionCountry(Base):
    __tablename__ = 'dimension_country'
    
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String)
    continent_id = Column(Integer, ForeignKey('dimension_continent.continent_id'))

    locations = relationship('DimensionLocation', back_populates='country')
    continent = relationship('DimensionContinent', back_populates='countries')

class DimensionContinent(Base):
    __tablename__ = 'dimension_continent'
    
    continent_id = Column(Integer, primary_key=True)
    continent_name = Column(String)
    
    countries = relationship('DimensionCountry', back_populates='continent')

class DimensionInvestor(Base):
    __tablename__ = 'dimension_investor'
    
    investor_id = Column(Integer, primary_key=True)
    investor = Column(String)
    
    investments = relationship('InvestorMapping', back_populates='investor')

class InvestorMapping(Base):
    __tablename__ = 'investor_mapping'
    
    transaction_id = Column(Integer, ForeignKey('fact_funding.transaction_id'), primary_key=True)
    investor_id = Column(Integer, ForeignKey('dimension_investor.investor_id'), primary_key=True)
    is_lead_investor = Column(Boolean)

    funding = relationship('FactFunding', back_populates='investors')
    investor = relationship('DimensionInvestor', back_populates='investments')

class DimensionIndustry(Base):
    __tablename__ = 'dimension_industry'
    
    industry_id = Column(Integer, primary_key=True)
    industry = Column(String)

    organizations = relationship('IndustryMapping', back_populates='industry')

class IndustryMapping(Base):
    __tablename__ = 'industry_mapping'
    
    organization_id = Column(Integer, ForeignKey('dimension_organization.organization_id'), primary_key=True)
    industry_id = Column(Integer, ForeignKey('dimension_industry.industry_id'), primary_key=True)

    organization = relationship('DimensionOrganization', back_populates='industries')
    industry = relationship('DimensionIndustry', back_populates='organizations')