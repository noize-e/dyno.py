# DyPy

A python client designed to work with AWS DynamoDB following the __SingleTable__ schema model.


## Ops 

### PutItem

This operation requires a partition key and optionally a sort key.

```python
from dypy.db import SingleItem
import uuid


item = SingleItem(pk='user@email.com', sk=uuid.uuid4().hex, name='Frank')
```

Create a new `Table` instance, call the `put` method passing the `SingleItem` object to execute the operation.


```python
...

response = Table('TableName').put(item)
```

Use the __`ok`__ attribute to validate if the request was successful.

```python
...

if response.ok:
    print("Item saved", item.data())
```

### Secure PutItem

The __`SecureItem`__ prevents items overwriting. 

```python
from dypy.db import SecureItem

item = SecureItem(pk='user@email.com', sk=uuid.uuid4().hex, name='Frank')
response = Table('TableName').put(item)
```

## DynamoDB-JSON Parse

### Convert JSON to DynamoJSON

Usage

```bash 
# shell command
dynamojson --dump 'your.json' 'TableName' 
```

```json
[
  {
    "uid": 1,
    "salt": "$2B$12$Pfsv3Tw6Rakclh/Ustdc3U",
    "media": { 
      "content": "/media1/live-radio-session-1.m3u8",
    }
  }
]
```

Dump:

```json
{
  "TableName": [
    {
      "PutRequest": {
        "Item": {
          "uid": {
            "N": "1"
          },
          "salt": {
            "S": "$2B$12$Pfsv3Tw6Rakclh/Ustdc3U"
          },
          "media": {
            "M": {
              "content": {
                "S": "/media1/live-radio-session-1.m3u8"
              }
            }
          }
        }
      }
    }
  ]
}
```
