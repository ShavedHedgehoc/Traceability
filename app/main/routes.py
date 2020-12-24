from flask import current_app as app
from ..extensions import db
from . import bp


from flask import render_template, redirect, url_for, jsonify

from flask_sqlalchemy.utils import sqlalchemy
from sqlalchemy import func, and_
from sqlalchemy.exc import DataError
from sqlalchemy.ext.serializer import loads, dumps

import json

from .tables import PlanTable
from app.models import Weighting, Boil, Product


@ bp.route('/')
def ind():
    return "Hello, World!"

@ bp.route('/<batchpk>')
def batch_view(batchpk):

    w_tmpqr = db.session.query(
        Weighting.BatchPK,
        Weighting.ProductId,
        func.sum(Weighting.Quantity).label('total')
    ).group_by(
        Weighting.BatchPK,
        Weighting.ProductId
    ).subquery()

    b_tmpqr = db.session.query(
        Boil.BatchPK,
        Boil.ProductId,
        func.sum(Boil.Quantity).label('plan')
    ).group_by(
        Boil.BatchPK,
        Boil.ProductId,
    ).subquery()

    boil_compare = db.session.query(
        b_tmpqr.c.ProductId.label('productid'),
        Product.ProductName.label('productname'),
        b_tmpqr.c.plan.label('plan'),
        w_tmpqr.c.total.label('fact')
    ).filter(
        b_tmpqr.c.BatchPK == batchpk
    ).join(
        Product, b_tmpqr.c.ProductId == Product.ProductId
    ).outerjoin(
        w_tmpqr,
        and_(
            b_tmpqr.c.BatchPK == w_tmpqr.c.BatchPK,
            b_tmpqr.c.ProductId == w_tmpqr.c.ProductId
        )
    )

    result = []

    for row in boil_compare.all():
        rr = {}
        for key in row.keys():
            rr[key] = str(getattr(row, key))
        result.append(rr)
    table = PlanTable(boil_compare.all())
    # print(table.__html__())
    return render_template('test.html', table=table)
    # return jsonify({"table": table})
    # json.dumps([(dict(row.items())) for row in boil_compare])
    # print(json.dumps(result, ensure_ascii=False,))

    # return json.dumps(result, ensure_ascii=False,)  # .encode('utf-8')