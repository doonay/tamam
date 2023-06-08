from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, ProgrammingError

from models import create_game_class
from config import user, password, host, port, database
#from table_create import create_table
from tamam_logger import tamam_logger

#from models import create_game_class

def insert_logic(session, existing_game, new_game):
    if existing_game:# игра существует в базе
        # завезли обновленные ценники
        if existing_game.discounted_price != new_game.discounted_price and new_game.discounted_price != 0:
            tamam_logger("DEBUG", f"{new_game.product_id, new_game.title}. В базе есть. Обновляем ценник.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {new_game.base_price}, цена со скидкой: {new_game.discounted_price}, скидка:{new_game.discount}.")
            existing_game.base_price = new_game.base_price
            existing_game.discounted_price = new_game.discounted_price
            existing_game.discount = new_game.discount
            try:
                session.commit()
            except Exception as ex:
                tamam_logger("ERROR", f"{str(ex)}")
                session.rollback()
        # обновленные ценники нулевые
        elif new_game.discounted_price == 0 or new_game.base_price == 0:
            tamam_logger("DEBUG", f"{new_game.product_id, new_game.title}. В базе есть. Удаляем.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {new_game.base_price}, цена со скидкой:{new_game.discounted_price}, скидка:{new_game.discount}.")
            session.delete(existing_game)
            try:
                session.commit()
            except Exception as ex:
                tamam_logger("ERROR", f"{str(ex)}")
                session.rollback()
        # ценники такие же, как и раньше
        else:
            tamam_logger("DEBUG", f"{new_game.product_id, new_game.title}. В базе есть. Пропускаем.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {new_game.base_price}, цена со скидкой:{new_game.discounted_price}, скидка:{new_game.discount}.")
    else: # игры в базе нет
        if new_game.discounted_price == 0.0 or new_game.base_price == 0.0:
            tamam_logger("DEBUG", f"{new_game.product_id, new_game.title}. В базе нет. Пропускаем.\nБазовая цена: {new_game.base_price}, цена со скидкой:{new_game.discounted_price}, скидка:{new_game.discount}.")
        else:
            tamam_logger("DEBUG", f"{new_game.product_id, new_game.title}. В базе нет. Создаем.\nБазовая цена: {new_game.base_price}, цена со скидкой:{new_game.discounted_price}, скидка:{new_game.discount}.")
            session.add(new_game)
            try:
                session.commit()
            except Exception as ex:
                tamam_logger("ERROR", f"{str(ex)}")
                session.rollback()

# логика удаления старых игр
def clean_db_logic(session, Game, games_data_list):
    games_data_ids = []
    for game in games_data_list:
        games_data_ids.append(game['product_id'])
    existing_games_obj = session.query(Game).all()
    for existing_game_obj in existing_games_obj:
        if existing_game_obj.product_id not in [new_game['product_id'] for new_game in games_data_list]:
            session.delete(existing_game_obj)
        try:
            session.commit()
        except Exception as ex:
            tamam_logger("ERROR", f"{str(ex)}")
            session.rollback()
        #finally:
        #    session.close()
    tamam_logger("DEBUG", "Все неактуальные игры удалены успешно.")

def db_insert(table_name, games_data_list):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    Session = sessionmaker(bind=engine)
    session = Session()
    Game = create_game_class(f'{table_name}_games')
    try:
        Game.__table__.create(bind=engine)
        tamam_logger("DEBUG", f"Таблица {table_name}_games создана")
    except ProgrammingError as ex:
        tamam_logger("DEBUG", f"Таблица {table_name}_games в базе уже существует.")

    try:
        tamam_logger("DEBUG", "--функция добавления--")
        for game_data_dict in games_data_list:
            new_game = Game(**game_data_dict)
            existing_game = session.query(Game).filter_by(product_id=new_game.product_id).first()
            insert_logic(session, existing_game, new_game)
            #session.add(new_game)
        tamam_logger("DEBUG", "--функция удаления--")
        clean_db_logic(session, Game, games_data_list)
        session.commit()
    except Exception as ex:
        tamam_logger("ERROR", f"{str(ex)}")
        session.rollback()
    finally:
        session.close()

if __name__ == '__main__':
    '''
    games_data_list = [
        {
            'product_id': '4',
            'title': 'Game 4',
            'platforms': ['PC'],
            'base_price': 20,
            'discounted_price': 15,
            'discount': 25,
            'img': 'game4.jpg'
        },
        {
            'product_id': '3',
            'title': 'Game 3',
            'platforms': ['PC', 'PS4'],
            'base_price': 30,
            'discounted_price': 25,
            'discount': 20,
            'img': 'game3.jpg'
        }
    ]
    '''
    games_data_list = [
        {
            'product_id': '1',
            'title': 'Game 1',
            'platforms': ['PC'],
            'base_price': 30,
            'discounted_price': 10,
            'discount': 33,
            'img': 'game1.jpg'
        }
    ]
    
    table_name = 'x'    
    tamam_logger("DEBUG", "-----Начало программы-----")
    db_insert(table_name, games_data_list)
    tamam_logger("DEBUG", "--------------------------")