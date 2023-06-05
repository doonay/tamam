from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import sessionmaker
from config import user, password, host, port, db_name

def show_tables():
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        for table_name in table_names:
            print(f'Table: {table_name}')
            columns = inspector.get_columns(table_name)
            for column in columns:
                print(f'\tColumn: {column["name"]}, Type: {column["type"]}')
            print('-------------------------')
    except Exception as ex:
        session.rollback()
        print('[INFO] Error while working with PostgreSQL:', ex)
    finally:
        session.close()

if __name__ == '__main__':
    show_tables()
    #Table: xbox_games
    #    Column: game_id, Type: VARCHAR
    #    Column: title, Type: VARCHAR
    #    Column: platforms, Type: ARRAY
    #    Column: base_price, Type: INTEGER
    #    Column: discounted_price, Type: INTEGER
    #    Column: discount, Type: SMALLINT
    #    Column: img, Type: VARCHAR
    #    Column: last_modified, Type: TIMESTAMP