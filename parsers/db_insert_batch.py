from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import Game
from config import user, password, host, port, db_name
from table_create import create_table


def db_insert_batch(table_name, games):
    engine = create_engine(
        f'postgresql://{user}:{password}@{host}:{port}/{db_name}?client_encoding=utf8')

    Session = sessionmaker(bind=engine)
    session = Session()

    inspector = inspect(engine)
    if not inspector.has_table(f'{table_name}_games'):
        # сначала создадим таблицу
        create_table(table_name)
    try:
        Game.__table__.name = f'{table_name}_games'
        for game in games:
            existing_game = session.query(Game).filter_by(game_id=game['game_id']).first()
            #Это был простой sql запрос SELECT * FROM Game WHERE game_id = <значение_game_id> LIMIT 1;
            #но в стиле sqlalchemy
            if existing_game:  # игра существует в базе
                # завезли обновленные ценники
                if existing_game.discounted_price != game['discounted_price'] and game['discounted_price'] != 0:
                    print(f"{game['game_id'], game['title']}")
                    print("В базе есть. Обновляем ценник.")
                    print(
                        f"База:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.")
                    print(
                        f"Парсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                    existing_game.base_price = game['base_price']
                    existing_game.discounted_price = game['discounted_price']
                    existing_game.discount = game['discount']
                # обновленные ценники нулевые
                elif game['discounted_price'] == 0 or game['base_price'] == 0:
                    print(f"{game['game_id'], game['title']}")
                    print("В базе есть. Удаляем.")
                    print(
                        f"База:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.")
                    print(
                        f"Парсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                    session.delete(existing_game)
                # ценники такие же, как и раньше
                else:
                    print(f"{game['game_id'], game['title']}")
                    print("В базе есть. Пропускаем.")
                    print(
                        f"База:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.")
                    print(
                        f"Парсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")                    
            else:  # игры в базе нет
                if game['discounted_price'] == 0.0 or game['base_price'] == 0.0:
                    print(f"{game['game_id'], game['title']}")
                    print("В базе нет. Пропускаем.")
                    print(
                        f"Базовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                    continue
                else:
                    print(f"{game['game_id'], game['title']}")
                    print("В базе нет. Создаем.")
                    print(
                        f"Базовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
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

        #session.commit() #удалить перед последним тестом!
        print('[INFO] All data inserted successfully.')
        # Проверка и удаление старых игр
        
        
        db_games = session.query(Game).all()
        for db_game in db_games:
            if db_game.game_id not in [game['game_id'] for game in games]:
                session.delete(db_game)

        session.commit()  # Фиксация изменений
        print('[INFO] All unused games have been deleted from the database.')


    except Exception as ex:
        session.rollback()
        print('[INFO] Error while working with PostgreSQL:', ex)
    finally:
        session.close()
