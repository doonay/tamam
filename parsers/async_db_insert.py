from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Game
from config import user, password, host, port, db_name
from table_create import create_table
from tamam_logger import tamam_logger, logger
import asyncio
import logging
from sqlalchemy import create_engine, inspect

@logger.catch
async def async_db_insert(table_name, games):
    engine = create_async_engine(f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}', echo=True)
    async with AsyncSession(engine) as session:
        async with session.begin():
            for item in games:
                Game.__table__.name = f'{table_name}_games'
                new_game = Game(
                    product_id=item['product_id'],
                    title=item['title'],
                    platforms=item['platforms'],
                    base_price=item['base_price'],
                    discounted_price=item['discounted_price'],
                    discount=item['discount'],
                    img=item['img']
                )
                session.add(new_game)
        await session.commit()
        tamam_logger("INFO", f"{len(games)} games successfully added to database")

def sync_main(table_name, games):
    #------------работаем синхронно--------
    # Переводим логгер SQLAlchemy в режим WARNING, что бы не видеть в консоли сообщения уровня INFO
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    # Если таблицы нет, сначала создадим таблицу
    inspector = inspect(engine)
    if not inspector.has_table(f'{table_name}_games'):
        create_table(table_name)

    # создаем асинхронный движок для связи с базой (да, само создание движка может выполняться синхронно)
    engine = create_async_engine(f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}', echo=True)

    #------------далее снова работаем асинхронно--------
    asyncio.run(async_main(engine, games))

async def adding_game(session, game):
    # Пробуем получить игру из базы, которая совпадает с игрой из парсера
    try:
        existing_game = session.query(Game).filter_by(product_id=game['product_id']).first()

        if existing_game: # игра существует в базе
            # завезли обновленные ценники
            if existing_game.discounted_price != game['discounted_price'] and game['discounted_price'] != 0:
                tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе есть. Обновляем ценник.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                existing_game.base_price = game['base_price']
                existing_game.discounted_price = game['discounted_price']
                existing_game.discount = game['discount']
                changed_games_count += 1
            # обновленные ценники нулевые
            elif game['discounted_price'] == 0 or game['base_price'] == 0:
                tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе есть. Удаляем.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                session.delete(existing_game)
                deleted_games_count += 1
            # ценники такие же, как и раньше
            else:
                tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе есть. Пропускаем.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                pass
        else:  # игры в базе нет
            if game['discounted_price'] == 0.0 or game['base_price'] == 0.0:
                tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе нет. Пропускаем.\nБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                pass
            else:
                tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе нет. Создаем.\nБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
                #тут создаем объект в базе            
                Game.__table__.name = f'{table_name}_games'
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
                added_games_count += 1

    except Exception:
        session.rollback()
        # декоратор loguru и так должен перехватывать эту ошибку детально без дополнительного логгера
        # logger("ERROR", f"Error while working with PostgreSQL.")

async def async_main(engine, games):
    async with AsyncSession(engine) as session:
        async with session.begin():
            coroutines = [adding_game(session, game) for game in games]
            await asyncio.gather(*coroutines)










@logger.catch
async def async_main(engine, games):
    async with AsyncSession(engine) as session:
        async with session.begin():
            added_games_count = 0
            changed_games_count = 0
            deleted_games_count = 0
            for game in games:
                
                -----------------------
            
            await session.commit()
            tamam_logger("INFO", f"{added_games_count} added. {changed_games_count} changed. {deleted_games_count} deleted. ")

                
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
            "product_id": "3TEST",
            "title": "3The Walking Test",
            "platforms": ["XBOX"],
            "base_price": 1998,
            "discounted_price": 13,
            "discount": 99,
            "img": "3https://store-image"
        }
    ]
    
    table_name = 'xbox'
    asyncio.run(async_db_insert('xbox', test_data))