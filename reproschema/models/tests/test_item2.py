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
        (
            "select",
            "select",
            {"en": "select"},
            {"en": "question for select item"},
            {
                "valueType": "xsd:integer",
                "minValue": 0,
                "maxValue": 2,
                "multipleChoice": False,
                "choices": [
                    {"name": {"en": "Response option 1"}, "value": 0},
                    {"name": {"en": "Response option 2"}, "value": 1},
                    {"name": {"en": "Response option 3"}, "value": 2},
                ],
            },
        ),
        (
            "radio",
            "radio",
            {"en": "radio"},
            {"en": "question for radio item"},
            {
                "valueType": "xsd:integer",
                "minValue": 0,
                "maxValue": 1,
                "multipleChoice": False,
                "choices": [
                    {"name": {"en": "Not at all"}, "value": 0},
                    {"name": {"en": "Several days"}, "value": 1},
                ],
            },
        ),
        (
            "slider",
            "slider",
            {"en": "slider"},
            {"en": "question for slider item"},
            {
                "valueType": "xsd:integer",
                "minValue": 0,
                "maxValue": 4,
                "multipleChoice": False,
                "choices": [
                    {"name": {"en": "not at all"}, "value": 0},
                    {"name": {"en": "a bit"}, "value": 1},
                    {"name": {"en": "so so"}, "value": 2},
                    {"name": {"en": "a lot"}, "value": 3},
                    {"name": {"en": "very much"}, "value": 4},
                ],
            },
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
        ("year", {"en": "year"}, {"en": "input a year"}),
        ("float", {"en": "float"}, {"en": "input a float"}),
        ("integer", {"en": "integer"}, {"en": "input an integer"}),
        ("selectLanguage", {"en": "language"}, {"en": "select language"}),
        ("selectState", {"en": "state"}, {"en": "select a USA state"}),
        ("selectCountry", {"en": "country"}, {"en": "select a country"}),
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
