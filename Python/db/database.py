import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv
# DATABASE_TYPE Read from .env File
load_dotenv()
TYPE = os.getenv("DATABASE_TYPE")
if TYPE is not None:
    TYPE = TYPE.lower() in ['true','yes']
else:
    TYPE = False

if TYPE :
    # SQLite database file Path
    DATABASE_URL = "sqlite:///./database.db"  
    # Check if the database file already exists
    if not os.path.exists("database.db"):
        print("Database file does not exist. Creating a new one...")
    # Create the engine, which will create the file if it doesn't exist
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else :
    # PostgreSQL Server
    DATABASE_URL = "postgresql://avnadmin:AVNS_KeUZSaQptyNPozIp0XP@pg-170b61e7-postgresql0005.i.aivencloud.com:25658/defaultdb?sslmode=require"
    # Create the engine, which will create the file if it doesn't exist
    engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# Models
class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    customer = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product = Column(String)
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")

# Create the tables if they don't exist
Base.metadata.create_all(bind=engine)

print("Database and tables are ready.")