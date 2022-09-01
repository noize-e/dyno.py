DyPy - A AWS DynamoDB Interface
-------------------------------

### Dependencies

- boto3 (`pip install boto3`)
- whiterose (`git clone https://github.com/noize-e/whiterose`)

### Usage

#### PutItem Operation

For this example create a new DynamoDB table following a __SingleTable__ design model schema. Define the partition key as `pk` and the sort key as `sk`. Once done, open up your fav IDE and code the following

```python
from dypy.db import SingleItem
import uuid


item = SingleItem(pk='user@email.com', sk=uuid.uuid4().hex, name='Frank')
```

What we have done here is, crete a SingleItem instance which basically receives the new item attributes as named arguments (keyworded variables), also can be passed as `**kwargs` inside a  dictionary.

Now lets import the Table class and create a new instance. It receives the table name that we have already created. Then call its method __`put()`__ passing the SingleItem instance.

```python
from dypy.db import Table

...
response = Table('{Your-Table}').put(item)
```

And thats it, you had put a new item. Validate if the request was successful by calling the __ok__ property from the response object. The full code block should look like this:


```python
from dypy.db import Table, SingleItem
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
from dypy.db import Table, SecureItem
import uuid


item = SecureItem(pk='user@email.com', sk=uuid.uuid4().hex, name='Frank')
response = Table('{Your-Table}').put(item)
```

