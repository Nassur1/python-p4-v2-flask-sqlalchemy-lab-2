from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class SerializerMixin:
    serialize_rules = ()

    def to_dict(self):
        d = {}

        # Serialize columns
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)

        # Serialize relationships safely
        for rel in self.__mapper__.relationships:
            
            if any(rule.strip('-') == rel.key for rule in getattr(self, 'serialize_rules', ())):
                continue

            value = getattr(self, rel.key)

            if value is None:
                d[rel.key] = None
            elif isinstance(value, list):
                
                d[rel.key] = [
                    {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
                    for obj in value
                ]
            else:
                d[rel.key] = {c.name: getattr(value, c.name) for c in value.__table__.columns}

        return d

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    
    reviews = db.relationship(
        "Review",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    
    items = association_proxy("reviews", "item")

    
    serialize_rules = (
        "-reviews.customer",   # prevent recursion
    )

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"



class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    
    reviews = db.relationship(
        "Review",
        back_populates="item",
        cascade="all, delete-orphan"
    )

    
    serialize_rules = (
        "-reviews.item",    
    )

    def __repr__(self):
        return f"<Item {self.id}, {self.name}, {self.price}>"



class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    
    customer = db.relationship("Customer", back_populates="reviews")
    item = db.relationship("Item", back_populates="reviews")

    
    serialize_rules = (
        "-customer.reviews",
        "-item.reviews",
    )

    def __repr__(self):
        return f"<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}>"

