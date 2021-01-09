PyARC
=====

* [Whiterose, a Date&Time Toolkit](#whiterose--a-date-time-toolkit)
    + [localtime()](#localtime--)
    + [today()](#today--)
    + [Unix Timestamps Toolkit](#unix-timestamps-toolkit)
        * [Epoch.dump()](#epochdump--)
        * [Epoch.load()](#epochload--)
        * [Epoch.now()](#epochnow--)
        * [Epoch.strfload()](#epochstrfload--)
* [DynamoDB Facade Interface](#dynamodb-facade-interface)
    + [Usage](#usage)
      - [PutItem Operation](#putitem-operation)
      - [Safe PutItem Operation](#safe-putitem-operation)

Whiterose, a Date&Time Toolkit
------------------------------

A date & time functions and classes toolkit.

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

DynamoDB Facade Interface
-------------------------

### Usage

#### PutItem Operation

Assuming the DynamoDB table is already created and following a __SingleTable__ design model schema lets put a new item, defining a mixed primary key with an extra attribute. The attributes can be passed as named arguments (keyworded variables) or a dictionary as `**kwargs` argument.

By default the key name __pk__ is used for the partition key value and __sk__ for the sort key.

```python
from nosql.dynamodb.item import SingleItem
import uuid


item = SingleItem(pk='user@email.com', sk=uuid.uuid4().hex, name='Frank')
```

Now lets import and create a new Table class intance, it receives the table name already created in DynamoDB. Then call the __put()__ passing to it the item created.

```python
from nosql.dynamodb.interface import Table

...
response = Table('{Your-Table}').put(item)
```

And thats it, you had put a new item. Validate if the request was successful by calling the __ok__ property from the response object. The full code block should look like this:


```python
from nosql.dynamodb.interface import Table
from nosql.dynamodb.item import SingleItem
import uuid


item = SingleItem(pk='user@email.com', sk=uuid.uuid4().hex, name='Frank')
response = Table('{Your-Table}').put(item)

if response.ok:
    print("Item saved", item.data())
else:
    print("Error: Item couldn't be saved")
```

#### Safe PutItem Operation

The facade provides the SecureItem class to prevent _PutItem_ operation overwrites. The implementation its the same as the previous one, just you need to replaces the SingleItem class.

```python
from nosql.dynamodb.interface import Table
from nosql.dynamodb.item import SecureItem
import uuid


item = SecureItem(pk='user@email.com', sk=uuid.uuid4().hex, name='Frank')
response = Table('{Your-Table}').put(item)
```

