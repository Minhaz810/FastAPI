from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Connection String Format
FORMAT = 'postgresql://<username>:<password>@<ip-address/<hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:pgadmin@localhost/fastapi_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

# Everytime we get a database request, then we are making a session and after the request is done, the session is closed, this is why we are using generators
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
