import os, sys, json
from ..base import SchemaBase
from ..activity_new import Activity
from ..item import Item
from reproschema.validate import validate

my_path = os.path.dirname(os.path.abspath(__file__))

# Left here in case Remi and python path or import can't be friends once again.
# sys.path.insert(0, my_path + "/../")

# TODO
# refactor across the different test modules
activity_dir = os.path.join(my_path, "activities")
if not os.path.exists(activity_dir):
    os.makedirs(os.path.join(activity_dir))

"""
Only for the few cases when we want to check against some of the files in
reproschema/tests/data
"""
reproschema_test_data = os.path.join(my_path, "..", "..", "tests", "data")


# def test_default():
#
#     """
#     FYI: The default activity does not conform to the schema
#     so  `reproschema validate` will complain if you run it in this
#     """
#
#     activity = Activity()
#     activity.set_defaults()
#
#     activity.write(activity_dir)
#     activity_content, expected = load_jsons(activity)
#     assert activity_content == expected
#
#     clean_up(activity)


def test_activity_new():

    activity = Activity(
        prefLabel="testing pref",
        description="trial",
        altLabel="test alt label",
        preamble={"en": "this is test preamble"},
        citation="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1495268/",
        image={
            "@type": "AudioObject",
            "contentUrl": "http://example.com/sample-image.png",
        },
        compute={
            "variableName": "activity1_total_score",
            "jsExpression": "item1 + item2",
        },
        shuffle=False,
    )

    item_1 = Item(prefLabel="item 1", URI="./item_1", variableName="item_1")
    activity.append_item(item_1)

    item_2 = Item(
        prefLabel="item 2", URI="./item_2", variableName="item_2", skippable=False
    )
    activity.append_item(item_2)

    item_3 = Item(
        prefLabel="activity1_total_score",
        URI="./activity1_total_score",
        variableName="activity1_total_score",
        visible=False,
    )
    activity.append_item(item_3)

    activity.write(activity_dir, "activity2_schema.jsonld")
    activity_content, expected = load_jsons(activity)

    fp = os.path.join(activity_dir, "activity2_schema.jsonld")
    validate(None, fp)
    assert activity_content == expected

    # clean_up(activity)


# TODO
# probably want to have items/item_name be a default
# item_1.set_URI(os.path.join("items", item_1.get_filename()))

# TODO
# We probably want a method to change those values rather that modifying
# the instance directly
# item_1.skippable = False
# item_1.required = True


"""
HELPER FUNCTIONS
"""


def load_jsons(obj):
    output_file = os.path.join(activity_dir, "activity2_schema.jsonld")
    content = read_json(output_file)

    data_file = os.path.join(my_path, "data", "activities", "activity2_schema.jsonld")
    expected = read_json(data_file)

    return content, expected


def read_json(file):
    with open(file, "r") as ff:
        return json.load(ff)


def clean_up(obj):
    os.remove(os.path.join(activity_dir, obj.get_filename()))
