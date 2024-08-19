from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.sql_model import BASE

db_user = 'postgres'
db_password = 'postgres'
db_port = 5432
db_host = 'localhost'

uri: str = F'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/CoderVai'

engine = create_engine(uri)

BASE.metadata.create_all(bind=engine)
print("Tables created successfully")

# Create a session factory bound to the engine
Session = sessionmaker(bind=engine, autoflush=True)

# Create an instance of the session
db_session = Session()

try: 
    connection = engine.connect()
    connection.close()
    print('Connection to the database was successful')
except Exception as e:
    print('Connection to the database was not successful')
    print(e)
