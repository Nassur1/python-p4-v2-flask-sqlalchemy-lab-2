# TODO List for Flask-SQLAlchemy Lab Tasks

## Task #1: Add Review Model and Relationships
- [ ] Edit server/models.py to add Review class with attributes: __tablename__, id, comment, customer_id, item_id, relationships to Customer and Item, back_populates.
- [ ] Add reviews relationship to Customer model.
- [ ] Add reviews relationship to Item model.
- [ ] Run flask db migrate -m 'add review' (in server directory).
- [ ] Run flask db upgrade head (in server directory).
- [ ] Run pytest testing/review_test.py to test Review model.

## Task #2: Add Association Proxy
- [x] Add association proxy 'items' to Customer model in server/models.py.
- [ ] Run pytest testing/association_proxy_test.py to test association proxy.

## Task #3: Add Serialization
- [x] Make Customer, Item, Review inherit from SerializerMixin in server/models.py.
- [x] Add serialize_rules to Customer (exclude 'reviews.customer'), Item (exclude 'reviews.item'), Review (exclude 'customer.reviews' and 'item.reviews').
- [ ] Run pytest testing/serialization_test.py to test serialization.

## Final Steps
- [ ] Run pytest to ensure all tests pass.
- [ ] Run python seed.py to populate database with sample data.
