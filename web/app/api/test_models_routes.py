from . import bp
from app import db
from flask import jsonify
from app.models import (
    Acceptance,
    Author,
    Barrel,
    Batch,
    Boil,
    Btproduct,
    Container,
    Doctype,
    Document,
    Load,
    Lot,
    Manufacturer,
    Manufacturerlot,
    Product,
    Seller,
    Trademark,
    Weighting,
)


@bp.route('/test')
def index():
    acceptance = db.session.query(Acceptance).first()
    acceptance = {
        'AcceptancePK': acceptance.AcceptancePK,
        'DocumentPK': acceptance.DocumentPK,
        'ProductId': acceptance.ProductId,
        'LotPK': acceptance.LotPK,
        'ExpiredDate': acceptance.ExpiredDate,
        'BarrelsId': acceptance.BarrelsId,
        'BarrelsQuantity': acceptance.BarrelsQuantity,
        'BarrelsCapasity': acceptance.BarrelsCapacity
    }

    author = db.session.query(Author).first()
    author = {
        'id': author.AuthorPK,
        'name': author.AuthorName,
        'barcode': author.AuthorBarcode
    }

    barrel = db.session.query(Barrel).first()
    barrel = {
        'id': barrel.BarrelsId,
        'name': barrel.BarrelsName
    }

    batch = db.session.query(Batch).first()
    batch = {
        'id': batch.BatchPK,
        'name': batch.BatchName,
        'date': batch.BatchDate,
        'plant': batch.Plant
    }

    boil = db.session.query(Boil).first()
    boil = {
        'id': boil.BoilPK,
        'batch': boil.BatchPK,
        'product': boil.ProductId,
        'quantity': boil.Quantity
    }

    btproduct = db.session.query(Btproduct).first()
    btproduct = {
        'id': btproduct.BtProductPK,
        'batch': btproduct.BatchPK,
        'product': btproduct.ProductId
    }

    container = db.session.query(Container).first()
    container = {
        'id': container.ContainerPK,
        'name': container.ContainerName
    }

    doctype = db.session.query(Doctype).first()
    doctype = {
        'id': doctype.DoctypePK,
        'name': doctype.DoctypeName,
        'alias': doctype.DoctypeAlias
    }

    document = db.session.query(Document).first()
    document = {
        'id': document.DoctypePK,
        'cl': document.DocumentClid,
        'dtype': document.DoctypePK,
        'author': document.AuthorPK,
        'date': document.CreateDate,
        'plant': document.Plant
    }

    load = db.session.query(Load).first()
    load = {
        'id': load.LoadsPK,
        'document': load.DocumentPK,
        'container': load.ContainerPK,
        'batch': load.BatchPK
    }

    lot = db.session.query(Lot).first()
    lot = {
        'id': lot.LotPK,
        'name': lot.LotName,
        'product': lot.ProductId,
        'seller': lot.SellerPK,
        'manufacturer': lot.ManufacturerPK,
        'man_lot': lot.ManufacturerLotPK,
        'tm': lot.TradeMarkPK
    }

    manufacturerlot = db.session.query(Manufacturerlot).first()
    manufacturerlot = {
        'id': manufacturerlot.ManufacturerLotPK,
        'name': manufacturerlot.ManufacturerLotName
    }

    manufacturer = db.session.query(Manufacturer).first()
    manufacturer = {
        'id': manufacturer.ManufacturerPK,
        'name': manufacturer.ManufacturerName
    }

    product = db.session.query(Product).first()
    product = {
        'id': product.ProductId,
        'name': product.ProductName,
        'marking': product.ProductMarking,
        'barcode': product.ProductBarcode
    }

    seller = db.session.query(Seller).first()
    seller = {
        'id': seller.SellerPK,
        'name': seller.SellerName,
    }

    trademark = db.session.query(Trademark).first()
    trademark = {
        'id': trademark.TrademarkPK,
        'name': trademark.TrademarkName
    }

    weighting = db.session.query(Weighting).first()
    weighting = {
        'id': weighting.WeightingsPK,
        'document': weighting.DocumentPK,
        'container': weighting.ContainerPK,
        'product': weighting.ProductId,
        'batch': weighting.BatchPK,
        'lot': weighting.LotPK,
        'quantity': weighting.Quantity
    }

    return jsonify({'data':
                    {
                        'acceptance': acceptance,
                        'author': author,
                        'barrel': barrel,
                        'batch': batch,
                        'boil': boil,
                        'btproduct': btproduct,
                        'container': container,
                        'doctype': doctype,
                        'document': document,
                        'load': load,
                        'lot': lot,
                        'manufacturer': manufacturer,
                        'manufacturerlot': manufacturerlot,
                        'product': product,
                        'seller': seller,
                        'trademark': trademark,
                        'weighting': weighting,
                    }
                    })
