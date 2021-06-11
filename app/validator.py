from schema import Schema, And, Use, Optional, SchemaError


class Validator():

    weighting_calling = False
    acceptance_calling = False
    load_calling = False

    def validate_weighting(self, data):

        self.weighting_calling = True

        weighting_schema = Schema(
            {
                'header':
                {
                    'doc_id': And(str, lambda s: s != ''),
                    'create_date_string': And(str, lambda s: s != ''),
                    'author': And(str, lambda s: s != ''),
                    'doc_type': And(str, lambda s: s != ''),
                },
                'fields':
                {
                    'container': And(str, lambda s: s != ''),
                    'batch': And(str, lambda s: s != ''),
                },
                'rows':
                [
                    {
                        'product_id': And(str, lambda s: s != ''),
                        'lot': And(str, lambda s: s != ''),
                        'expired_date':And(str),
                        'quantity': And(str, lambda s: s != ''),
                        'packing_capasity': And(str, lambda s: s == ''),
                        'packing_quantity': And(str, lambda s: s == ''),
                        'packing_name': And(str, lambda s: s == ''),
                        'packing_code': And(str, lambda s: s == ''),
                    },
                ]
            }
        )

        try:
            validate = weighting_schema.validate(data)
            return validate
        except:
            return False

    def validate_load(self, data):

        self.load_calling = True

        load_schema = Schema(
            {
                'header':
                {
                    'doc_id': And(str, lambda s: s != ''),
                    'create_date_string': And(str, lambda s: s != ''),
                    'author': And(str, lambda s: s != ''),
                    'doc_type': And(str, lambda s: s != ''),
                },
                'fields':
                {
                    'container': And(str, lambda s: s != ''),
                    'batch': And(str, lambda s: s != ''),
                },
                'rows':
                [
                    {
                        'product_id': And(str, lambda s: s != ''),
                        'lot': And(str, lambda s: s != ''),
                        'expired_date':And(str),
                        'quantity': And(str, lambda s: s != ''),
                        'packing_capasity': And(str, lambda s: s == ''),
                        'packing_quantity': And(str, lambda s: s == ''),
                        'packing_name': And(str, lambda s: s == ''),
                        'packing_code': And(str, lambda s: s == ''),
                    },
                ]
            }
        )

        try:
            validate = load_schema.validate(data)
            return validate
        except:
            return False

    def validate_acceptance(self, data):
        # make comparision date >2021 year
        # make validate author
        self.acceptance_calling = True

        acceptance_schema = Schema(
            {
                'header':
                {
                    'doc_id': And(str, lambda s: s != ''),
                    'create_date_string': And(str, lambda s: s != ''),
                    'author': And(str, lambda s: s != ''),
                    'doc_type': And(str, lambda s: s != ''),
                },
                'fields':
                {
                    'container': And(str, lambda s: s == ''),
                    'batch': And(str, lambda s: s == ''),
                },
                'rows':
                [
                    {
                        'product_id': And(str, lambda s: s != ''),
                        'lot': And(str, lambda s: s != ''),
                        'expired_date':And(str),
                        'quantity': And(str, lambda s: s != ''),
                        'packing_capasity': And(str, lambda s: s != ''),
                        'packing_quantity': And(str, lambda s: s != ''),
                        'packing_name': And(str, lambda s: s != ''),
                        'packing_code': And(str, lambda s: s != ''),
                    },
                ]
            }
        )

        try:
            validate = acceptance_schema.validate(data)
            return validate
        except:
            return False

    def dispatch(self, value, data):
        method_name = 'validate_' + str(value)
        method = getattr(self, method_name)
        return method(data)


def validate_data(doc_type, data):
    validator = Validator()
    result = validator.dispatch(doc_type, data)
    return result
