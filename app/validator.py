class Validator():

    def validate_weighting(self, data):
        print('weighting')
        print(data)
        return True

    def validate_load(self, data):
        print('load')
        print(data)
        return True

    def validate_acceptance(self, data):
        print('acceptance')
        print(data)
        return True

    def dispatch(self, value, data):
        method_name = 'validate_' + str(value)
        method = getattr(self, method_name)
        return method(data)


def validate_data(doc_type, data):
    validator = Validator()
    result = validator.dispatch(doc_type, data)
    return result
