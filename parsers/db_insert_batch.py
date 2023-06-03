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
            existing_game = session.query(Game).filter_by(
                game_id=game['game_id']).first()
            if existing_game:  # игра существует в базе
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
                elif game['discounted_price'] == 0 or game['base_price'] == 0:
                    print(f"{game['game_id'], game['title']}")
                    print("В базе есть. Удаляем.")
                    print(
                        f"База:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.")
                    print(
                        f"Парсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                    session.delete(existing_game)
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

        # Проверка и удаление старых игр
        all_games = session.query(Game).all()
        for game in all_games:
            game_found = False
            for new_game in games:
                if game.game_id == new_game['game_id']:
                    game_found = True
                    break
            if not game_found:
                session.delete(game)

        session.commit()
        print('[INFO] Data inserted successfully.')

    except Exception as ex:
        session.rollback()
        print('[INFO] Error while working with PostgreSQL:', ex)
    finally:
        session.close()
