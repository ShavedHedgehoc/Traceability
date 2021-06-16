from lxml import etree as et

author_replace_dict = {
    'Непогодин А.С': 'Непогодин А.С.',
    'Пономарёв К.А.': 'Пономарев К.А.',
    'Кудряшов К. В.': 'Кудряшов К.В.',
}


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


def get_author(tree):
    author = tree.xpath("/Document/@userId")[0]
    if author in author_replace_dict:
        return author_replace_dict[author]
    return author


def get_header(tree):
    _header = {
        'doc_id': tree.xpath("/Document/@id")[0],
        'create_date_string': tree.xpath("/Document/@createDate")[0],
        'author': get_author(tree),
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


if __name__ == '__main__':
    xlm_value = '<Document xmlns:ns0="http://schemas.cleverence.ru/clr" createDate="2018-09-23T11:09:39.0000000+03:00" lastChangeDate="2018-09-23T11:10:01.9576230+03:00" deviceId="DatalogicMemorX3-P17F02939" deviceIP="192.168.1.66" deviceName="MemorX3" documentTypeName="Vzveshivanie" id="new_30540c20-c281-4eaf-9286-a1969f041c0a" name="Взвешивание_23.09.2018_11.09.41_122" appointment="Ахметов Т.В." userId="Ахметов Т.В." userName="Ахметов Т.В." warehouseId="Основной склад"><Fields count="4"><FieldValue fieldName="Варка"><Value ns0:Type="String">870I8</Value></FieldValue><FieldValue fieldName="Выполнил"><Value ns0:Type="String">Ахметов Т.В.</Value></FieldValue><FieldValue fieldName="ШтрихкодЕмкости"><Value ns0:Type="String">98723092018110944122</Value></FieldValue><FieldValue fieldName="Аппарат"><Value ns0:Type="String">21</Value></FieldValue></Fields><States count="1"><DocumentState finished="True" finishedDate="2018-09-23T11:10:00.0000000+03:00" inProcess="False" inProcessDate="2018-09-23T11:09:39.0000000+03:00" modified="True" modifiedDate="2018-09-23T11:09:46.0000000+03:00" processingTime="00:00:19" userId="Ахметов Т.В."/></States><Tables count="0" isLazy="False" lazyCount="0"/><DeclaredItems capacity="8" count="5" isLazy="False" lazyCount="0"><DocumentItem createdBy="Device" currentQuantity="1" declaredQuantity="0" expiredDate="0001-01-01T00:00:00.0000000" firstCellId="" packingId="кг" productId="001631" registeredDate="0001-01-01T00:00:00.0000000" secondCellId="" uid="04371735-481b-4532-a774-c55dc357dca4"><Fields count="1"><FieldValue fieldName="Партия"><Value ns0:Type="String">03405176052305201811</Value></FieldValue></Fields></DocumentItem><DocumentItem createdBy="Device" currentQuantity="1" declaredQuantity="0" expiredDate="0001-01-01T00:00:00.0000000" firstCellId="" packingId="кг" productId="000049" registeredDate="0001-01-01T00:00:00.0000000" secondCellId="" uid="e6200bd4-2606-4843-a508-ce57ba5566ab"><Fields count="1"><FieldValue fieldName="Партия"><Value ns0:Type="String">03405190091608201802</Value></FieldValue></Fields></DocumentItem><DocumentItem createdBy="Device" currentQuantity="1" declaredQuantity="0" expiredDate="0001-01-01T00:00:00.0000000" firstCellId="" packingId="кг" productId="000045" registeredDate="0001-01-01T00:00:00.0000000" secondCellId="" uid="428f3d0c-1812-4f7e-b409-ccf7b769acee"><Fields count="1"><FieldValue fieldName="Партия"><Value ns0:Type="String">03405176052305201804</Value></FieldValue></Fields></DocumentItem><DocumentItem createdBy="Device" currentQuantity="1" declaredQuantity="0" expiredDate="0001-01-01T00:00:00.0000000" firstCellId="" packingId="кг" productId="000050" registeredDate="0001-01-01T00:00:00.0000000" secondCellId="" uid="4560aeb4-91e0-49db-aa62-c96d1896986e"><Fields count="1"><FieldValue fieldName="Партия"><Value ns0:Type="String">12475194341009201801</Value></FieldValue></Fields></DocumentItem><DocumentItem createdBy="Device" currentQuantity="1" declaredQuantity="0" expiredDate="0001-01-01T00:00:00.0000000" firstCellId="" packingId="кг" productId="000108" registeredDate="0001-01-01T00:00:00.0000000" secondCellId="" uid="b2df700c-ffa7-4fcd-a2a2-975ff9429f85"><Fields count="1"><FieldValue fieldName="Партия"><Value ns0:Type="String">03405192703108201806</Value></FieldValue></Fields></DocumentItem></DeclaredItems><CurrentItems capacity="8" count="5" isLazy="False" lazyCount="0"><DocumentItem blUid="04371735-481b-4532-a774-c55dc357dca4" createdBy="Device" currentQuantity="1" declaredQuantity="0" expiredDate="0001-01-01T00:00:00.0000000" firstCellId="" packingId="кг" productId="001631" registeredDate="0001-01-01T00:00:00.0000000" secondCellId="" uid="04371735-481b-4532-a774-c55dc357dca4"><Fields count="1"><FieldValue fieldName="Партия"><Value ns0:Type="String">03405176052305201811</Value></FieldValue></Fields></DocumentItem><DocumentItem blUid="e6200bd4-2606-4843-a508-ce57ba5566ab" createdBy="Device" currentQuantity="1" declaredQuantity="0" expiredDate="0001-01-01T00:00:00.0000000" firstCellId="" packingId="кг" productId="000049" registeredDate="0001-01-01T00:00:00.0000000" secondCellId="" uid="e6200bd4-2606-4843-a508-ce57ba5566ab"><Fields count="1"><FieldValue fieldName="Партия"><Value ns0:Type="String">03405190091608201802</Value></FieldValue></Fields></DocumentItem><DocumentItem blUid="428f3d0c-1812-4f7e-b409-ccf7b769acee" createdBy="Device" currentQuantity="1" declaredQuantity="0" expiredDate="0001-01-01T00:00:00.0000000" firstCellId="" packingId="кг" productId="000045" registeredDate="0001-01-01T00:00:00.0000000" secondCellId="" uid="428f3d0c-1812-4f7e-b409-ccf7b769acee"><Fields count="1"><FieldValue fieldName="Партия"><Value ns0:Type="String">03405176052305201804</Value></FieldValue></Fields></DocumentItem><DocumentItem blUid="4560aeb4-91e0-49db-aa62-c96d1896986e" createdBy="Device" currentQuantity="1" declaredQuantity="0" expiredDate="0001-01-01T00:00:00.0000000" firstCellId="" packingId="кг" productId="000050" registeredDate="0001-01-01T00:00:00.0000000" secondCellId="" uid="4560aeb4-91e0-49db-aa62-c96d1896986e"><Fields count="1"><FieldValue fieldName="Партия"><Value ns0:Type="String">12475194341009201801</Value></FieldValue></Fields></DocumentItem><DocumentItem blUid="b2df700c-ffa7-4fcd-a2a2-975ff9429f85" createdBy="Device" currentQuantity="1" declaredQuantity="0" expiredDate="0001-01-01T00:00:00.0000000" firstCellId="" packingId="кг" productId="000108" registeredDate="0001-01-01T00:00:00.0000000" secondCellId="" uid="b2df700c-ffa7-4fcd-a2a2-975ff9429f85"><Fields count="1"><FieldValue fieldName="Партия"><Value ns0:Type="String">03405192703108201806</Value></FieldValue></Fields></DocumentItem></CurrentItems></Document>'
    print(xml_parse(xlm_value))
