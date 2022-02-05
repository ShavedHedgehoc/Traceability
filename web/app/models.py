from app import db
from sqlalchemy.sql import func


class Acceptance(db.Model):
    __tablename__ = "Acceptance"

    AcceptancePK = db.Column(db.Integer, primary_key=True)
    DocumentPK = db.Column(db.Integer, nullable=False)
    ProductId = db.Column(db.String(6), nullable=False)
    LotPK = db.Column(db.Integer, nullable=False)
    ExpiredDate = db.Column(db.DateTime, nullable=False)
    BarrelsId = db.Column(db.Integer, nullable=False)
    BarrelsCapacity = db.Column(db.Numeric(
        precision=9, scale=5), nullable=False)
    BarrelsQuantity = db.Column(db.Integer, nullable=False)


class Author(db.Model):
    __tablename__ = "Authors"

    AuthorPK = db.Column(db.Integer, primary_key=True)
    AuthorName = db.Column(db.String(50), unique=True, nullable=False)
    AuthorBarcode = db.Column(db.String(13))


class Barrel(db.Model):
    __tablename__ = "Barrels"

    BarrelsId = db.Column(db.Integer, primary_key=True)
    BarrelsName = db.Column(db.String(50), unique=True, nullable=False)


class Batch(db.Model):
    __tablename__ = "Batchs"

    BatchPK = db.Column(db.Integer, primary_key=True)
    BatchName = db.Column(db.String(10), unique=True, nullable=False)
    BatchDate = db.Column(db.DateTime)
    Plant = db.Column(db.String(1))

    @classmethod
    def get_name_date_plant_by_id(cls, id):
        """Return dictionary {name, date, plant}
        """
        batch = db.session.query(cls).filter(cls.BatchPK == id).one_or_none()
        if batch is None:
            return {
                'name': 'Not found',
                'date': 'Not found',
                'plant': 'Not found'
            }
        return {
            'name': batch.BatchName,
            'date': batch.BatchDate,
            'plant': batch.Plant
        }


class Boil(db.Model):
    __tablename__ = "Boils"

    BoilPK = db.Column(db.Integer, primary_key=True)
    BatchPK = db.Column(db.Integer, nullable=False)
    ProductId = db.Column(db.String(6), nullable=False)
    Quantity = db.Column(db.Numeric(
        precision=9, scale=5), nullable=False)


class Btproduct(db.Model):
    __tablename__ = "BtProducts"

    BtProductPK = db.Column(db.Integer, primary_key=True)
    BatchPK = db.Column(db.Integer, nullable=False)
    ProductId = db.Column(db.String(6), nullable=False)


class Container(db.Model):
    __tablename__ = "Containers"

    ContainerPK = db.Column(db.Integer, primary_key=True)
    ContainerName = db.Column(db.String(50), unique=True, nullable=False)


class Doctype(db.Model):
    __tablename__ = "Doctypes"

    DoctypePK = db.Column(db.Integer, primary_key=True)
    DoctypeName = db.Column(db.String(50), unique=True, nullable=False)
    DoctypeAlias = db.Column(db.String(200))


class Document(db.Model):
    __tablename__ = "Documents"

    DocumentPK = db.Column(db.Integer, primary_key=True)
    DocumentClid = db.Column(db.String(50), unique=True, nullable=False)
    DoctypePK = db.Column(db.Integer, nullable=False)
    AuthorPK = db.Column(db.Integer, nullable=False)
    CreateDate = db.Column(db.DateTime, nullable=False)
    Plant = db.Column(db.String(1))


class Load(db.Model):
    __tablename__ = "Loads"

    LoadsPK = db.Column(db.Integer, primary_key=True)
    DocumentPK = db.Column(db.Integer, nullable=False)
    ContainerPK = db.Column(db.Integer, nullable=False)
    BatchPK = db.Column(db.Integer, nullable=False)


class Lot(db.Model):
    __tablename__ = "Lots"

    LotPK = db.Column(db.Integer, primary_key=True)
    LotName = db.Column(db.String(50), unique=True, nullable=False)
    ProductId = db.Column(db.String(6), nullable=False)
    SellerPK = db.Column(db.Integer, nullable=False)
    ManufacturerPK = db.Column(db.Integer, nullable=False)
    ManufacturerLotPK = db.Column(db.Integer, nullable=False)
    TradeMarkPK = db.Column(db.Integer, nullable=False)


class Manufacturerlot(db.Model):
    __tablename__ = "ManufacturerLots"

    ManufacturerLotPK = db.Column(db.Integer, primary_key=True)
    ManufacturerLotName = db.Column(
        db.String(200), unique=True, nullable=False)


class Manufacturer(db.Model):
    __tablename__ = "Manufacturers"

    ManufacturerPK = db.Column(db.Integer, primary_key=True)
    ManufacturerName = db.Column(
        db.String(200), unique=True, nullable=False)


class Product(db.Model):
    __tablename__ = "Products"

    ProductId = db.Column(db.String(6), primary_key=True)
    ProductName = db.Column(db.String(200))
    ProductMarking = db.Column(db.String(50))
    ProductBarcode = db.Column(db.String(13))

    @classmethod
    def get_name_by_id(cls, id):
        product = db.session.query(cls).filter(
            cls.ProductId == id).one_or_none()
        if product is None:
            return 'Not found'
        return product.ProductName


class Seller(db.Model):
    __tablename__ = "Sellers"

    SellerPK = db.Column(db.Integer, primary_key=True)
    SellerName = db.Column(db.String(200), unique=True, nullable=False)


class Trademark(db.Model):
    __tablename__ = "Trademarks"

    TrademarkPK = db.Column(db.Integer, primary_key=True)
    TrademarkName = db.Column(
        db.String(200), unique=True, nullable=False)


class Weighting(db.Model):
    __tablename__ = "Weightings"

    # replace 's' from fieldname 'WeightingsPK' in mssql?
    WeightingsPK = db.Column(db.Integer, primary_key=True)
    DocumentPK = db.Column(db.Integer, nullable=False)
    ContainerPK = db.Column(db.Integer, nullable=False)
    ProductId = db.Column(db.String(6), nullable=False)
    BatchPK = db.Column(db.Integer, nullable=False)
    LotPK = db.Column(db.Integer, nullable=False)
    Quantity = db.Column(db.Numeric(
        precision=9, scale=5), nullable=False)

    @classmethod
    def get_sum_by_batch_product(cls, batchid, productid):
        sum = db.session.query(func.sum(cls.Quantity).label('sum')).filter(
            cls.BatchPK == batchid).filter(cls.ProductId == productid).scalar()
        if sum is None:
            return 0
        return sum
