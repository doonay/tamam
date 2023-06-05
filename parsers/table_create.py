from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import sessionmaker
from models import Game
from config import user, password, host, port, db_name
from tamam_logger import tamam_logger, logger

@logger.catch
def create_table(table_name):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    Session = sessionmaker(bind=engine)
    session = Session()

    with Session() as session:
        try:
            #раскомментить, если надо проверять наличие существующей таблицы по-тихому
            #Game.__table__.create(bind=engine, checkfirst=True)
            Game.__table__.name = f'{table_name}_games'
            inspector = inspect(engine)
            if inspector.has_table(f'{table_name}_games'):
                tamam_logger('INFO', f'Table {table_name}_games already exist.')
            else:
                Game.__table__.create(bind=engine)
                tamam_logger('INFO', f'Table {table_name}_games created successfully.')
        except Exception:
            session.rollback()
        
if __name__ == '__main__':
    #create_table('xyz')
    import sys
    if len(sys.argv) == 2:
        create_table(sys.argv[1])
    else:
        print("Company name not specified. Please provide a company name when executing the script.")
        print("For example:")
        print("\tpython table_create_alchemy.py xbox")
        print("\tpython table_create_alchemy.py playstation")