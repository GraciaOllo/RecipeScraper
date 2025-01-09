from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)

def init_db():
    engine = create_engine('sqlite:///recipes.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
