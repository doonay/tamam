from sqlalchemy import BigInteger, Integer, Column, String, ARRAY, SmallInteger, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey

Base = declarative_base()
class Platform(Base):
    __tablename__ = 'platform'
    id = Column(Integer, primary_key=True)
    name = Column(String)

def create_game_class(table_name):
    class Game(Base):
        __tablename__ = table_name
        #id = Column(Integer, primary_key=True)
        id = Column(BigInteger, primary_key=True, autoincrement=True)
        product_id = Column(String)
        title = Column(String)
        #platform_id = Column(Integer, ForeignKey('platform.id'))
        #platform = Column(String)
        platform = Column(Integer, ForeignKey('platform.id'))
        sub_platforms = Column(ARRAY(String))
        base_price = Column(Integer)
        discounted_price = Column(Integer)
        discount = Column(SmallInteger)
        img = Column(String)
        last_modified = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    return Game
