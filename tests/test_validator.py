import unittest
from app import validator
from app.validator import Validator


class Validator_test(unittest.TestCase):
    def test_dispatch(self):
        new_obj = Validator()
        new_obj.dispatch('weighting', [])
        self.assertTrue(new_obj.weighting_calling)
        new_obj.dispatch('load', [])
        self.assertTrue(new_obj.load_calling)
        new_obj.dispatch('acceptance', [])
        self.assertTrue(new_obj.acceptance_calling)

    def test_weighting_validation(self):

        empty_dict = {}
        self.assertFalse(validator.validate_data('weighting', empty_dict))

        dict_with_empty_fields = {'header':
                                  {'doc_id': '23442-ffggg-eeeer-555555',
                                   'create_date_string': '22-05-2021',
                                   'author': 'Иванов А.А.',
                                   'doc_type': 'Vzveshianie',
                                   },
                                  'fields': {},
                                  'rows': [
                                      {'product_id': '000334',
                                       'lot': '12345678901234567890',
                                       'quantity': '15.6',
                                       'packing_capasity': '',
                                       'packing_quantity': '',
                                       'packing_name': '',
                                       'packing_code': '',
                                       },
                                      {'product_id': '000335',
                                       'lot': '12345678901234567890',
                                       'quantity': '0.6',
                                       'packing_capasity': '',
                                       'packing_quantity': '',
                                       'packing_name': '',
                                       'packing_code': '', }
                                  ],
                                  }
        self.assertFalse(validator.validate_data(
            'weighting', dict_with_empty_fields))

        dict_with_empty_rows = {'header':
                                {'doc_id': '23442-ffggg-eeeer-555555',
                                 'create_date_string': '22-05-2021',
                                 'author': 'Иванов А.А.',
                                 'doc_type': 'Vzveshianie',
                                 },
                                'fields': {
                                    'container': '123456789',
                                    'batch': '123A3',
                                },
                                'rows': [{}],
                                }
        self.assertFalse(validator.validate_data(
            'weighting', dict_with_empty_rows))

        dict_with_empty_fields_and_rows = {'header':
                                           {'doc_id': '23442-ffggg-eeeer-555555',
                                            'create_date_string': '22-05-2021',
                                            'author': 'Иванов А.А.',
                                            'doc_type': 'Vzveshianie',
                                            },
                                           'fields': {},
                                           'rows': [{}],
                                           }
        self.assertFalse(validator.validate_data(
            'weighting', dict_with_empty_fields_and_rows))

        good_dict = {'header':
                     {'doc_id': '23442-ffggg-eeeer-555555',
                      'create_date_string': '22-05-2021',
                      'author': 'Иванов А.А.',
                      'doc_type': 'Vzveshianie',
                      },
                     'fields': {
                         'container': '123456789',
                         'batch': '123A3',
                     },
                     'rows': [
                         {'product_id': '000334',
                          'lot': '12345678901234567890',
                          'quantity': '15.6',
                          'packing_capasity': '',
                          'packing_quantity': '',
                          'packing_name': '',
                          'packing_code': '',
                          },
                         {'product_id': '000335',
                          'lot': '12345678901234567890',
                          'quantity': '0.6',
                          'packing_capasity': '',
                          'packing_quantity': '',
                          'packing_name': '',
                          'packing_code': '', }

                     ],
                     }
        self.assertTrue(validator.validate_data('weighting', good_dict))

    def test_load_validation(self):

        empty_dict = {}
        self.assertFalse(validator.validate_data('load', empty_dict))

        dict_with_empty_fields = {'header':
                                  {'doc_id': '23442-ffggg-eeeer-555555',
                                   'create_date_string': '22-05-2021',
                                   'author': 'Иванов А.А.',
                                   'doc_type': 'ZagruzkaEmkosteiVApparat',
                                   },
                                  'fields': {},
                                  'rows': [
                                      {'product_id': '000334',
                                       'lot': '12345678901234567890',
                                       'quantity': '15.6',
                                       'packing_capasity': '',
                                       'packing_quantity': '',
                                       'packing_name': '',
                                       'packing_code': '',
                                       },
                                      {'product_id': '000335',
                                       'lot': '12345678901234567890',
                                       'quantity': '0.6',
                                       'packing_capasity': '',
                                       'packing_quantity': '',
                                       'packing_name': '',
                                       'packing_code': '', }

                                  ],
                                  }
        self.assertFalse(validator.validate_data(
            'load', dict_with_empty_fields))

        dict_with_empty_rows = {'header':
                                {'doc_id': '23442-ffggg-eeeer-555555',
                                 'create_date_string': '22-05-2021',
                                 'author': 'Иванов А.А.',
                                 'doc_type': 'Vzveshianie',
                                 },
                                'fields': {
                                    'container': '123456789',
                                    'batch': '123A3',
                                },
                                'rows': [{}],
                                }
        self.assertFalse(validator.validate_data(
            'load', dict_with_empty_rows))

        dict_with_empty_fields_and_rows = {'header':
                                           {'doc_id': '23442-ffggg-eeeer-555555',
                                            'create_date_string': '22-05-2021',
                                            'author': 'Иванов А.А.',
                                            'doc_type': 'Vzveshianie',
                                            },
                                           'fields': {},
                                           'rows': [{}],
                                           }
        self.assertFalse(validator.validate_data(
            'load', dict_with_empty_fields_and_rows))

        good_dict = {'header':
                     {'doc_id': '23442-ffggg-eeeer-555555',
                      'create_date_string': '22-05-2021',
                      'author': 'Иванов А.А.',
                      'doc_type': 'Vzveshianie',
                      },
                     'fields': {
                         'container': '123456789',
                         'batch': '123A3',
                     },
                     'rows': [
                         {'product_id': '000334',
                          'lot': '12345678901234567890',
                          'quantity': '15.6',
                          'packing_capasity': '',
                          'packing_quantity': '',
                          'packing_name': '',
                          'packing_code': '',
                          },
                         {'product_id': '000335',
                          'lot': '12345678901234567890',
                          'quantity': '0.6',
                          'packing_capasity': '',
                          'packing_quantity': '',
                          'packing_name': '',
                          'packing_code': '', }
                     ],
                     }
        self.assertTrue(validator.validate_data('load', good_dict))

    def test_acceptance_validation(self):

        empty_dict = {}
        self.assertFalse(validator.validate_data('acceptance', empty_dict))

        dict_with_empty_fields = {'header':
                                  {'doc_id': '23442-ffggg-eeeer-555555',
                                   'create_date_string': '22-05-2021',
                                   'author': 'Иванов А.А.',
                                   'doc_type': 'ZagruzkaEmkosteiVApparat',
                                   },
                                  'fields': {},
                                  'rows': [
                                      {'product_id': '000334',
                                       'lot': '12345678901234567890',
                                       'quantity': '1',
                                       'packing_capasity': '100',
                                       'packing_quantity': '5',
                                       'packing_name': 'Бочка 200л',
                                       'packing_code': '1',
                                       },
                                      {'product_id': '000335',
                                       'lot': '12345678901234567890',
                                       'quantity': '1',
                                       'packing_capasity': '100',
                                       'packing_quantity': '6',
                                       'packing_name': 'Куб (1000)',
                                       'packing_code': '15', }

                                  ],
                                  }
        self.assertFalse(validator.validate_data(
            'acceptance', dict_with_empty_fields))

        dict_with_empty_rows = {'header':
                                {'doc_id': '23442-ffggg-eeeer-555555',
                                 'create_date_string': '22-05-2021',
                                 'author': 'Иванов А.А.',
                                 'doc_type': 'Vzveshianie',
                                 },
                                'fields': {
                                    'container': '',
                                    'batch': '',
                                },
                                'rows': [{}],
                                }
        self.assertFalse(validator.validate_data(
            'acceptance', dict_with_empty_rows))

        dict_with_empty_fields_and_rows = {'header':
                                           {'doc_id': '23442-ffggg-eeeer-555555',
                                            'create_date_string': '22-05-2021',
                                            'author': 'Иванов А.А.',
                                            'doc_type': 'Vzveshianie',
                                            },
                                           'fields': {},
                                           'rows': [{}],
                                           }
        self.assertFalse(validator.validate_data(
            'acceptance', dict_with_empty_fields_and_rows))

        good_dict = {'header':
                     {'doc_id': '23442-ffggg-eeeer-555555',
                      'create_date_string': '22-05-2021',
                      'author': 'Иванов А.А.',
                      'doc_type': 'Vzveshianie',
                      },
                     'fields': {
                         'container': '',
                         'batch': '',
                     },
                     'rows': [
                         {'product_id': '000334',
                          'lot': '12345678901234567890',
                          'quantity': '1',
                          'packing_capasity': '15',
                          'packing_quantity': '10',
                          'packing_name': 'Бочка 200 л',
                          'packing_code': '3',
                          },
                         {'product_id': '000335',
                          'lot': '12345678901234567890',
                          'quantity': '1',
                          'packing_capasity': '5',
                          'packing_quantity': '12',
                          'packing_name': 'Куб 1000 л',
                          'packing_code': '6', }
                     ],
                     }
        self.assertTrue(validator.validate_data('acceptance', good_dict))


if __name__ == '__main__':
    unittest.main()
