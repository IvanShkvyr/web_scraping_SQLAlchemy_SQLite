from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base




url = 'sqlite:///quotes_toscrape_com.db'

Base = declarative_base()

engine = create_engine(url, echo=True)

DBSession = sessionmaker(bind=engine)
session = DBSession()


# alembic init migration

# 
# sqlalchemy.url = sqlite:///quotes_toscrape_com.db

# alembic revision --autogenerate -m 'Init'

# alembic upgrade head

# scrapy startproject quotes_info

# scrapy genspider get_links quotes.toscrape.com