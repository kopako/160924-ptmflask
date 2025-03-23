from sqlalchemy import create_engine, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, sessionmaker
# Task 1: Create an instance of the engine to connect to the in-memory SQLite database.
# Task 2: Create a session to interact with the database using the engine you just created.
# Task 3: Define a Product model with the following column types:
# id: numeric identifier
# name: string (max 100 characters)
# price: fixed-precision numeric value
# in_stock: boolean
# Task 4: Define a related Category model with the following column types:
# id: numeric identifier
# name: string (max 100 characters)
# description: string (max 255 characters)
# Task 5: Establish a relationship between the Product and Category tables using the category_id column.

URL = "sqlite:///:memory:"
sql_engine = create_engine(url=URL,
                           echo_pool=True,
                           echo=True)

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    product_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(8, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean)

    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('category.category_id'))
    category: Mapped['Category'] = relationship(
        "Category", back_populates="product")


class Category(Base):
    __tablename__ = "category"
    category_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(String(250))

    product: Mapped['Product'] = relationship(
        "Product", back_populates="category")


Base.metadata.create_all(bind=sql_engine)

SessionFabric = sessionmaker(bind=sql_engine)
session = SessionFabric()
session.close()
