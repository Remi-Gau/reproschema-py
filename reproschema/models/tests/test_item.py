"""
SELECTION ITEMS: radio and select
tested both with:
- only one response allowed
- multiple responses allowed
"""


def test_radio():

    item = Item("1.0.0-rc4")
    item.set_defaults("radio")
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
