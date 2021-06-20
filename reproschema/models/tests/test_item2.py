import os, sys, json

# from ..item import Item, ResponseOption
from reproschema.models.item import Item

my_path = os.path.dirname(os.path.abspath(__file__))

# Left here in case Remi and python path or import can't be friends once again.
# sys.path.insert(0, my_path + "/../")

# TODO
# refactor across the different test modules
item_dir = os.path.join(my_path, "items")
if not os.path.exists(item_dir):
    os.makedirs(os.path.join(item_dir))

"""
Only for the few cases when we want to check against some of the files in
reproschema/tests/data
"""
reproschema_test_data = os.path.join(my_path, "..", "..", "tests", "data")


"""
text items
"""


def test_text():

    item = Item(
        inputType="text",
        prefLabel={"en": "text"},
        question={"en": "question for text item"},
        responseOptions={"maxLength": 100, "valueType": "xsd:string"},
        description="text",
    )

    item.write(item_dir, "text.jsonld")
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


"""
HELPER FUNCTIONS
"""


def load_jsons(item):

    output_file = os.path.join(item_dir, item.filename)
    item_content = read_json(output_file)

    data_file = os.path.join(my_path, "data", "items", item.filename)
    expected = read_json(data_file)

    return item_content, expected


def read_json(file):

    with open(file, "r") as ff:
        return json.load(ff)


def clean_up(item):
    os.remove(os.path.join(item_dir, item.filename))
