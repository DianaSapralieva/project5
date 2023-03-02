from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Dtabase URL (Bad practice to put it here)
DATABASE_URL="postgresql://postgres:API@localhost/reddit_clone_ORM"

#Running engine for ORM translation (Python to SQL)
database_engine=create_engine(DATABASE_URL)
#tamplate for the connection 
SessionTamplete=sessionmaker(autocommit=False, autoflush=False, bind=database_engine)


#create and close session on demand
def get_db():
    db=SessionTamplete()
    try:
        yield db #yield is a poweful return it terurns a generator(indexed data) 
    finally:
        db.close()    
