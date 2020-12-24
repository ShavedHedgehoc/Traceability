from flask_table import Table, Col


class PlanTable(Table):

    productid = Col('Код 1С')
    productname = Col('Наименование')
    plan = Col('План')
    fact = Col('Факт')

    no_items = u'Нет данных'
