from sqlalchemy import create_engine
from urllib.parse import quote_plus

password = quote_plus('5Il9%00$jSdMYS')
database_url = f'mysql://root:{password}@localhost/internet_provider'
engine = create_engine(database_url)
