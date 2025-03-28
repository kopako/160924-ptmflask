from typing import List
from sqlalchemy import create_engine, Integer, String, Boolean, Numeric, ForeignKey, func, select, update
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
                              echo=True
                           )

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
        "Category", back_populates="products")

class Category(Base):
    __tablename__ = "category"
    category_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(String(250))

    products: Mapped[list['Product']] = relationship(
        "Product", back_populates="category")


def task1(session):
    categories: List[Category] = []
    electronic_category = Category(
        name="Электроника", description="Гаджеты и устройства.")
    book_category = Category(
        name="Книги", description="Печатные книги и электронные книги.")
    cloth_category = Category(
        name="Одежда", description="Одежда для мужчин и женщин.")
    categories.append(electronic_category)
    categories.append(book_category)
    categories.append(cloth_category)
    products: List[Product] = []
    products.append(Product(name="Смартфон", price=299.99,
                    in_stock=True, category=electronic_category))
    products.append(Product(name="Ноутбук", price=499.99,
                    in_stock=True, category=electronic_category))
    products.append(Product(name="Научно-фантастический роман",
                    price=15.99, in_stock=True, category=book_category))
    products.append(Product(name="Джинсы", price=40.50,
                    in_stock=True, category=cloth_category))
    products.append(Product(name="Футболка", price=20,
                    in_stock=True, category=cloth_category))
    session.add_all(categories)
    session.add_all(products)
    session.commit()


def task2(session):
    for cat in session.query(Category).all():
        print('# # '*20)
        [print(f" Category: {cat.name}; Product name:{p.name}, price: {p.price}")
         for p in cat.products]


def task3(session):
    stmt = update(Product).where(Product.name ==
                                 "Смартфон").values(price=349.99)
    session.execute(stmt)


def task4(session):
    result = (session
              .query(Category.name, func.count(Product.product_id).label("product_count"))
              .outerjoin(Category.products)
              .group_by(Category.category_id)
              .all())
    for category_name, product_count in result:
        print(f"Category: {category_name}, Product Count: {product_count}")


def task5(session):
    result = (session
              .query(Category.name)
              .outerjoin(Category.products)
              .group_by(Category.category_id)
              .having(func.count(Product.product_id) > 1)
              .all())
    [print(c) for c in result]


if __name__ == "__main__":
    Base.metadata.create_all(bind=sql_engine)
    SessionFabric = sessionmaker(bind=sql_engine)
    session = SessionFabric()
    task1(session=session)
    task2(session=session)
    task3(session=session)
    task3(session=session)
    task4(session=session)
    task5(session=session)

    session.close()
