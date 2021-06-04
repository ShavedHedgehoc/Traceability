import celery.events.state
import time
import os
from dateutil.parser import parse
from sqlalchemy.sql.expression import false
from celery_singleton import Singleton
from lxml import etree as et
from psycopg2 import OperationalError
from app import celery
from app import db
from app import models
from app import xml_parser as xp
from app.validator import validate_data 

from .models import (User,
                     XmlData,
                     Author,
                     Document,
                     Doctype,
                     Product,
                     Lot,
                     Weighting,
                     Container,
                     Batch,
                     XmlDataP
                     )


def get_id_by_name(model_name, name_value):
    try:
        local_model = getattr(models, model_name)
        record = db.session.query(local_model).filter(
            local_model.name == name_value).one_or_none()
    except TypeError:
        return -1
    if record is None:
        new_record = local_model(name=name_value)
        db.session.add(new_record)
        db.session.commit()
        get_id = new_record.id
    else:
        get_id = record.id
    return get_id


def get_doctype_id_alias(doctype_name):
    doctype = db.session.query(Doctype).filter(
        Doctype.name == doctype_name).one_or_none()
    if doctype is None:
        return -1, -1
    return doctype.id, doctype.alias


@ celery.task(base=Singleton, name='doc_reload')
def doc_reload():

    docs_limit = os.environ.get('DOCS_LIMIT')
    processed_list = []

    sub_qry = db.session.query(XmlData.id, XmlData.xml_data).filter(
        XmlData.processed == false()).limit(docs_limit)

    if sub_qry.count() < 1:
        print('No rows')
        return('No rows')
    else:
        Flag = False
        for row in sub_qry:
            if not Flag:
                start_id = row.id
                Flag = True
            NewXMLData = XmlDataP(
                xml_data=row.xml_data,
                processed=False,
                empty_doc=False,
                unsupported_doc=False
            )
            db.session.add(NewXMLData)
            db.session.commit()
            processed_list.append(row.id)
        data = {'processed': True}
        upd_qry = db.session.query(XmlData).filter(
            XmlData.id.in_(processed_list)).update(data, False)
        db.session.commit()
    print(f'End task {start_id}')


@ celery.task(name='doc_write')
def doc_write():

    docs_limit = os.environ.get('DOCS_LIMIT')
    try:
        sub_qry = db.session.query(XmlDataP.id, XmlDataP.xml_data).filter(
            XmlDataP.empty_doc == false()).filter(
            XmlDataP.processed == false()).filter(
            XmlDataP.unsupported_doc == false()).limit(docs_limit).with_for_update().all()
    except:
        return ('Lock finded')

    if len(sub_qry) == 0:
        db.session.commit()
        print('No docs')
        return ('No docs')

    processed_list = []
    unsupported_list = []
    empty_list = []

    for row in sub_qry:
        parsed_data = xp.xml_parse(row.xml_data)

        doctype_id, doctype_alias = get_doctype_id_alias(
            parsed_data['header']['doc_type']
        )
        if doctype_id == -1:
            unsupported_list.append(row.id)
        else:
            doc_valid = validate_data(doctype_alias, parsed_data)
            if doc_valid:
                processed_list.append(row.id)
            else:
                empty_list.append(row.id)
    data = {'processed': True}
    upd_qry = db.session.query(XmlDataP).filter(
        XmlDataP.id.in_(processed_list)).update(data, False)
    data = {'unsupported_doc': True}
    upd_qry = db.session.query(XmlDataP).filter(
        XmlDataP.id.in_(unsupported_list)).update(data, False)
    db.session.commit()
    print(
        f'End task processed:{len(processed_list)}, unsupported: {len(unsupported_list)}')
    return({'processed': len(processed_list),
            'unsupported': len(unsupported_list)
            })

    # parsed_data = xp.xml_parse(sub_qry.xml_data)

    # doctype_id, doctype_alias = get_doctype_id_alias(
    #     parsed_data['header']['doc_type']
    # )

    # if doctype_id == -1:
    #     print('Unsupported')
    #     status = 'unsupported_doc'
    # else:
    #     parsed_data = xp.xml_parse(sub_qry.xml_data)
    #     print(parsed_data)
    #     print('----------------------------------')
    #     status = 'processed'

    # if doctype_alias == 'Взвешивание':
    #     parsed_data = xml_parse_weighting(sub_qry.xml_data)
    #     if parsed_data['rows'] == []:
    #         print('Empty')
    #         status = 'empty_doc'
    #     else:
    #         print('Processed')
    #         status = 'processed'
    # if doctype_alias == 'Загрузка':
    #     parsed_data = xml_parse_load(sub_qry.xml_data)
    #     if parsed_data['rows'] == []:
    #         print('Empty')
    #         status = 'empty_doc'
    #     else:
    #         print('Processed')
    #         status = 'processed'

    # data = {status: True}
    # upd_qry = db.session.query(XmlDataP).filter(
    #     XmlDataP.id == catched_id).update(data, False)
    # db.session.commit()
    # print(status)
    # return (status)
