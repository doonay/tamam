import sys
from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import sessionmaker
from models import Game
from config import db_name, user, password, host, port

def drop_table(platform_name):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        Game.__table__.name = f'{platform_name}_games'
        inspector = inspect(engine)
        if inspector.has_table(f'{platform_name}_games'):
            Game.__table__.drop(bind=engine)
            print(f"[INFO] Table {platform_name}_games dropped successfully.")
        else:
            print(f"[INFO] Table {platform_name}_games does not exist.")
    except Exception as ex:
        session.rollback()
        print("[INFO] Error while working with PostgreSQL:", ex)
    finally:
        session.close()
        #print("[INFO] PostgreSQL connection closed")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        drop_table(sys.argv[1])
    else:
        print("Company name not specified. Please provide a company name when executing the script.")
        print("For example:")
        print("\tpython table_delete_alchemy.py xbox")
        print("\tpython table_delete_alchemy.py playstation")
