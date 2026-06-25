from decimal import Decimal
from sqlalchemy import create_engine, String, Numeric, ForeignKey, func
from sqlalchemy.orm import (sessionmaker, DeclarativeBase, Mapped,
                            mapped_column, relationship)
from typing import List

engine = create_engine('sqlite:///test_2.db')
LocalSession = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False,unique=True)
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[List["Product"]] = relationship(back_populates="category")

    def __str__(self):
        return f"Category: {self.name}"

    def __repr__(self):
        return f"Category(id={self.id}, name='{self.name}')"

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    in_stock: Mapped[bool] = mapped_column(default=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped["Category"] = relationship(back_populates="products")

    def __str__(self):
        return f"{self.name:<30} | price: {self.price:>8} | categorie: {self.category.name:>12}"

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}')"


Base.metadata.create_all(engine)

if __name__ == '__main__':
    with LocalSession() as session:

        if not session.query(Category).first():
            c1 = Category(name="Электроника", description="Гаджеты и устройства.",
                        products=[
                            Product(name="Смартфон", price=Decimal("299.99")),
                            Product(name="Ноутбук", price=Decimal("499.99"))
                        ])
            c2 = Category(name="Книги", description="Печатные книги и электронные книги.",
                          products=[
                                Product(name="Научно-фантастический роман", price=Decimal("15.99"))
                                     ])
            c3 = Category(name="Одежда", description="Одежда для мужчин и женщин.",
                          products=[
                                    Product(name="Джинсы", price=Decimal("40.50")),
                                    Product(name="Футболка", price=Decimal("20.00"))
                                ])
            session.add_all([c1, c2, c3])
            session.commit()
        print("\n--- List of all products ---")
        for p in session.query(Product).all():
            print(p)

        print("\n--- List of all categories ---")
        for c in session.query(Category).all():
            print(c)

            print("\nСтатистика (Категории с > 1 продуктом):")
            stats = session.query(Category.name, func.count(Product.id)) \
                .join(Product) \
                .group_by(Category.name) \
                .having(func.count(Product.id) > 1) \
                .all()

            for name, count in stats:
                print(f"{name}: {count} продукта(ов)")

