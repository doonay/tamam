import aiohttp
import asyncio
import time

async def get_all_xbox_game_ids(session):
    url = 'https://catalog.gamepass.com/sigls/v2?id=f6f1f99f-9b49-4ccd-b3bf-4d9767a77f5e&language=ru-ru&market=RU'
    async with session.get(url) as response:
        all_xbox_games_ids = await response.json()
        ids_list = [game['id'] for game in all_xbox_games_ids[1:]]
        return ids_list

async def get_product_data(session, ids_list):
    url = f'https://displaycatalog.mp.microsoft.com/v7.0/products?bigIds={ids_list}&market=RU&languages=RU-RU&MS-CV=DGU1mcuYo0WMMp+F.1'
    async with session.get(url) as response:
        product_data = await response.json()
        return product_data['Products']

async def get_all_product_data(session, ids_list):
    tasks = []
    products = []
    chunk_size = 10  # Количество идентификаторов в пакете
    id_chunks = [ids_list[i:i + chunk_size] for i in range(0, len(ids_list), chunk_size)]
    for chunk in id_chunks:
        tasks.append(get_product_data(session, ','.join(chunk)))
    product_results = await asyncio.gather(*tasks)
    for result in product_results:
        products.extend(result)
    return products

async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=20)) as session:
        
        ids_list = await get_all_xbox_game_ids(session)

        start_time = time.time()
        product_data = await get_all_product_data(session, ids_list)
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"Время: {execution_time} секунд. Кол-во полученных объектов: {len(product_data)}")

if __name__ == '__main__':
    asyncio.run(main())
    #200 limit=10 Время: 13.92 секунд. Кол-во полученных объектов: 425
    #100 limit=10 Время: 6.62 секунд, Кол-во полученных объектов: 425
    #50 limit=10 Время: 3.67 секунд. Кол-во полученных объектов: 425
    #25 limit=10 Время: 3.97 секунд. Кол-во полученных объектов: 425
    #10 limit=10 Время: 3.26 секунд. Кол-во полученных объектов: 425
    #10 limit=20 Время: 3.10 секунд. Кол-во полученных объектов: 425
    #15 limit=10 Время: 3.82 секунд. Кол-во полученных объектов: 425
    #5 limit=10 Время: 4.37 секунд. Кол-во полученных объектов: 425
    #50 limit=50 Время: 3.49 секунд. Кол-во полученных объектов: 425
    #100 limit=100 Время: 3.96 секунд. Кол-во полученных объектов: 425