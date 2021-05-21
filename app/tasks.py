import datetime
from celery.result import AsyncResult
import celery.events.state
import time
import pandas as pd
import os
from dateutil.parser import parse
from lxml import etree as et
from sqlalchemy.sql.expression import false, true
from celery_singleton import Singleton
from celery import uuid
from sqlalchemy import update
from app import celery
from app import db
from decimal import Decimal
from .models import (User,
                     XmlData,
                     Author,
                     Document,
                     Doctype,
                     Product,
                     Lot,
                     Weighting,
                     Container,
                     Batch
                     )


def get_doctype_id_alias(data):
    """ Return [doctype.id, doctype.alias] if exists,
        else return [-1,-1]
    """
    tree = et.XML(data)
    doctype_name = tree.xpath("/Document/@documentTypeName")[0]
    doctype = db.session.query(Doctype).filter(
        Doctype.name == doctype_name).one_or_none()
    if doctype is None:
        return -1, -1
    return doctype.id, doctype.alias


def document_exist(doc_id):
    qry = db.session.query(Document).filter(
        Document.doc_id == doc_id).one_or_none()
    if qry is None:
        return False
    return True


def get_author_id(author_name):
    """ Insert new Author in table 'Author' and return id,
        or return id if author exists
    """
    author = db.session.query(Author).filter(
        Author.name == author_name).one_or_none()
    if author is None:
        new_author = Author(name=author_name)
        db.session.add(new_author)
        db.session.commit()
        author_id = new_author.id
    else:
        author_id = author.id
    return author_id


@ celery.task(base=Singleton, name='doc_write')
def doc_write():
    sub_qry = db.session.query(XmlData.id, XmlData.xml_data).filter(
        XmlData.processed == false()).filter(
        XmlData.catched == false()).filter(
        XmlData.empty_doc == false()).filter(
        XmlData.unsupported_doc == false()).first()
    catched_id = sub_qry.id
    doctype_id, doctype_alias = get_doctype_id_alias(sub_qry.xml_data)
    if doctype_alias == "Взвешивание":
        parsed_data = xml_parse_weighting(sub_qry.xml_data)
        if parsed_data['doc_row_count'] == 0:
            data = {'empty_doc': True, 'task_id': ''}
            upd_qry = db.session.query(XmlData).filter(
                XmlData.id == catched_id).update(data, False)
        else:
            if document_exist(parsed_data['doc_id']):
                pass
            else:
                new_document = Document(
                    doc_id=parsed_data['doc_id'],
                    doctype_id=doctype_id,
                    author_id=parsed_data['author_id'],
                    date=parse(parsed_data['create_date_string'])
                )
                db.session.add(new_document)
                db.session.commit()

            data = {'processed': True, 'task_id': ''}
            upd_qry = db.session.query(XmlData).filter(
                XmlData.id == catched_id).update(data, False)
        print(parsed_data)
    else:
        data = {'unsupported_doc': True, 'task_id': ''}
        upd_qry = db.session.query(XmlData).filter(
            XmlData.id == catched_id).update(data, False)
        print('Unsupported!')
    db.session.commit()


# def get_doctype_id_alias2(doctype_name):
#     """ Return [doctype.id, doctype.alias] if exists,
#         else return [-1,-1]
#     """
#     doctype = db.session.query(Doctype).filter(
#         Doctype.name == doctype_name).one_or_none()
#     if doctype is None:
#         return -1, -1
#     return doctype.id, doctype.alias


def xml_parse_weighting(data):
    """ Parse XML data to dictionary
        if doctype is "weighting"
    """
    tree = et.XML(data)
    doc_id = tree.xpath("/Document/@id")[0]
    create_date_string = tree.xpath("/Document/@createDate")[0]
    author = tree.xpath("/Document/@userId")[0]

    doc_type = tree.xpath("/Document/@documentTypeName")[0]

    try:
        doc_row_count = len(tree.xpath("/Document/CurrentItems/DocumentItem"))
    except:
        doc_row_count = -2
    if (doc_row_count == 0) or (doc_row_count == -2):
        result_dict = {
            "doc_id": doc_id,
            "doc_type": doc_type,
            "author": author,
            "doc_row_count": doc_row_count,
            "create_date_string": create_date_string,
            "container": '',
            "rows": []
        }
        return result_dict

    container = tree.xpath(
        '/Document/Fields/FieldValue\
                             [@fieldName="ШтрихкодЕмкости"]/Value/text()')[0]

    doc_strings = tree.xpath("/Document/CurrentItems/DocumentItem")
    doc_rows = []

    for string in doc_strings:
        product_id = string.xpath('@productId')[0]
        lot = string.xpath(
            'Fields/FieldValue[@fieldName="Партия"]/Value/text()')[0]
        quantity = string.xpath('@currentQuantity')[0]
        row_dict = {
            "product_id": product_id,
            "lot": lot,
            "quantity": quantity
        }
        doc_rows.append(row_dict)

    result_dict = {
        "doc_id": doc_id,
        "doc_type": doc_type,
        "author": author,
        "author_id": get_author_id(author),
        'doc_row_count': doc_row_count,
        "create_date_string": create_date_string,
        "container": container,
        "rows": doc_rows
    }

    return(result_dict)


def xml_parse(data):
    """ Parse XML data to dictionary
    """
    tree = et.XML(data)
    doc_id = tree.xpath("/Document/@id")[0]
    doc_type = tree.xpath("/Document/@documentTypeName")[0]
    create_date_string = tree.xpath("/Document/@createDate")[0]
    create_date = parse(create_date_string)
    author = tree.xpath("/Document/@userId")[0]
    doctype_id = get_doctype_id_alias(doc_type)[0]
    doctype_alias = get_doctype_id_alias(doc_type)[1]
    try:
        doc_row_count = len(tree.xpath("/Document/CurrentItems/DocumentItem"))
    except:
        doc_row_count = -2
    # if doctype_alias == 'Взвешивание':
    #     # container = tree.xpath(
    #     #     '/Document/Fields/FieldValue\[@fieldName="ШтрихкодЕмкости"]/Value/text()')[0]
    #     doc_strings = tree.xpath("/Document/CurrentItems/DocumentItem")

    result_dict = {
        "doc_id": doc_id,
        "doc_type_id": doctype_id,
        "doc_type_alias": doctype_alias,
        "author": author,
        "create_date": create_date,
        "doc_row_count": doc_row_count

    }

    return(result_dict)


@ celery.task(base=Singleton, name='doctype_update')
def doctype_update():
    """ Update table 'doctypes' with supported documents types
    """

    doctypes = [
        ['VzveshivanieBezPechatiTest', 'Взвешивание'],
        ['VzveshivaniePechatTest', 'Взвешивание'],
        ['Vzveshivanie', 'Взвешивание'],
        ['VzveshivanieKolpino', 'Взвешивание'],
    ]
    try:
        for reserved_docktype in doctypes:
            existing_docktype = Doctype.query.filter(
                Doctype.name == reserved_docktype[0]).one_or_none()
            if existing_docktype is None:
                new_docktype = Doctype(name=reserved_docktype[0],
                                       alias=reserved_docktype[1]
                                       )
                db.session.add(new_docktype)
                db.session.commit()
    except:
        pass


@ celery.task(base=Singleton, name='dispatch', bind=True)
def dispatch(self):
    docs_limit = os.environ.get('DOCS_LIMIT')
    # Проверка мертвых задач
    sub_qry = db.session.query(XmlData.id, XmlData.xml_data).filter(
        XmlData.processed == false()).filter(
        XmlData.catched == false()).filter(
        XmlData.unsupported_doc == false()).limit(docs_limit)

    if sub_qry.count() < 1:
        print('No rows')
        return('No rows')

    unsupported_list = []
    processed_list = []
    empty_list = []
    error_list = []
    for row in sub_qry:
        parsed_data = xml_parse(row.xml_data)
        doc_type_id = parsed_data['doc_type_id']
        doc_row_count = parsed_data['doc_row_count']
        # print(parsed_data['doc_row_count'])
        if doc_row_count == 0:
            empty_list.append(row.id)
            # continue
        if doc_type_id == -1:
            unsupported_list.append(row.id)
            # continue
        # if doc_row_count == 0:
        #     empty_list.append(row.id)
        #     continue
        if doc_row_count == -2:
            error_list.append(row.id)
        processed_list.append(row.id)
    data = {'catched': False, 'processed': True, 'task_id': ''}
    upd_qry = db.session.query(XmlData).filter(
        XmlData.id.in_(processed_list)).update(data, False)
    db.session.commit()
    data2 = {'catched': False, 'unsupported_doc': True, 'task_id': ''}
    upd_qry2 = db.session.query(XmlData).filter(
        XmlData.id.in_(unsupported_list)).update(data2, False)
    db.session.commit()
    data3 = {'catched': False, 'empty_doc': True, 'task_id': ''}
    upd_qry3 = db.session.query(XmlData).filter(
        XmlData.id.in_(empty_list)).update(data3, False)
    db.session.commit()
    data4 = {'catched': False, 'error': True, 'task_id': ''}
    upd_qry4 = db.session.query(XmlData).filter(
        XmlData.id.in_(error_list)).update(data4, False)
    db.session.commit()
    print(f'Stop')


# ========================
    # catched_list = []
    # for row in sub_qry:
    #     catched_list.append(row.id)

    # task_idd = uuid()
    # data = {'catched': True, 'task_id': task_idd}
    # upd_qry = db.session.query(XmlData).filter(
    #     XmlData.id.in_(catched_list)).update(data, False)
    # db.session.commit()

    # unsupported_list = []
    # processed_list = []
    # error_list = []

    # for id in catched_list:
    #     row = XmlData.query.get(id)
    #     parsed_data = xml_parse(row.xml_data)
    #     doc_id = parsed_data['doc_id']
    #     doc_type_id = get_doctype_id(parsed_data['doc_type'])
    #     author_name = parsed_data['author']

    #     if doc_type_id == -1:
    #         unsupported_list.append(id)
    #     else:
    #         processed_list.append(id)

    # data = {'catched': False, 'processed': True, 'task_id': ''}
    # upd_qry = db.session.query(XmlData).filter(
    #     XmlData.id.in_(processed_list)).update(data, False)
    # db.session.commit()
    # data2 = {'catched': False, 'unsupported_doc': True, 'task_id': ''}
    # upd_qry2 = db.session.query(XmlData).filter(
    #     XmlData.id.in_(unsupported_list)).update(data2, False)
    # db.session.commit()
    # print(f'Stop {task_idd}')


# ===========================

    # print(
    #     f'Row {id} - {get_author_id(author_name)}, {get_doctype_id(doc_type)},{doc_id}'
    # )


# # @celery.task(base=Singleton, name='write_docs')
# # def write_docs():
# #     docs_limit = os.environ.get('DOCS_LIMIT')
# #     print('Start')

# #     not_processed_data = XmlData.query.filter(
# #         XmlData.processed == false()).filter(
# #         XmlData.empty_doc == false()).filter(
# #         XmlData.unsupported_doc == false()).limit(docs_limit)

# #     data = {'processed': True}

# #     sub_qry = db.session.query(XmlData.id, XmlData.xml_data).filter(
# #         XmlData.processed == false()
# #     ).limit(5)

# #     ll = []
# #     df = pd.read_sql(query.statement, query.session.bind)
# #     for row in sub_qry:
# #         ll.append([row.id, et.XML(row.xml_data).xpath("/Document/@id")[0]])

# #     print([item[0] for item in ll])
# #     upd_qry = db.session.query(XmlData).filter(
# #         XmlData.id.in_([item[0] for item in ll])).update(data, False)

# #     db.session.commit()
# # print('Stop')
# # for i in ll:
# #     print(i[0])
# # print('------------------')
# # for row in sub_qry:
# #     print(row.id)

# # processed_count = 0
# # added_count = 0
# # doc_count = not_processed_data.count()

# # for one_file in not_processed_data:
# #     processed_count += 1

# #     print('Processing %s documents from %s ...' %
# #           (processed_count, doc_count))

# #     tree = et.XML(one_file.xml_data)
# #     doc_id = tree.xpath("/Document/@id")[0]
# #     doc_type = tree.xpath("/Document/@documentTypeName")[0]
# #     create_date_string = tree.xpath("/Document/@createDate")[0]
# #     create_date = parse(create_date_string)
# #     author = tree.xpath("/Document/@userId")[0]

# #     exists = db.session.query(Document).filter(
# #         Document.doc_id == doc_id).scalar() is not None
# #     if exists:
# #         try:
# #             new_doc = Document(
# #                 doc_id=doc_id,
# #                 doctype_id=doctype.id,
# #                 author_id=author_id,
# #                 date=create_date
# #             )
# #             db.session.add(new_doc)
# #             one_file.processed=True
# #             db.session.commit()
# #             print('Write...')
# #             added_count+=1
# #         except:
# #             db.sesion.rollback()
# #             one_file.error=True
# #             print('Skip...rollback')
# #         finally:
# #             db.sesion.remove()
# #     else:
# #         one_file.processed = True
# #         db.session.commit()
# #         print('Skip')
# # print('Added %s documents...' % added_count)
# # print('Stop')
# # return({'added': added_count})


# @ celery.task(name='child', bind=True)
# def child(self, clist):
#     print("Start child")
#     # запуск задачи обработки
#     for id in clist:
#         row = XmlData.query.get(id)
#         row_data = row.xml_data
#         doc_id, doc_type, author_name = xml_parse(row_data)  # ['author']

#         print(get_author_id(author_name), doc_id, doc_type)

#     data = {'processed': True}
#     upd_qry_err = db.session.query(XmlData).filter(
#         XmlData.id.in_(clist)).update(data, False)
#     db.session.commit()

#     data = {'catched': False, 'task_id': ''}
#     upd_qry_err2 = db.session.query(XmlData).filter(
#         XmlData.id.in_(clist)).update(data, False)
#     db.session.commit()

#     # print(self.request.id)
#     # print(clist)
#     # time.sleep(10)

#     # # data = {'error': True, 'processed': True}
#     # data = {'processed': True}
#     # upd_qry_err = db.session.query(XmlData).filter(
#     #     XmlData.id.in_(clist)).update(data, False)
#     # db.session.commit()
#     # data = {'catched': False}
#     # upd_qry_err2 = db.session.query(XmlData).filter(
#     #     XmlData.id.in_(clist)).update(data, False)

#     # db.session.commit()
#     print("Stop child")
#     return (clist)

#     # for i in clist:
#     #     ff = XmlData.query.get(i)
#     #     author = xml_parse(ff)['author']
#     #     exists = Author.query.filter(
#     #         Author.name == author).scalar() is not None
#     #     if not exists:
#     #         new_author = Author(name=author)
#     #         try:
#     #             db.session.add(new_author)
#     #             db.session.commit()
#     #             print('Add new author %s' % author)
#     #         except:
#     #             db.session.rollback()
#     #             print('Rollback')
#     #     else:
#     #         print('Skip author %s' % author)

#     return('Ended')

#     # task = child.s(catched_list)
#     # result = task.apply_async(task_id=task_idd)

#     # except:
#     #     print('rollback')
#     #     db.session.rollback()
#     # return(catched_list)
#     # except:
#     #     db.session.rollback()
#     # print(catched_list)

#     # task = child.s(catched_list)
#     # result = task.apply_async(task_id=task_idd)
#     # task_idd = result.task_id

#     # print("running uuid: %s" % task_idd)
#     # time.sleep(10)

#     # res = AsyncResult(id=task_idd)
#     # print(res.state)

#     # print("Stop")


# @ celery.task(base=Singleton, name='base_update')
# def test():
#     docs_limit = os.environ.get('DOCS_LIMIT')

#     print('Start')

#     sub_qry = db.session.query(XmlData.id, XmlData.xml_data).filter(
#         XmlData.processed == false()).filter(
#         XmlData.empty_doc == false()).filter(
#         XmlData.unsupported_doc == false()).limit(docs_limit)

#     data = {'error': True}

#     processed_count = 0
#     added_count = 0
#     doc_count = docs_limit

#     catched_list = []
#     for row in sub_qry:
#         catched_list.append(
#             [row.id,
#              et.XML(row.xml_data).xpath("/Document/@id")[0],
#              et.XML(row.xml_data).xpath("/Document/@documentTypeName")[0]
#              ]
#         )
#     # Make field 'Error' marked
#     upd_qry = db.session.query(XmlData).filter(
#         XmlData.id.in_([item[0] for item in catched_list])).update(data, False)

#     db.session.commit()

#     exist_list = []

#     for item in catched_list:
#         existing_document = Document.query.filter(
#             Document.doc_id == item[1]).one_or_none()
#         if existing_document is None:
#             exist_list.append(item[0])
#         else:
#             print('Skip existing document....')
#             continue
#     data = {'empty_doc': True}
#     upd_qry = db.session.query(XmlData).filter(
#         XmlData.id.in_(exist_list)).update(data, False)
#     data = {'error': False, 'processed': True}
#     upd_qry = db.session.query(XmlData).filter(
#         XmlData.id.in_([item[0] for item in catched_list])).update(data, False)

#     db.session.commit()

#     # for f in not_processed_data:
#     #     processed_count += 1
#     #     print('Processing %s documents from %s ...' %
#     #           (processed_count, doc_count))

#     #     tree = et.XML(f.xml_data)
#     #     doc_id = tree.xpath("/Document/@id")[0]
#     #     doc_type = tree.xpath("/Document/@documentTypeName")[0]
#     #     create_date_string = tree.xpath("/Document/@createDate")[0]
#     #     create_date = parse(create_date_string)
#     #     author = tree.xpath("/Document/@userId")[0]

#     #     # existing_document = Document.query.filter(
#     #     #     Document.doc_id == doc_id).one_or_none()

#     #     existing_document = db.session.query(Document).filter(
#     #         Document.doc_id == doc_id).one_or_none()

#     #     if existing_document is None:
#     #         pass
#     #     else:
#     #         f.processed = True
#     #         db.session.commit()
#     #         print('Skip existing document....')
#     #         continue

#     #     cur_items_nodes = tree.xpath(
#     #         "/Document/CurrentItems/DocumentItem"
#     #     )
#     #     cur_items_count = len(cur_items_nodes)

#     #     if cur_items_count == 0:
#     #         f.empty_doc = True
#     #         db.session.commit()
#     #         print('Skip empty document....')
#     #         continue

#     #     # doctype = Doctype.query.filter(
#     #     #     Doctype.name == doc_type).one_or_none()

#     #     doctype = db.session.query(Doctype).filter(
#     #         Doctype.name == doc_type).one_or_none()

#     #     if doctype is None:
#     #         f.unsupported_doc = True
#     #         db.session.commit()
#     #         print('Skip unsupported document....')
#     #         continue

#     #     if doctype.alias == "Взвешивание":

#     #         fields_items_nodes = tree.xpath(
#     #             "/Document/Fields/FieldValue"
#     #         )
#     #         fields_items_count = len(fields_items_nodes)

#     #         if fields_items_count == 0:
#     #             f.error = True
#     #             db.session.commit()
#     #             print('Skip error document....')
#     #             continue

#     #         # existing_author = Author.query.filter(
#     #         #     Author.name == author).one_or_none()

#     #         existing_author = db.session.query(Author).filter(
#     #             Author.name == author).one_or_none()

#     #         if existing_author is None:
#     #             # insert restricted authors check here
#     #             new_author = Author(name=author)
#     #             db.session.add(new_author)
#     #             db.session.commit()
#     #             author_id = new_author.id
#     #         else:
#     #             author_id = existing_author.id

#     #         # existing_document = Document.query.filter(
#     #         #     Document.doc_id == doc_id).one_or_none()

#     #         # if existing_document is not None:
#     #         #     f.processed = True
#     #         #     db.session.commit()
#     #         #     continue
#     #         new_doc = Document(
#     #             doc_id=doc_id,
#     #             doctype_id=doctype.id,
#     #             author_id=author_id,
#     #             date=create_date
#     #         )
#     #         db.session.add(new_doc)
#     #         db.session.commit()
#     #         print('Added new document....')
#     #         document_id = new_doc.id
#     #         added_count += 1

#     #         doc_strings = tree.xpath("/Document/CurrentItems/DocumentItem")
#     #         temp_table = []

#     #         for string in doc_strings:
#     #             product_id = string.get('productId')

#     #             # existing_product = Product.query.filter(
#     #             #     Product.id == product_id).one_or_none()
#     #             existing_product = db.session.query(Product).filter(
#     #                 Product.id == product_id).one_or_none()
#     #             if existing_product is None:
#     #                 new_product = Product(id=product_id)
#     #                 db.session.add(new_product)
#     #                 db.session.commit()

#     #             lot = string.xpath('Fields/FieldValue/Value/text()')[0]
#     #             # existing_lot = Lot.query.filter(
#     #             #     Lot.name == lot).one_or_none()
#     #             existing_lot = db.session.query(Lot).filter(
#     #                 Lot.name == lot).one_or_none()
#     #             if existing_lot is None:
#     #                 new_lot = Lot(name=lot, product_id=product_id)
#     #                 db.session.add(new_lot)
#     #                 db.session.commit()
#     #                 lot_id = new_lot.id
#     #             else:
#     #                 lot_id = existing_lot.id

#     #             container = tree.xpath(
#     #                 '/Document/Fields/FieldValue\
#     #                 [@fieldName="ШтрихкодЕмкости"]/Value/text()')[0]
#     #             # existing_container = Container.query.filter(
#     #             #     Container.name == container).one_or_none()
#     #             existing_container = db.session.query(Container).filter(
#     #                 Container.name == container).one_or_none()
#     #             if existing_container is None:
#     #                 new_container = Container(name=container)
#     #                 db.session.add(new_container)
#     #                 db.session.commit()
#     #                 container_id = new_container.id
#     #             else:
#     #                 container_id = existing_container.id

#     #             batch = tree.xpath(
#     #                 '/Document/Fields/FieldValue\
#     #                     [@fieldName="Варка"]/Value/text()')[0]
#     #             # existing_batch = Batch.query.filter(
#     #             #     Batch.name == batch).one_or_none()
#     #             existing_batch = db.session.query(Batch).filter(
#     #                 Batch.name == batch).one_or_none()
#     #             if existing_batch is None:
#     #                 new_batch = Batch(name=batch)
#     #                 db.session.add(new_batch)
#     #                 db.session.commit()
#     #                 batch_id = new_batch.id
#     #             else:
#     #                 batch_id = existing_batch.id

#     #             quantity = float(string.get('currentQuantity'))

#     #             new_weighting_row = Weighting(
#     #                 document_id=document_id,
#     #                 container_id=container_id,
#     #                 product_id=product_id,
#     #                 lot_id=lot_id,
#     #                 batch_id=batch_id,
#     #                 quantity=quantity
#     #             )
#     #             db.session.add(new_weighting_row)
#     #             db.session.commit()

#     #         f.processed = True
#     #         db.session.commit()
#     # db.session.remove()

#     # print('id: %s' % doc_id)
#     # print('doctype: %s' % doc_type)
#     # print('Author: %s' % author)
#     # print('Create date: %s' % create_date)

#     # can_id = tree.xpath(
#     #     '/Document/Fields/FieldValue[@fieldName="ШтрихкодЕмкости"]/Value/text()')[0]
#     # batch = tree.xpath(
#     #     '/Document/Fields/FieldValue[@fieldName="Варка"]/Value/text()')[0]

#     # root = ET.fromstring(f.xml_data)
#     # tree = ET.fromstring(f.xml_data)
#     # for prefix, uri in ns.items():
#     #     ET.register_namespace(prefix, uri)
#     # root = tree.getroot()

#     # doc_type = root.attrib['documentTypeName']

#     # if doc_type == 'ZagruzkaEmkosteiVApparat':
#     #     doc_id = root.attrib['id']
#     #     batch = root.tag['Fields']

#     #     print(root.attrib['id'])
#     #     print(root.attrib['documentTypeName'])
#     #     print(batch)
#     #     # for k in root.findall("./Fields/FieldValue"):
#     #     print(k.attrib['fieldName'], k)
#     # print(root.attrib['documentTypeName'])

#     # f.processed = False
#     print('Added %s documents...' % added_count)
#     print('Stop')
#     return({'added': added_count})
