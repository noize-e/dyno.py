from pprint import pprint
import json
import sys
import os


DATA_TYPES = {
    "S": lambda x: str(x),
    "B": lambda x: bool(x),
    "N": lambda x: str(x),
    "L": lambda x: cast_value_by_type(x),
    "M": lambda x: cast_value_by_type(x),
}

# ----

def cast_value_by_type(raw):
    raw_type = type(raw)

    if raw_type is list:
        raw_list = []
        for index in raw:
            raw_list.append(cast_value_by_type(index))
        raw = raw_list
        return raw
                
    elif raw_type is dict:
        for key in raw.keys():
            try:
                raw = DATA_TYPES[key](raw[key])
                break
            except:
                raw[key] = cast_value_by_type(raw[key])
        return raw

    else:
        return raw


# ----

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except Exception:
        print("Missing filename arg at index 0")
        exit()

    file_path = "{}/{}.json".format(
            os.getcwd(), filename)
    dump_path = "{}/dump-{}.json".format(
        os.getcwd(), filename)

    dynamo_schema = json.loads(open(file_path, 'r').read())
    dump_file = open(dump_path, 'w')
    dump_file.write(
        json.dumps(cast_value_by_type(dynamo_schema), indent=4))
    dump_file.close()
