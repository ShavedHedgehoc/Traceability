from lxml import etree as et


def get_fields_count(tree):
    _count = tree.xpath("/Document/Fields/@count")[0]
    return _count


def get_rows_count(tree):
    try:
        doc_row_count = len(
            tree.xpath(
                "/Document/CurrentItems/DocumentItem"
            )
        )
    except:
        doc_row_count = -2
    return doc_row_count


def get_batch(tree):
    try:
        batch = tree.xpath(
            '/Document/Fields/FieldValue[@fieldName="Варка"]\
                /Value/text()')[0]
    except IndexError:
        batch = ''
    return batch


def get_container(tree):
    try:
        container = tree.xpath(
            '/Document/Fields/FieldValue[@fieldName="ШтрихкодЕмкости"]\
                /Value/text()'
        )[0]
    except IndexError:
        container = ''
    return container


def get_header(tree):
    _header = {
        'doc_id': tree.xpath("/Document/@id")[0],
        'create_date_string': tree.xpath("/Document/@createDate")[0],
        'author': tree.xpath("/Document/@userId")[0],
        'doc_type': tree.xpath("/Document/@documentTypeName")[0],
    }
    return _header


def get_fields(tree):
    _fields_count = get_fields_count(tree)
    if _fields_count == "0":
        return {}
    _fields = {
        'container': get_container(tree),
        'batch': get_batch(tree),
    }
    return _fields


def get_rows_strings(tree):
    doc_row_count = get_rows_count(tree)
    if (doc_row_count == 0) or (doc_row_count == -2):
        return []
    rows = tree.xpath("/Document/CurrentItems/DocumentItem")
    return rows


def get_product_id(one_string):
    return one_string.xpath('@productId')[0]


def get_lot(one_string):
    try:
        lot = one_string.xpath(
            'Fields/FieldValue[@fieldName="Партия"]/Value/text()'
        )[0]
    except AttributeError:
        lot = ''
    except IndexError:
        lot = ''
    return lot


def get_exp_date(one_string):
    try:
        exp_date = one_string.xpath('@expiredDate')[0]
    except IndexError:        
        exp_date = ''        
    except AttributeError:
        exp_date = ''        
    return exp_date


def get_quantity(one_string):
    return one_string.xpath('@currentQuantity')[0]


def get_packing_capasity(one_string):
    try:
        packing_capasity = one_string.xpath(
            'Fields/FieldValue[@fieldName="КоличествоВТарномМесте"]\
                /Value/text()'
        )[0]
    except AttributeError:
        packing_capasity = ''
    except IndexError:
        packing_capasity = ''
    return packing_capasity


def get_packing_quantity(one_string):
    try:
        packing_quantity = one_string.xpath(
            'Fields/FieldValue[@fieldName="КоличествоТарныхМест"]\
                /Value/text()'
        )[0]
    except AttributeError:
        packing_quantity = ''
    except IndexError:
        packing_quantity = ''
    return packing_quantity


def get_packing_name(one_string):
    try:
        packing_name = one_string.xpath(
            'Fields/FieldValue[@fieldName="ИмяТарногоМеста"]/Value/text()'
        )[0]
    except AttributeError:
        packing_name = ''
    except IndexError:
        packing_name = ''
    return packing_name


def get_packing_code(one_string):
    try:
        packing_code = one_string.xpath(
            'Fields/FieldValue[@fieldName="КодТарногоМеста"]/Value/text()'
        )[0]
    except AttributeError:
        packing_code = ''
    except IndexError:
        packing_code = ''
    return packing_code


def get_rows(tree):
    doc_strings = get_rows_strings(tree)
    rows = []
    if doc_strings == []:
        return [{}]
    for one_string in doc_strings:
        product_id = get_product_id(one_string)
        lot = get_lot(one_string)
        expire_date = get_exp_date(one_string)
        quantity = get_quantity(one_string)
        packing_capasity = get_packing_capasity(one_string)
        packing_quantity = get_packing_quantity(one_string)
        packing_name = get_packing_name(one_string)
        packing_code = get_packing_code(one_string)

        row_dict = {
            'product_id': product_id,
            'lot': lot,
            'expire_date': expire_date,
            'quantity': quantity,
            'packing_capasity': packing_capasity,
            'packing_quantity': packing_quantity,
            'packing_name': packing_name,
            'packing_code': packing_code,
        }
        rows.append(row_dict)
    return rows


def xml_parse(data):
    tree = et.XML(data)
    header = get_header(tree)
    fields = get_fields(tree)
    rows = get_rows(tree)

    result_dict = {
        'header': header,
        'fields': fields,
        'rows': rows,
    }
    return result_dict
