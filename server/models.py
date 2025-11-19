from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

# ------------------------------------------------------------
# Customer Model
# ------------------------------------------------------------
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    # Task 1: Relationship to Review
    reviews = db.relationship(
        "Review",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    # Task 2: Association Proxy → get items through reviews
    items = association_proxy("reviews", "item")

    # Task 3: Serialization rules
    serialize_rules = (
        "-reviews.customer",   # prevent recursion
    )

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"


# ------------------------------------------------------------
# Item Model
# ------------------------------------------------------------
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Task 1: Relationship to Review
    reviews = db.relationship(
        "Review",
        back_populates="item",
        cascade="all, delete-orphan"
    )

    # Task 3 serialization rules
    serialize_rules = (
        "-reviews.item",    # prevent recursion
    )

    def __repr__(self):
        return f"<Item {self.id}, {self.name}, {self.price}>"


# ------------------------------------------------------------
# Review Model (Task 1)
# ------------------------------------------------------------
class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    # Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    # Relationships
    customer = db.relationship("Customer", back_populates="reviews")
    item = db.relationship("Item", back_populates="reviews")

    # Task 3: Serialization rules
    serialize_rules = (
        "-customer.reviews",
        "-item.reviews",
    )

    def __repr__(self):
        return f"<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}>"

