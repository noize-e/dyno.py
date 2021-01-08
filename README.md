# PyARC

## Module Whiterose

Date & time toolkit module.

### localtime()

```python
>>> localtime()
time.struct_time(...)
```

### today()

```python
>>> today('UTC')
'2020/12/18T22:24:58'
>>> today('MX')
'2020/12/18T16:24:58'
```

### Unix Timestamps Toolkit

##### Epoch.dump()

```python
>>> Epoch.dump(2020, 12, 18, 16)
1608328800.0
```

##### Epoch.load()

```python
>>> tms = Epoch.load(epoch)
'2020-12-18 16:24:58.109826'
>>> type(tms)
"<class 'datetime.datetime'>"
```

##### Epoch.now()

```python
>>> Epoch.now()
1608330298.110156
```

##### Epoch.strfload()

```python
>>> Epoch.strfload(1608330298.110156, datetime=True)
'2020/12/18T16:24:58'
>>> Epoch.strfload(1608330298.110156, datetime=False)
'2020/12/18'
```

## Module DynamoDB

Lets put a single item in an DynamoDB table.

Create an Item instance and pass the attributes as named arguments (keyworded variables):

```python
from nosql.dynamodb.interface import Client, Table
from nosql.dynamodb.item import SingleItem
import uuid


item = SingleItem(pk='user@email.com', sk=uuid.uuid4().hex, name='Frank')
response = Table(TableName).put(item)

if response.ok:
    print("Item saved", item.data())
else:
    print("Error: Item couldn't be saved")
```

