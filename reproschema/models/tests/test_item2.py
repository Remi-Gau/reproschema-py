import os, json, pytest
from reproschema.models.item import Item
from reproschema.validate import validate

my_path = os.path.dirname(os.path.abspath(__file__))

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


@pytest.mark.parametrize(
    "inputType, description, prefLabel, question, responseOptions",
    [
        (
            "text",
            "text",
            {"en": "text"},
            {"en": "question for text item"},
            {"maxLength": 100, "valueType": "xsd:string"},
        ),
        (
            "multitext",
            "multitext",
            {"en": "multitext"},
            {"en": "question for multitext item"},
            {"maxLength": 50, "valueType": "xsd:string"},
        ),
    ],
)
def test_text(inputType, description, prefLabel, question, responseOptions):

    item = Item(
        inputType=inputType,
        description=description,
        prefLabel=prefLabel,
        question=question,
        responseOptions=responseOptions,
    )

    item.write(item_dir, inputType + ".jsonld")
    item_content, expected = load_jsons(item)

    fp = os.path.join(item_dir, item.filename)
    validate(None, fp)
    assert item_content == expected

    clean_up(item)


@pytest.mark.parametrize(
    "inputType, prefLabel, question",
    [
        ("email", {"en": "email"}, {"en": "input email address"}),
        ("pid", {"en": "participant id"}, {"en": "input the participant id number"}),
        ("date", {"en": "date"}, {"en": "input a date"}),
        ("timeRange", {"en": "time range"}, {"en": "input a time range"}),
    ],
)
def test_specific_input_type(inputType, prefLabel, question):

    item = Item(inputType=inputType, prefLabel=prefLabel, question=question)

    item.write(item_dir, inputType + ".jsonld")
    item_content, expected = load_jsons(item)

    fp = os.path.join(item_dir, item.filename)
    validate(None, fp)
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
