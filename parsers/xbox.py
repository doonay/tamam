import asyncio
import aiohttp
from tamam_logger import tamam_logger
from insert_games import db_insert
import requests
from xbox_redata_logic import redata_logic

def get_games_ids() -> list: # список айдишников всех игр
    url = 'https://catalog.gamepass.com/sigls/v2?id=f6f1f99f-9b49-4ccd-b3bf-4d9767a77f5e&language=ru-ru&market=RU'
    session = requests.Session()
    r = session.get(url)
    games_ids_list = [id_dict['id'] for id_dict in r.json()[1:]]
    #games_ids_list = [r.json()[1:][1]['id'], r.json()[1:][2]['id']]
    return games_ids_list

async def get_product_data(session, chunks_str): #вот эти корутины запускаются параллельно
    url = f'https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds={chunks_str}&market=RU&languages=RU-RU&MS-CV=DGU1mcuYo0WMMp+F.1'
    async with session.get(url) as response:
        product_data = await response.json()
    return product_data['Products']

async def parser():
    games_ids_list = get_games_ids()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=20)) as session:
        tasks = []
        chunk_size = 10  # Количество идентификаторов в пакете
        id_chunks = [games_ids_list[i:i + chunk_size] for i in range(0, len(games_ids_list), chunk_size)]
        for chunk in id_chunks:
            tasks.append(get_product_data(session, ','.join(chunk)))
        product_results = await asyncio.gather(*tasks)
        all_redata_games = []
        for all_pages_item in product_results:
            for one_page_item in all_pages_item:
                one_redata_game = redata_logic(one_page_item)
                all_redata_games.append(one_redata_game)
        return all_redata_games    

def main():
    import os
    table_name = os.path.basename(__file__).split('.')[0]
    #tamam_logger("DEBUG", f"Задано имя таблицы {table_name}")
    all_redata_games = asyncio.run(parser())
    db_insert(table_name, all_redata_games)
    
if __name__ == '__main__':
    main()
    tamam_logger("DEBUG", "-----")
