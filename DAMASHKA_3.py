from decimal import Decimal
from typing import List
from sqlalchemy import create_engine, String, Numeric, ForeignKey
from sqlalchemy.orm import (sessionmaker, DeclarativeBase, Mapped,
                            mapped_column, relationship)

engine = create_engine('sqlite:///test_1.db')

LocalSession = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False,unique=True)
    description: Mapped[str] = mapped_column(String(255), default="No description")

    products: Mapped[List["Product"]] = relationship(back_populates="category")

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}', description='{self.description}')"

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    in_stock: Mapped[bool] = mapped_column(default=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped["Category"] = relationship(back_populates="products")

    def __str__(self):
        return f"{self.name} (price: {self.price})"


Base.metadata.create_all(engine)

if __name__ == '__main__':

    with LocalSession() as session:
        existing_category = session.query(Category).filter_by(name="Electronics").first()
        if not existing_category:
            new_category = Category(
                name="Electronics",
                description="Electronics Department",
                products=[
                    Product(name="Laptop", price=Decimal("999.99")),
                    Product(name="Mouse", price=Decimal("25.50")),
                    Product(name="Keyboard", price=Decimal("45.00"))
                ]
            )
            session.add(new_category)
            session.commit()
# products = session.query(Product).all()
# print(products)
for cat in session.query(Product).all():
    print(cat)