from sqlalchemy import Column, Integer, String, ARRAY, SmallInteger, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base


Base = declarative_base()
def create_game_class(table_name):
    class Game(Base):
        __tablename__ = table_name
        id = Column(Integer, primary_key=True)
        product_id = Column(String)
        title = Column(String)
        platforms = Column(ARRAY(String))
        base_price = Column(Integer)
        discounted_price = Column(Integer)
        discount = Column(SmallInteger)
        img = Column(String)
        last_modified = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    return Game
