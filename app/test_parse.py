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


if __name__ == '__main__':
    data = '''\
        <Document xmlns:ns0="http://schemas.cleverence.ru/clr" appointment="Син И.Х." createDate="2020-03-09T23:47:04.0000000+03:00" deviceIP="192.168.0.27" deviceId="DatalogicMemorX3-P18N00668" deviceName="MemorX3" documentTypeName="VzveshivaniePechatTest" finished="True" id="new_5d77c2f4-87ee-44f8-9d44-38f06dfa6a44" lastChangeDate="2020-03-09T23:52:33.2075140+03:00" modified="True" name="Взвешивание_09.03.2020_21.47.05_302" userId="Син И.Х." userName="Син И.Х." warehouseId="Основной склад">
  <Fields count="4">
    <FieldValue fieldName="Варка">
      <Value ns0:Type="String">318C0</Value>
    </FieldValue>
    <FieldValue fieldName="Выполнил">
      <Value ns0:Type="String">Син И.Х.</Value>
    </FieldValue>
    <FieldValue fieldName="ШтрихкодЕмкости">
      <Value ns0:Type="String">98709032020214709302</Value>
    </FieldValue>
    <FieldValue fieldName="Аппарат">
      <Value ns0:Type="String">58</Value>
    </FieldValue>
  </Fields>
  <States count="1">
    <DocumentState finished="True" finishedDate="2020-03-09T23:52:30.0000000+03:00" inProcess="False" inProcessDate="2020-03-09T23:47:04.0000000+03:00" modified="True" modifiedDate="2020-03-09T23:47:05.0000000+03:00" processingTime="00:05:25" userId="Син И.Х." />
  </States>
  <Tables count="0" isLazy="False" lazyCount="0" />
  <DeclaredItems capacity="8" count="5" isLazy="False" lazyCount="0">
    <DocumentItem createdBy="Device" currentQuantity="219.5" declaredQuantity="0" packingId="кг" productId="007891" uid="8367c38d-ba2c-409d-9e44-ff61f3c3f225">
      <Fields count="1">
        <FieldValue fieldName="Партия">
          <Value ns0:Type="String">03405274371402202003</Value>
        </FieldValue>
      </Fields>
    </DocumentItem>
    <DocumentItem createdBy="Device" currentQuantity="109.8" declaredQuantity="0" packingId="кг" productId="002049" uid="decdf998-cffd-4a56-88a8-74ffcba30b46">
      <Fields count="1">
        <FieldValue fieldName="Партия">
          <Value ns0:Type="String">08836272790602202003</Value>
        </FieldValue>
      </Fields>
    </DocumentItem>
    <DocumentItem createdBy="Device" currentQuantity="82.4" declaredQuantity="0" packingId="кг" productId="005872" uid="ffd0de9c-229a-4a2b-892c-b816abf37afc">
      <Fields count="1">
        <FieldValue fieldName="Партия">
          <Value ns0:Type="String">03405275612502202001</Value>
        </FieldValue>
      </Fields>
    </DocumentItem>
    <DocumentItem createdBy="Device" currentQuantity="27.5" declaredQuantity="0" packingId="кг" productId="010670" uid="493819fe-4e0b-4b5b-9614-9cf2cc3476aa">
      <Fields count="1">
        <FieldValue fieldName="Партия">
          <Value ns0:Type="String">03405274641702202001</Value>
        </FieldValue>
      </Fields>
    </DocumentItem>
    <DocumentItem createdBy="Device" currentQuantity="109.8" declaredQuantity="0" packingId="кг" productId="001935" uid="d6242843-c639-46b2-9d3f-074c244fba83">
      <Fields count="1">
        <FieldValue fieldName="Партия">
          <Value ns0:Type="String">08545269742101202003</Value>
        </FieldValue>
      </Fields>
    </DocumentItem>
  </DeclaredItems>
  <CurrentItems capacity="8" count="5" isLazy="False" lazyCount="0">
    <DocumentItem blUid="8367c38d-ba2c-409d-9e44-ff61f3c3f225" createdBy="Device" currentQuantity="219.5" declaredQuantity="0" packingId="кг" productId="007891" uid="8367c38d-ba2c-409d-9e44-ff61f3c3f225">
      <Fields count="1">
        <FieldValue fieldName="Партия">
          <Value ns0:Type="String">03405274371402202003</Value>
        </FieldValue>
      </Fields>
    </DocumentItem>
    <DocumentItem blUid="decdf998-cffd-4a56-88a8-74ffcba30b46" createdBy="Device" currentQuantity="109.8" declaredQuantity="0" packingId="кг" productId="002049" uid="decdf998-cffd-4a56-88a8-74ffcba30b46">
      <Fields count="1">
        <FieldValue fieldName="Партия">
          <Value ns0:Type="String">08836272790602202003</Value>
        </FieldValue>
      </Fields>
    </DocumentItem>
    <DocumentItem blUid="ffd0de9c-229a-4a2b-892c-b816abf37afc" createdBy="Device" currentQuantity="82.4" declaredQuantity="0" packingId="кг" productId="005872" uid="ffd0de9c-229a-4a2b-892c-b816abf37afc">
      <Fields count="1">
        <FieldValue fieldName="Партия">
          <Value ns0:Type="String">03405275612502202001</Value>
        </FieldValue>
      </Fields>
    </DocumentItem>
    <DocumentItem blUid="493819fe-4e0b-4b5b-9614-9cf2cc3476aa" createdBy="Device" currentQuantity="27.5" declaredQuantity="0" packingId="кг" productId="010670" uid="493819fe-4e0b-4b5b-9614-9cf2cc3476aa">
      <Fields count="1">
        <FieldValue fieldName="Партия">
          <Value ns0:Type="String">03405274641702202001</Value>
        </FieldValue>
      </Fields>
    </DocumentItem>
    <DocumentItem blUid="d6242843-c639-46b2-9d3f-074c244fba83" createdBy="Device" currentQuantity="109.8" declaredQuantity="0" packingId="кг" productId="001935" uid="d6242843-c639-46b2-9d3f-074c244fba83">
      <Fields count="1">
        <FieldValue fieldName="Партия">
          <Value ns0:Type="String">08545269742101202003</Value>
        </FieldValue>
      </Fields>
    </DocumentItem>
  </CurrentItems>
</Document>
        '''
    print(xml_parse(data))
