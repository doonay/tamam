from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import sessionmaker
from models import Game
from config import user, password, host, port, db_name

def create_table(table_name):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        Game.__table__.name = f'{table_name}_games'
        #раскомментить, если надо проверять наличие существующей таблицы по-тихому
        #Game.__table__.create(bind=engine, checkfirst=True)
        inspector = inspect(engine)
        if inspector.has_table(f'{table_name}_games'):
            print(f'[INFO] Table {table_name}_games already exist.')
        else:
            Game.__table__.create(bind=engine)
            print(f'[INFO] Table {table_name}_games created successfully.')
            # Сброс автоинкрементного значения
            sequence_name = f'{table_name}_games_id_seq'
            engine.execute(f"SELECT setval('{sequence_name}', 1, false);")
            print(f'[INFO] Auto-increment sequence {sequence_name} reset.')
    except Exception as ex:
        session.rollback()
        print('[INFO] Error while working with PostgreSQL:', ex)
    finally:
        session.close()
        #print('[INFO] PostgreSQL connection closed')

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        create_table(sys.argv[1])
    else:
        print("Company name not specified. Please provide a company name when executing the script.")
        print("For example:")
        print("\tpython table_create_alchemy.py xbox")
        print("\tpython table_create_alchemy.py playstation")