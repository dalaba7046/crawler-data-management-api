from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging
logger = logging.getLogger()
flag = load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL and flag:
  DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_DATA_USER')}:{os.getenv('MYSQL_DATA_PASSWORD')}@{os.getenv('MYSQL_DATA_HOST')}:{os.getenv('MYSQL_DATA_PORT')}/{os.getenv('MYSQL_DATA_DATABASE')}"

if DATABASE_URL:
  logger.info("Database setting success")
else:
  raise ValueError("Database setting failed")

# create SQL engine
engine = create_engine(DATABASE_URL, echo=True)

# create SQL communication session and bind
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create SQL mapping table
Base = declarative_base()
