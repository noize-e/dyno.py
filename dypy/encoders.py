from boto3.dynamodb.types import Binary
import decimal
import json


class MultiEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)

        if isinstance(o, Binary):
            return repr(o)

        return super(MultiEncoder, self).default(o)


class DecimalEncoder(json.JSONEncoder):

    """ Helper class to convert a DynamoDB item to JSON.
    The DecimalEncoder class is used to print out numbers
    stored using the Decimal class. The Boto SDK uses the
    Decimal class to hold DynamoDB number values.
    """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)