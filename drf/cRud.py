from sqlalchemy import create_engine, Column, Integer, String, JSON, Numeric, SmallInteger, TIMESTAMP
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base


# Создаем соединение с базой данных
engine = create_engine('postgresql://tamamrunner:Go_063223@localhost:5432/tamambase')

# Создаем сессию для выполнения запросов
Session = sessionmaker(bind=engine)
session = Session()

# Создаем базовую модель
Base = declarative_base()

# Определяем модель таблицы
class XboxGame(Base):
    __tablename__ = 'xbox_games'

    id = Column(Integer, primary_key=True)
    game_id = Column(String, unique=True)
    title = Column(String)
    platforms = Column(JSON)
    base_price = Column(Numeric(12, 2))
    discounted_price = Column(Numeric(12, 2))
    discount = Column(SmallInteger)
    img = Column(String)
    last_modified = Column(TIMESTAMP)

# Создаем таблицы
Base.metadata.create_all(engine)

if __name__ == '__main__':
    # Создаем и вносим тестовую запись
    game = XboxGame(
        game_id='123456',
        title='Example Game',
        platforms=['Xbox One', 'Xbox Series X'],
        base_price=59.99,
        discounted_price=49.99,
        discount=10,
        img='example.jpg'
    )

    session.add(game)
    session.commit()
