from boto3.dynamodb.conditions import Key, Attr


class ConditionalKey(object):
    KEY_CONDITIONS=("begins_with",
                    "between",
                    "eq",
                    "gt",
                    "gte",
                    "lt",
                    "lte")

    def __init__(self, query, key):
        self.key = key
        self.query = query

    def __getattr__(self, attr):
        if attr not in self.KEY_CONDITIONS:
            raise ValueError("Attribute not found")

        def wrapper(*args, **kwargs):
            self.query.conditions.append(Key(self.key).__getattribute__(attr)(*args))

        return wrapper


class QueryKey(object):
    def __init__(self):
        self.conditions = []
        self.index_name = None

        self.__setattr__('pk', ConditionalKey(self, 'pk'))
        self.__setattr__('sk', ConditionalKey(self, 'sk'))

    def index(self, key, name):
        self.index_name = name
        self.__setattr__(key, ConditionalKey(self, key))

    def __call__(self):
        for condition in self.conditions:
            try:
                key_conditions &= condition
            except:
                key_conditions = condition

        data = dict(KeyConditionExpression=key_conditions)

        if self.index_name:
            data.update(IndexName=self.index_name)

        return data

    def load(self, response):
        self.has_items = bool(len(response.Items))
        if self.has_items:
            self.items = response.Items