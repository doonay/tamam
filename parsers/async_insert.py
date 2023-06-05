from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Game
from config import user, password, host, port, db_name
from table_create import create_table
from tamam_logger import tamam_logger, logger
import asyncio
import logging
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Query
from sqlalchemy import select
from sqlalchemy.future import select

# Добавление новых игр
@logger.catch
async def adding_game(session, table_name, game):
    #try:
    existing_game = await session.execute(select(Game).filter_by(product_id=game['product_id']))
    existing_game = existing_game.scalars().first()

    if existing_game: # игра существует в базе
        # завезли обновленные ценники
        if existing_game.discounted_price != game['discounted_price'] and game['discounted_price'] != 0:
            tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе есть. Обновляем ценник.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
            existing_game.base_price = game['base_price']
            existing_game.discounted_price = game['discounted_price']
            existing_game.discount = game['discount']
            return 'changed'
        # обновленные ценники нулевые
        elif game['discounted_price'] == 0 or game['base_price'] == 0:
            tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе есть. Удаляем.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
            session.delete(existing_game)
            return 'deleted'
        # ценники такие же, как и раньше
        else:
            tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе есть. Пропускаем.\nБаза:\tБазовая цена: {existing_game.base_price}, цена со скидкой:{existing_game.discounted_price}, скидка:{existing_game.discount}.\nПарсер:\tБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
            return 'skipped'
    else:  # игры в базе нет
        if game['discounted_price'] == 0.0 or game['base_price'] == 0.0:
            tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе нет. Пропускаем.\nБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
            return 'skipped'
        else:
            tamam_logger("DEBUG", f"{game['product_id'], game['title']}. В базе нет. Создаем.\nБазовая цена: {game['base_price']}, цена со скидкой:{game['discounted_price']}, скидка:{game['discount']}.")
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
            return 'added'
    
    #except Exception as e:
    #    await session.rollback()
    #    return 'error'

# Проверка и удаление старых игр
@logger.catch
async def clean_db(session, table_name, games):
    #try:
    Game.__table__.name = f'{table_name}_games'
    existing_games = await session.execute(select(Game))
    #existing_games = await existing_games.fetchall()
    #db_games = await session.execute(Query(Game).select_from(Game).all())
    #db_games = db_games.scalars().all()
    for existing_game in existing_games:
        if existing_game.product_id not in [game['product_id'] for game in games]:
            session.delete(existing_game)
    tamam_logger("INFO", "All unused games have been deleted from the database.")
    
    
    


    #except Exception:
    #    await session.rollback()
    #    return 'error'

async def async_main(engine, table_name, games):
    async with AsyncSession(engine) as session:
        async with session.begin():
            coroutines = [adding_game(session, table_name, game) for game in games]
            results = await asyncio.gather(*coroutines)

            
            await clean_db(session, table_name, games)

            await session.commit()

            added_games_count = results.count('added')
            changed_games_count = results.count('changed')
            deleted_games_count = results.count('deleted')

            # ...
            # Остальной код для обработки результатов, логирования и др.
            # ...

def sync_main(table_name, games):
    #------------работаем синхронно--------
    # Переводим логгер SQLAlchemy в режим WARNING, что бы не видеть в консоли сообщения уровня INFO
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    # создаем асинхронный движок для связи с базой (да, само создание движка может выполняться синхронно)
    engine = create_async_engine(f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}', echo=True)

    # Если таблицы нет, сначала создадим таблицу
    #inspector = inspect(engine)
    #if not inspector.has_table(f'{table_name}_games'):
    create_table(table_name)

    #------------далее снова работаем асинхронно--------
    asyncio.run(async_main(engine, table_name, games))

if __name__ == '__main__':
    test_data = [
        {
            "product_id": "7TEST",
            "title": "7The Walking Test",
            "platforms": ["XBOX"],
            "base_price": 1998,
            "discounted_price": 13,
            "discount": 99,
            "img": "7https://store-image"
        }
    ]
    
    import os
    TABLE_NAME = os.path.basename(__file__).split('.')[0]
    sync_main('xyz', test_data)