from lxml import etree as et


def xml_parse_weighting(data):
    """ Parse XML data to dictionary
        if doctype is "weighting"
    """
    tree = et.XML(data)
    doc_id = tree.xpath("/Document/@id")[0]
    create_date_string = tree.xpath("/Document/@createDate")[0]
    author = tree.xpath("/Document/@userId")[0]
    doc_type = tree.xpath("/Document/@documentTypeName")[0]
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
        "create_date_string": create_date_string,
        "container": container,
        "rows": doc_rows
    }

    return(result_dict)