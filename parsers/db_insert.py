from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import Game
from config import user, password, host, port, db_name
from table_create import create_table
from tamam_logger import tamam_logger, logger

@logger.catch
def db_insert_batch(table_name, games):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

    Session = sessionmaker(bind=engine)
    session = Session()

    inspector = inspect(engine)
    if not inspector.has_table(f'{table_name}_games'):
        # сначала создадим таблицу
        create_table(table_name)
    try:
        Game.__table__.name = f'{table_name}_games'
        for game in games:
            existing_game = session.query(Game).filter_by(product_id=game['product_id']).first()
            if existing_game: # игра существует в базе
                # завезли обновленные ценники
                if existing_game.discounted_price != game['discounted_price'] and game['discounted_price'] != 0:
                    tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе есть. Обновляем ценник.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                    existing_game.base_price = game['base_price']
                    existing_game.discounted_price = game['discounted_price']
                    existing_game.discount = game['discount']
                # обновленные ценники нулевые
                elif game['discounted_price'] == 0 or game['base_price'] == 0:
                    tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе есть. Удаляем.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                    session.delete(existing_game)
                # ценники такие же, как и раньше
                else:
                    tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе есть. Пропускаем.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                    continue
            else:  # игры в базе нет
                if game['discounted_price'] == 0.0 or game['base_price'] == 0.0:
                    tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе нет. Пропускаем.\nБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                    continue
                else:
                    tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе нет. Создаем.\nБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                    new_game = Game(
                        product_id=game['product_id'],
                        title=game['title'],
                        platforms=game['platforms'],
                        base_price=game['base_price'],
                        discounted_price=game['discounted_price'],
                        discount=game['discount'],
                        img=game['img']
                    )
                    session.add(new_game)

        tamam_logger("INFO", "All data inserted successfully.")
        # Проверка и удаление старых игр
        db_games = session.query(Game).all()
        for db_game in db_games:
            if db_game.product_id not in [game['product_id'] for game in games]:
                session.delete(db_game)
                tamam_logger("INFO", "All unused games have been deleted from the database.")

        session.commit()  # Фиксация изменений

    except Exception as _ex:
        session.rollback()
        # декоратор и так должен перехватывать эту ошибку детально
        #logger("ERROR", f"Error while working with PostgreSQL: {_ex}")
    finally:
        session.close()

if __name__ == '__main__':
    test_data = [
        {
            "product_id": "TEST",
            "title": "The Walking Test",
            "platforms": ["XBOX"],
            "base_price": 1998,
            "discounted_price": 13,
            "discount": 99,
            "img": "https://store-image"
        }
    ]

    db_insert_batch('xbox', test_data)