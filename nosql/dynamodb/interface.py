from .item import Item
import traceback
import boto3
import json


def debug(func=None):
    def wrapper(*args, **kwargs):
        try:
            print("-- Debug: {} --".format(func.__name__))
            for key, value in kwargs.items():
                print("{}: {}".format(key, value))
            print("")
            return func(*args, **kwargs)
        except Exception as err:
            print("{}".format(err))
            # print(traceback.format_exc())
    return wrapper


class Connector(object):
    conns = {
        "resource": None,
        "client": None
    }

    @classmethod
    def connect(cls, conn_type: str):
        connection = cls.conns.get(conn_type)
        if bool(connection):
            return connection
        else:
            return (boto3.__getattribute__(conn_type))('dynamodb')


class Response(object):
    def __init__(self, data):
        self.rawdata = data

        """
        ResponseMetadata:
            RequestId: "LT9DLNDBNPGFSOTPT7Q474OGTJVV4KQNSO5AEMVJF66Q9ASUAAJG",
            HTTPStatusCode: 200,
            HTTPHeaders:
                server: "Server",
                date: "Wed, 06 Jan 2021 08:29:19 GMT",
                content-type: "application/x-amz-json-1.0",
                content-length: "49",
                connection: "keep-alive",
                x-amzn-requestid: "LT9DLNDBNPGFSOTPT7Q474OGTJVV4KQNSO5AEMVJF66Q9ASUAAJG",
                x-amz-crc32: "568409600"
            RetryAttempts: 0

        Item:
            created_at: "1609921283.235505"
        """

        for key, value in data.items():
            # setattr(self, key, value)
            if key not in ["Item", "Items"]:
                if type(value) is dict:
                    child = type(key, (object,), {})
                    setattr(self, key, child)
                    self.load_attrs(child, value)
                else:
                    setattr(self, key, value)

        self.Item = data.get("Item", None)
        self.Items = data.get("Items", None)

    def load_attrs(self, parent, data):
        for key, value in data.items():
            if type(value) is dict:
                child = type(key, (object,), {})
                setattr(parent, key, child)
                self.load_attrs(child, value)
            else:
                setattr(parent, key, value)

    def item_found(self):
        return bool(self.Item)

    @property
    def ok(self):
        return self.ResponseMetadata.HTTPStatusCode == 200

    def __str__(self):
        return "{}\n{}".format(type(self), dir(self))



class Client(object):
    def __init__(self):
        self.client = Connector.connect('client')

    def table_exists(self, name):
        try:
            return self.client.describe_table(
                TableName=name
            )
        except:
            return False

    def create_table(self, name):
        self.table = self.client.create_table(
            TableName=name,
            KeySchema=[
                {
                    'AttributeName': 'pk',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'sk',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'pk',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'sk',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table exists.
        self.table.meta.client.get_waiter('table_exists').wait(TableName=name)


class Table(object):

    """ DynamoDB table resource and client connector class """

    CONSUMED_CAPACITY = "TOTAL"
    ARGS_KEYS = (
        "Item",
        "Key",
        "IndexName",
        "ConditionExpression",
        "ExpressionAttributeNames",
        "ProjectionExpression",
        "KeyConditionExpression")

    def __init__(self, name):
        self.name = name
        self.resource = Connector.connect("resource")
        self.table = self.resource.Table(self.name)

    @classmethod
    def args_valid(cls, **kwargs):
        return all(key in cls.ARGS_KEYS for key in kwargs.keys())

    # @debug
    def put(self, item: Item):
        """ PutItem operation proxy """

        attributes = item()
        if self.args_valid(**attributes):
            return Response(self.table.put_item(**attributes))
        return None

    # @debug
    def get(self, item: Item):
        """ GetItem operation proxy

        Expected key=val atrributes:
            Key, ProjectionExpression, ExpressionAttributeNames
        """

        attributes = item()
        if self.args_valid(**attributes):
            attributes.update(ReturnConsumedCapacity=self.CONSUMED_CAPACITY)
            response = Response(self.table.get_item(**attributes))
            item.load(response)
            return response
        return None

    # @debug
    def delete(self, item: Item):
        """ DeleteItem operation proxy

        Expected key=val atrributes:
            Key=dict()
        """

        attributes = item()
        if self.args_valid(**attributes):
            return Response(self.table.delete_item(**attributes))
        return None

    # @debug
    def query(self, query):
        """ table items query operation proxy

        kwargs:
            KeyConditionExpression, IndexName
        """

        attributes = query()
        if self.args_valid(**attributes):
            response = Response(self.table.query(**attributes))
            query.load(response)
            return response
        return None