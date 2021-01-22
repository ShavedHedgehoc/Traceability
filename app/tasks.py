import datetime
import os
from dateutil.parser import parse
from lxml import etree as et
from sqlalchemy.sql.expression import false, true
from celery_singleton import Singleton
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


@celery.task(base=Singleton, name='base_update')
def test():
    docs_limit = os.environ.get('DOCS_LIMIT')

    doctypes = [
        ['VzveshivanieBezPechatiTest', 'Взвешивание'],
        ['VzveshivaniePechatTest', 'Взвешивание'],
        ['Vzveshivanie', 'Взвешивание'],
        ['VzveshivanieKolpino', 'Взвешивание'],
    ]
    for reserved_docktype in doctypes:
        existing_docktype = Doctype.query.filter(
            Doctype.name == reserved_docktype[0]).one_or_none()
        if existing_docktype is None:
            new_docktype = Doctype(name=reserved_docktype[0],
                                   alias=reserved_docktype[1]
                                   )
            db.session.add(new_docktype)
            db.session.commit()

    print('Start')
    not_processed_data = db.session.query(XmlData).filter(
        XmlData.processed == false()).filter(
        XmlData.empty_doc == false()).filter(
        XmlData.unsupported_doc == false()).limit(docs_limit)

    processed_count = 0
    added_count = 0
    doc_count = not_processed_data.count()
    for f in not_processed_data.all():
        processed_count += 1
        print('Processing %s documents from %s ...' %
              (processed_count, doc_count))

        tree = et.XML(f.xml_data)
        doc_id = tree.xpath("/Document/@id")[0]
        doc_type = tree.xpath("/Document/@documentTypeName")[0]
        create_date_string = tree.xpath("/Document/@createDate")[0]
        create_date = parse(create_date_string)
        author = tree.xpath("/Document/@userId")[0]

        existing_document = Document.query.filter(
            Document.doc_id == doc_id).one_or_none()

        if existing_document is None:
            pass
        else:
            f.processed = True
            db.session.commit()
            print('Skip existing document....')
            continue

        cur_items_nodes = tree.xpath(
            "/Document/CurrentItems/DocumentItem"
        )
        cur_items_count = len(cur_items_nodes)

        if cur_items_count == 0:
            f.empty_doc = True
            db.session.commit()
            print('Skip empty document....')
            continue

        doctype = Doctype.query.filter(
            Doctype.name == doc_type).one_or_none()

        if doctype is None:
            f.unsupported_doc = True
            db.session.commit()
            print('Skip unsupported document....')
            continue

        if doctype.alias == "Взвешивание":

            fields_items_nodes = tree.xpath(
                "/Document/Fields/FieldValue"
            )
            fields_items_count = len(fields_items_nodes)

            if fields_items_count == 0:
                f.error = True
                db.session.commit()
                print('Skip error document....')
                continue

            existing_author = Author.query.filter(
                Author.name == author).one_or_none()

            if existing_author is None:
                # insert restricted authors check here
                new_author = Author(name=author)
                db.session.add(new_author)
                db.session.commit()
                author_id = new_author.id
            else:
                author_id = existing_author.id

            existing_document = Document.query.filter(
                Document.doc_id == doc_id).one_or_none()

            if existing_document is not None:
                f.processed = True
                db.session.commit()
                continue
            new_doc = Document(
                doc_id=doc_id,
                doctype_id=doctype.id,
                author_id=author_id,
                date=create_date
            )
            db.session.add(new_doc)
            db.session.commit()
            print('Added new document....')
            document_id = new_doc.id
            added_count += 1

            doc_strings = tree.xpath("/Document/CurrentItems/DocumentItem")
            temp_table = []

            for string in doc_strings:
                product_id = string.get('productId')
                existing_product = Product.query.filter(
                    Product.id == product_id).one_or_none()
                if existing_product is None:
                    new_product = Product(id=product_id)
                    db.session.add(new_product)
                    db.session.commit()

                lot = string.xpath('Fields/FieldValue/Value/text()')[0]
                existing_lot = Lot.query.filter(
                    Lot.name == lot).one_or_none()
                if existing_lot is None:
                    new_lot = Lot(name=lot, product_id=product_id)
                    db.session.add(new_lot)
                    db.session.commit()
                    lot_id = new_lot.id
                else:
                    lot_id = existing_lot.id

                container = tree.xpath(
                    '/Document/Fields/FieldValue\
                    [@fieldName="ШтрихкодЕмкости"]/Value/text()')[0]
                existing_container = Container.query.filter(
                    Container.name == container).one_or_none()
                if existing_container is None:
                    new_container = Container(name=container)
                    db.session.add(new_container)
                    db.session.commit()
                    container_id = new_container.id
                else:
                    container_id = existing_container.id

                batch = tree.xpath(
                    '/Document/Fields/FieldValue\
                        [@fieldName="Варка"]/Value/text()')[0]
                existing_batch = Batch.query.filter(
                    Batch.name == batch).one_or_none()
                if existing_batch is None:
                    new_batch = Batch(name=batch)
                    db.session.add(new_batch)
                    db.session.commit()
                    batch_id = new_batch.id
                else:
                    batch_id = existing_batch.id

                quantity = float(string.get('currentQuantity'))

                new_weighting_row = Weighting(
                    document_id=document_id,
                    container_id=container_id,
                    product_id=product_id,
                    lot_id=lot_id,
                    batch_id=batch_id,
                    quantity=quantity
                )
                db.session.add(new_weighting_row)
                db.session.commit()

            f.processed = True
            db.session.commit()

        # print('id: %s' % doc_id)
        # print('doctype: %s' % doc_type)
        # print('Author: %s' % author)
        # print('Create date: %s' % create_date)

        # can_id = tree.xpath(
        #     '/Document/Fields/FieldValue[@fieldName="ШтрихкодЕмкости"]/Value/text()')[0]
        # batch = tree.xpath(
        #     '/Document/Fields/FieldValue[@fieldName="Варка"]/Value/text()')[0]

        # root = ET.fromstring(f.xml_data)
        # tree = ET.fromstring(f.xml_data)
        # for prefix, uri in ns.items():
        #     ET.register_namespace(prefix, uri)
        # root = tree.getroot()

        # doc_type = root.attrib['documentTypeName']

        # if doc_type == 'ZagruzkaEmkosteiVApparat':
        #     doc_id = root.attrib['id']
        #     batch = root.tag['Fields']

        #     print(root.attrib['id'])
        #     print(root.attrib['documentTypeName'])
        #     print(batch)
        #     # for k in root.findall("./Fields/FieldValue"):
        #     print(k.attrib['fieldName'], k)
        # print(root.attrib['documentTypeName'])

        # f.processed = False
    print('Added %s documents...' % added_count)
    print('Stop')
    return({'added': added_count})
