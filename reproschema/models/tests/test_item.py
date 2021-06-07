import os, sys, json

from ..item import Item, ResponseOption

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


def test_default():

    item = Item()
    item.set_defaults()

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


# TODO
# many items types (audio ones for examples) are not yet tested because the code cannot yet generate them.

"""
text items
"""


def test_text():

    text_length = 100

    item = Item("1.0.0-rc4")
    item.set_defaults("text")
    item.set_input_type_as_text(text_length)

    item.set_question("question for text item")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


def test_multitext():

    text_length = 50

    item = Item("1.0.0-rc4")
    item.set_defaults("multitext")
    item.set_input_type_as_multitext(text_length)

    item.set_question("This is an item where the user can input several text field.")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


"""
items with a specific "type"
"""


def test_email():

    item = Item("1.0.0-rc4")
    item.set_defaults("email")
    item.set_input_type_as_email()

    item.set_question("input email address")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


def test_participant_id():

    item = Item("1.0.0-rc4")
    item.set_defaults("participant id")
    item.set_input_type_as_id()

    item.set_question("input the participant id number")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


def test_date():

    item = Item("1.0.0-rc4")
    item.set_defaults("date")
    item.set_input_type_as_date()

    item.set_question("input a date")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


def test_time_range():

    item = Item("1.0.0-rc4")
    item.set_defaults("time range")
    item.set_input_type_as_time_range()

    item.set_question("input a time range")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


def test_year():

    item = Item("1.0.0-rc4")
    item.set_defaults("year")
    item.set_input_type_as_year()

    item.set_question("input a year")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


"""
Items that refer to a preset list of responses choices
"""


def test_language():

    item = Item()
    item.set_defaults("language")
    item.set_input_type_as_language()
    item.set_question("This is an item where the user can select several language.")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


def test_country():

    item = Item()
    item.set_defaults("country")
    item.set_input_type_as_country()
    item.set_question("select a country")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


def test_state():

    item = Item()
    item.set_defaults("state")
    item.set_input_type_as_state()
    item.set_question("select a USA state")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


"""
NUMERICAL ITEMS
"""


def test_float():

    item = Item("1.0.0-rc4")
    item.set_defaults("float")
    item.set_description("This is a float item.")
    item.set_input_type_as_float()
    item.set_question("This is an item where the user can input a float.")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


def test_integer():

    item = Item()
    item.set_defaults("integer")
    item.set_description("This is a integer item.")
    item.set_input_type_as_int()
    item.set_question("This is an item where the user can input a integer.")

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


"""
SELECTION ITEMS: radio and select
tested both with:
- only one response allowed
- multiple responses allowed
"""


def test_radio():

    item = Item("1.0.0-rc4")
    item.set_defaults("radio")

    item.set_question("question for radio item", "en")

    response_options = ResponseOption()
    response_options.add_choice("Not at all", 0, "en")
    response_options.add_choice("Several days", 1, "en")
    # TODO
    # set_min and set_max cold probably be combined into a single method that gets
    # those values from the content of the choice key
    response_options.set_max(1)

    item.set_input_type_as_radio(response_options)

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)

    item.set_filename("radio multiple")
    item.set_description("radio multiple")
    item.set_pref_label("radio multiple")
    item.set_question("question for radio item with multiple responses")
    response_options.set_multiple_choice(True)
    item.set_input_type_as_radio(response_options)
    item.write(item_dir)

    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


def test_select():

    item = Item()
    item.set_defaults("select")
    item.set_question("question for select item")

    response_options = ResponseOption()
    response_options.add_choice("Response option 1", 0)
    response_options.add_choice("Response option 2", 1)
    response_options.add_choice("Response option 3", 2)
    response_options.set_max(2)

    item.set_input_type_as_select(response_options)

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)

    item.set_filename("select multiple")
    item.set_description("select multiple")
    item.set_pref_label("select multiple")
    item.set_question("question for select item with multiple responses")
    response_options.set_multiple_choice(True)
    item.set_input_type_as_select(response_options)
    item.write(item_dir)

    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


def test_slider():

    item = Item()
    item.set_defaults("slider")
    item.set_question("question for slider item", "en")

    response_options = ResponseOption()
    response_options.add_choice("not at all", 0)
    response_options.add_choice("a bit", 1)
    response_options.add_choice("so so", 2)
    response_options.add_choice("a lot", 3)
    response_options.add_choice("very much", 4)
    response_options.set_max(4)

    item.set_input_type_as_slider(response_options)

    item.write(item_dir)
    item_content, expected = load_jsons(item)
    assert item_content == expected

    clean_up(item)


"""
Just to check that item with read only values

Tries to recreate the item from
reproschema/tests/data/activities/items/activity1_total_score
"""


def test_read_only():

    item = Item()
    item.set_defaults("activity1_total_score")
    item.set_context("../../../contexts/generic")
    item.set_filename("activity1_total_score", "")
    item.schema["prefLabel"] = "activity1_total_score"
    item.set_description("Score item for Activity 1")
    item.set_read_only_value(True)
    item.set_input_type_as_int()
    item.response_options.set_max(3)
    item.response_options.set_min(0)
    item.unset(["question"])

    item.write(item_dir)

    output_file = os.path.join(item_dir, item.get_filename())
    item_content = read_json(output_file)

    # test against one of the pre existing files
    data_file = os.path.join(
        reproschema_test_data, "activities", "items", "activity1_total_score"
    )
    expected = read_json(data_file)
    assert item_content == expected

    clean_up(item)


"""
HELPER FUNCTIONS
"""


def load_jsons(item):

    output_file = os.path.join(item_dir, item.get_filename())
    item_content = read_json(output_file)

    data_file = os.path.join(my_path, "data", "items", item.get_filename())
    expected = read_json(data_file)

    return item_content, expected


def read_json(file):

    with open(file, "r") as ff:
        return json.load(ff)


def clean_up(obj):
    os.remove(os.path.join(item_dir, obj.get_filename()))
