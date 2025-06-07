# SQLAlchemy

__N.B:__ it is a standalone library and has no assocation with FastAPI, can be used with any other web framework

__N.B:__ SQLalchemy does not know how to talk to a database, it needs the databse driver (like pyscopg2).

## Engine

__The Engine is the starting point for any SQLAlchemy application.__
```bash
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://scott:tiger@localhost:5432/mydatabase")
```
The above engine creates a Dialect object tailored towards PostgreSQL, as well as a Pool object which will establish a DBAPI connection at localhost:5432 when a __connection request is first received.__ Note that the Engine and its underlying Pool do not establish the first actual DBAPI connection until the __Engine.connect()__ or __Engine.begin()__ methods are called.

![Logo](https://docs.sqlalchemy.org/en/20/_images/sqla_engine_arch.png)

__Dialect:__

In SQLAlchemy, a dialect is the system SQLAlchemy uses to communicate with different types of databases (e.g., PostgreSQL, MySQL, SQLite, Oracle, etc.). Each database has its own SQL syntax and behaviors. A dialect abstracts these differences, allowing SQLAlchemy to generate the correct SQL and handle database-specific nuances.

__Pool:__

A connection pool is a cache of database connections maintained so they can be reused when future requests to the database are required. Instead of creating a new connection every time (which is expensive), SQLAlchemy keeps a few connections open and hands them out as needed.

## Base

The purpose of declarative_base in SQLAlchemy is to provide a base class for your ORM (Object Relational Mapping) models. It enables the use of declarative syntax to define database tables as Python classes, combining table structure and Python behavior in one place.

```bash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'  # Name of the table in the DB

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```

## Session
In the most general sense, the Session establishes all conversations with the database and represents a “holding zone” for all the objects which you’ve loaded or associated with it during its lifespan. It provides the interface where SELECT and other queries are made that will return and modify ORM-mapped objects

The Session may be constructed on its own or by using the sessionmaker class. It typically is passed a single Engine as a source of connectivity up front.

The purpose of sessionmaker is to provide a factory for Session objects with a fixed configuration. As it is typical that an application will have an Engine object in module scope, the sessionmaker can provide a factory for Session objects that are constructed against this engine

```bash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# an Engine, which the Session will use for connection
# resources, typically in module scope
engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/")

# a sessionmaker(), also in the same scope as the engine
Session = sessionmaker(engine)

# we can now construct a Session() without needing to pass the
# engine each time
with Session() as session:
    session.add(some_object)
    session.add(some_other_object)
    session.commit()
# closes the session
```

Difference between session and sessionmaker
```bash
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

engine = create_engine("sqlite:///example.db")

# Must pass engine every time
session = Session(bind=engine)
```
using sessionmaker
```bash
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)  # Configured once

# Create sessions as needed
session1 = SessionLocal()
session2 = SessionLocal()
```

__N.B:__ If we chagne something in model, it will not be reflected on database, Sqlalchemy does not do that default


## Creating Session
```bash
# Everytime we get a database request, then we are making a session and after the request is done, the session is closed, this is why we are using generators
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
## Querying:

__Get all__
```bash
@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    var = db.query(your_model).all()
    return {"data":var}
```

__Create:__
```bash
@app.post("/createpost")
def create_post(post:Post,db:Session = Depends(get_db)):
    new_post =  models.Post(title=post.title,content=post.content) #create a new post
    db.add(new_post) #add it to our database
    db.commit() #commit()
    db.refresh(new_post) #stored back into the variable new_post
    return {"data":new_post} 
```
But if we have 30 or 50 fields, writing every fields manually will be tough, so what we can do is we can unpack the dictionary
```bash
**post.model_dump()
new_post =  models.Post(**post.model_dump()) 
```
