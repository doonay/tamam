from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import Game
from config import user, password, host, port, db_name

def db_insert_batch(table_name, games):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        inspector = inspect(engine)
        if inspector.has_table(f'{table_name}_games'):
            Game.__table__.name = f'{table_name}_games'
            for game in games:
                existing_game = session.query(Game).filter_by(game_id=game['game_id']).first()
                if existing_game:
                    if existing_game.discounted_price != game['discounted_price'] and game['discounted_price'] != 0.0:
                        existing_game.base_price = game['base_price']
                        existing_game.discounted_price = game['discounted_price']
                        existing_game.discount = game['discount']
                    elif game['discounted_price'] == 0.0:
                        session.delete(existing_game)
                elif game['discounted_price'] == 0.0:
                    continue
                else:
                    new_game = Game(
                        game_id=game['game_id'],
                        title=game['title'],
                        platforms=game['platforms'],
                        base_price=game['base_price'],
                        discounted_price=game['discounted_price'],
                        discount=game['discount'],
                        img=game['img']
                    )
                    session.add(new_game)
                    
            session.commit()
            print('[INFO] Data inserted successfully.')
        else:
            print(f'[ERROR] Table {table_name}_games does not exist.')
    except Exception as ex:
        session.rollback()
        print('[INFO] Error while working with PostgreSQL:', ex)
    finally:
        session.close()