from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login

from sqlalchemy.dialects.mssql.base import XML, BIT

from sqlalchemy.sql import expression


class XmlData(db.Model):

    __bind_key__ = 'data'
    __tablename__ = 'XMLData'

    id = db.Column(db.Integer, primary_key=True)
    xml_data = db.Column(XML)
    processed = db.Column(db.Boolean(), server_default=expression.false())
    # error = db.Column(db.Boolean(), server_default=expression.false())
    # empty_doc = db.Column(db.Boolean(), server_default=expression.false())
    # unsupported_doc = db.Column(
    #     db.Boolean(), server_default=expression.false())
    # catched = db.Column(db.Boolean(), server_default=expression.false())
    # task_id = db.Column(db.String(64), index=True)


class XmlDataP(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    xml_data = db.Column(db.Text())
    processed = db.Column(db.Boolean(), default=False)
    empty_doc = db.Column(db.Boolean(), default=False)
    unsupported_doc = db.Column(db.Boolean(), default=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    verified = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    barcode = db.Column(db.String(13), index=True)

    @classmethod
    def get_id(cls, name):
        author = db.session.query(cls).filter(
            cls.name == name).one_or_none()
        if author is None:
            author = cls(name=name)
            db.session.add(author)
            db.session.commit()
        return author.id


class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), index=True, unique=True, nullable=False)
    date = db.Column(db.DateTime())
    plant = db.Column(db.String(1), index=True)

    @classmethod
    def get_id(cls, name):
        batch = db.session.query(cls).filter(
            cls.name == name).one_or_none()
        if batch is None:
            batch = cls(name=name)
            db.session.add(batch)
            db.session.commit()
        return batch.id


class Barrel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)

    @classmethod
    def get_id(cls, name):
        barrel = db.session.query(cls).filter(
            cls.name == name).one_or_none()
        if barrel is None:
            barrel = cls(name=name)
            db.session.add(barrel)
            db.session.commit()
        return barrel.id


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True, nullable=False)

    @classmethod
    def get_id(cls, name):
        container = db.session.query(cls).filter(
            cls.name == name).one_or_none()
        if container is None:
            container = cls(name=name)
            db.session.add(container)
            db.session.commit()
        return container.id


class Doctype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    alias = db.Column(db.String(50), index=True)


class Product(db.Model):
    id = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(255), index=True)
    marking = db.Column(db.String(50), index=True)
    barcode = db.Column(db.String(13), index=True)

    @classmethod
    def get_id(cls, id):
        product = db.session.query(cls).filter(
            cls.id == id).one_or_none()
        if product is None:
            product = cls(id=id)
            db.session.add(product)
            db.session.commit()
        return product.id


class Boil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey(
        'batch.id'), index=True, nullable=False)
    product_id = db.Column(db.String(6), db.ForeignKey(
        'product.id'), index=True, nullable=False)
    quantity = db.Column(db.Numeric(precision=5, scale=4))


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.String(50), index=True, unique=True)
    doctype_id = db.Column(db.Integer, db.ForeignKey(
        'doctype.id'), index=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'author.id'), index=True, nullable=False)
    date = db.Column(db.DateTime())
    plant = db.Column(db.String(1), index=True)

    @classmethod
    def get_id(cls, doc_id, doctype_id, author_id, date, plant):
        document = db.session.query(cls).filter(
            cls.doc_id == doc_id).one_or_none()
        if document is None:
            document = cls(doc_id=doc_id,
                           doctype_id=doctype_id,
                           author_id=author_id,
                           date=date,
                           plant=plant)
            db.session.add(document)
            db.session.commit()
        return document.id


class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)


class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)


class ManufacturerLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)


class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    product_id = db.Column(db.String(6), db.ForeignKey(
        'product.id'), index=True, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey(
        'seller.id'), index=True, nullable=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey(
        'manufacturer.id'), index=True, nullable=True)
    manufacturer_lot_id = db.Column(db.Integer, db.ForeignKey(
        'manufacturer_lot.id'), index=True, nullable=True)

    @classmethod
    def get_id(cls, name, product_id):
        lot = db.session.query(cls).filter(
            cls.name == name).one_or_none()
        if lot is None:
            lot = cls(name=name,
                      product_id=product_id)
            db.session.add(lot)
            db.session.commit()
        return lot.id


class BatchProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey(
        'batch.id'), index=True, nullable=False)
    product_id = db.Column(db.String(6), db.ForeignKey(
        'product.id'), index=True, nullable=False)


class Acceptance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey(
        'document.id'), index=True, nullable=False)
    product_id = db.Column(db.String(6), db.ForeignKey(
        'product.id'), index=True, nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey(
        'lot.id'), index=True, nullable=False)
    expire_date = db.Column(db.DateTime())
    barrel_id = db.Column(db.Integer, db.ForeignKey(
        'barrel.id'), index=True, nullable=False)
    barrel_capacity = db.Column(db.Numeric(precision=9, scale=4))
    barrel_quantity = db.Column(db.Integer)


class Load(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey(
        'document.id'), index=True, nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey(
        'container.id'), index=True, nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey(
        'batch.id'), index=True, nullable=False)


class Weighting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey(
        'document.id'), index=True, nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey(
        'container.id'), index=True, nullable=False)
    product_id = db.Column(db.String(6), db.ForeignKey(
        'product.id'), index=True, nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey(
        'lot.id'), index=True, nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey(
        'batch.id'), index=True, nullable=False)
    quantity = db.Column(db.Numeric(precision=9, scale=4))
