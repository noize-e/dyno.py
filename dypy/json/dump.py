from datetime import datetime
import pprint
import json
import sys
import os


DATA_TYPES = {
    "<class 'str'>": "S",
    "<class 'bool'>": "B",
    "<class 'int'>": "N",
    "<class 'list'>": "L",
    "<class 'dict'>": "M"
}


def iterate_list(list_items, key=None):
    items = []

    for item in list_items:
        if type(item) is dict:
            item = iterate_dictionary(item)
        if type(item) is list:
            item = {key: iterate_list(item)}
        else:
            vtype = DATA_TYPES[str(type(item))]
            item = {
                vtype: item
            }
        items.append(item)

    return {"L": items}


def iterate_dictionary(dict_items, first=False):
    items = {}

    for key, val in dict_items.items():
        if type(val) is dict:
            val = iterate_dictionary(val)
        if type(val) is list:
            val = {key: iterate_list(val, key)}
        else:
            vtype = DATA_TYPES[str(type(val))]
            val = {
                key: {
                    vtype: (lambda x: str(x) if type(x) is int else x)(val)
                }
            }

        items.update(val)

    return items


def parse_json_items(items, table_name):
    table = {table_name: []}

    for item in items:
        hour = datetime.strftime(datetime.now(), "%H")
        created_at = datetime.utcnow().isoformat()
        item.update({
            "hour": hour,
            "created_at": created_at
        })

        put_item = {
            "PutRequest": {
                "Item": iterate_dictionary(item)
            }
        }

        table[table_name].append(put_item)

    return table


def  dump_json():
    try:
        input_file = sys.argv[2]
        table_name = sys.argv[3]
    except IndexError:
        print("ValueError: Missing values 'input file path' 'dynamo table name'")
        exit(1)

    if not os.path.exists(input_file):
        print("NotFoundError: Input file not found")

    with open(input_file, "r") as jsonfile:
        json_items = list(json.load(jsonfile))

    parsed_json = parse_json_items(json_items, table_name)

    with open(f"{table_name}.json", "w+") as jsonfile:
        jsonfile.write(json.dumps(parsed_json))