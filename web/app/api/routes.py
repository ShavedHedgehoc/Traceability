import operator
from flask import abort, jsonify
from sqlalchemy.sql import func, case

from . import bp
from app import db
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


@bp.route("/api/v1/boils/summary/<int:batchid>", methods=['GET'])
def boil_summary_data(batchid):

    batch_data = Batch.get_name_date_plant_by_id(batchid)

    boil_subqry = db.session.query(
        Boil.BatchPK.label('batch_id'),
        Boil.ProductId.label('product_id'),
        Boil.Quantity.label('plan'),
        Product.ProductName.label('product_name')
    ).join(
        Product, Boil.ProductId == Product.ProductId
    ).filter(
        Boil.BatchPK == batchid
    ).subquery()

    wght_subqry = db.session.query(
        Weighting.BatchPK,
        Weighting.ProductId.label('product_id'),
        Product.ProductName.label('product_name'),
        func.sum(Weighting.Quantity).label('fact')
    ).join(
        Product, Weighting.ProductId == Product.ProductId
    ).filter(
        Weighting.BatchPK == batchid
    ).group_by(
        Weighting.BatchPK,
        Weighting.ProductId,
        Product.ProductName
    ).subquery()

    boil_qry = db.session.query(
        boil_subqry.c.product_id.label('b_product_id'),
        boil_subqry.c.product_name.label('b_product_name'),
        boil_subqry.c.plan.label('plan'),
        wght_subqry.c.product_id.label('w_product_id'),
        wght_subqry.c.product_name.label('w_product_name'),
        wght_subqry.c.fact.label('fact')
    ).join(
        wght_subqry,
        boil_subqry.c.product_id == wght_subqry.c.product_id,
        full=True
    ).order_by(case(
        [(boil_subqry.c.product_name != '', boil_subqry.c.product_name), ],
        else_=wght_subqry.c.product_name
    ) .asc())

    boil_rows = boil_qry.all()

    if boil_rows is None:
        abort(404)

    data = []

    for row in boil_rows:
        product_id = row.b_product_id if row.b_product_id\
            else row.w_product_id
        product_name = row.b_product_name if row.b_product_name\
            else row.w_product_name
        state = (row.plan is not None) and (row.fact is not None)
        data.append({
            'product_id': product_id,
            'product_name': product_name,
            'state': state,
            'plan': str(row.plan),
            'fact':  str(row.fact)
        })

    response = {'boil': {'name': batch_data['name'],
                         'date': batch_data['date'],
                         'plant': batch_data['plant'],
                         'data': data}
                }

    return jsonify(response)


@bp.route("/api/v1/boils/weighting/<int:batchid>", methods=['GET'])
def boil_weighting_data(batchid):

    batch_data = Batch.get_name_date_plant_by_id(batchid)

    wght_qry = db.session.query(
        Weighting.ProductId.label('product_id'),
        Product.ProductName.label('product_name'),
        Weighting.Quantity.label('quantity'),
        Lot.LotPK.label('lot_id'),
        Lot.LotName.label('lot'),
        Author.AuthorName.label('user'),
        Document.CreateDate.label('date')
    ).join(
        Product, Weighting.ProductId == Product.ProductId
    ).join(
        Lot, Weighting.LotPK == Lot.LotPK
    ).join(
        Document, Weighting.DocumentPK == Document.DocumentPK
    ).join(
        Author, Document.AuthorPK == Author.AuthorPK
    ).filter(
        Weighting.BatchPK == batchid
    ).order_by((Product.ProductName).asc())

    weighting_rows = wght_qry.all()

    if weighting_rows is None:
        abort(404)

    data = []

    for row in weighting_rows:
        data.append({
            'product_id': row.product_id,
            'product_name': row.product_name,
            'quantity': str(row.quantity),
            'lot_id': row.lot_id,
            'lot': row.lot,
            'user': row.user,
            'date':
            row.date.strftime("%d-%m-%Y %H:%M:%S") if row.date else None,
            # 'time': r.date.strftime("%H:%M:%S") if r.date else None,
        })

    response = {'boil': {'name': batch_data['name'],
                         'date': batch_data['date'],
                         'plant': batch_data['plant'],
                         'data': data}
                }

    return jsonify(response)


@bp.route("/api/v1/boils/load/<int:batchid>", methods=['GET'])
def boil_load_data(batchid):

    batch_data = Batch.get_name_date_plant_by_id(batchid)

    dist_cont_subqry = db.session.query(
        Load.ContainerPK
    ).filter(
        Load.BatchPK == batchid
    ).distinct().subquery()

    cont_subqry = db.session.query(
        Load.ContainerPK.label('container_id'),
        Author.AuthorPK.label('user'),
        Document.CreateDate.label('date')
    ).distinct(
        Load.ContainerPK
    ).join(
        Document, Load.DocumentPK == Document.DocumentPK
    ).join(
        Author, Document.AuthorPK == Author.AuthorPK
    ).filter(
        Load.BatchPK == batchid
    ).subquery()

    wght_subqry = db.session.query(
        Weighting.ContainerPK.label('container_id'),
        Weighting.ProductId.label('product_id'),
        Product.ProductName.label('product_name')
    ).join(
        Product, Weighting.ProductId == Product.ProductId
    ).filter(
        Weighting.ContainerPK.in_(dist_cont_subqry)
    ).subquery()

    load_qry = db.session.query(
        cont_subqry.c.user.label('user'),
        cont_subqry.c.date.label('date'),
        wght_subqry.c.product_id.label('product_id'),
        wght_subqry.c.product_name.label('product_name')
    ).join(
        wght_subqry,
        cont_subqry.c.container_id == wght_subqry.c.container_id
    ).order_by(
        wght_subqry.c.product_name
    )

    load_data = load_qry.all()

    data = []

    for row in load_data:
        data.append({
            'product_id': row.product_id,
            'product_name': row.product_name,
            'user': row.user,
            'date': row.date.strftime("%d-%m-%Y %H:%M:%S") if row.date else None,
        })

    response = {'boil': {'name': batch_data['name'],
                         'date': batch_data['date'],
                         'plant': batch_data['plant'],
                         'data': data}
                }

    return jsonify(response)
