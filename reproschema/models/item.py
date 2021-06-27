import attr, json, os
from reproschema.models.base import SchemaBase
from collections import OrderedDict


SCHEMA_ORDER = [
    "@context",
    "@type",
    "@id",
    "prefLabel",
    "altLabel",
    "about",
    "description",
    "schemaVersion",
    "version",
    "question",
    "citation",
    "image",
    "audio",
    "video",
    "ui",
    "responseOptions",
]


@attr.s
class Item(SchemaBase):
    def check_labels(self, attribute, value):

        if not isinstance(value, (str, dict)):
            raise ValueError(
                f"{attribute.name} must be a string or a dict! Got {type(value)}"
            )

    question = attr.ib(default=None, validator=attr.validators.optional(check_labels))

    inputType = attr.ib(default=None, validator=attr.validators.instance_of(str))

    URI = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )

    variableName = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )

    responseOptions = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(dict)),
    )

    readonlyValue = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(bool)),
    )
    isPartOf = attr.ib(default=attr.Factory(list))
    additionalNotesObj = attr.ib(
        default=attr.Factory(list),
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(dict),
            iterable_validator=attr.validators.instance_of(list),
        ),
    )
    skippable = attr.ib(default=True)
    visible = attr.ib(default=True)
    required = attr.ib(default=True)

    _schemaType = attr.ib(default="reproschema:Field")

    def __attrs_post_init__(self):

        if self.inputType in ["email", "pid"]:
            self.responseOptions = {"valueType": "xsd:string"}
        elif self.inputType in ["date", "year"]:
            self.responseOptions = {"valueType": "xsd:date"}
        elif self.inputType in ["timeRange"]:
            self.responseOptions = {"valueType": "xsd:datetime"}
        elif self.inputType in ["integer"]:
            self.responseOptions = {"valueType": "xsd:integer"}
        elif self.inputType in ["float"]:
            self.responseOptions = {"valueType": "xsd:float"}
        elif self.inputType in ["selectLanguage"]:
            self.responseOptions = {
                "valueType": "xsd:string",
                "choices": "https://raw.githubusercontent.com/ReproNim/reproschema-library/master/resources/languages.json",
            }
        elif self.inputType in ["selectCountry"]:
            self.responseOptions = {
                "valueType": "xsd:string",
                "choices": "https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-name.json",
            }
        elif self.inputType in ["selectState"]:
            self.responseOptions = {
                "valueType": "xsd:string",
                "choices": "https://gist.githubusercontent.com/mshafrir/2646763/raw/8b0dbb93521f5d6889502305335104218454c2bf/states_hash.json",
            }

        if self.inputType in ["integer"]:
            self.inputType = "number"

    def write(self, output_dir, filename):
        """
        Reused by the write method of the children classes
        """
        schema = {
            "@context": "https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc4/contexts/generic",
            "@type": str(self._schemaType),
            "@id": filename,
        }

        props = self.__dict__.copy()

        ui_obj = {"inputType": props["inputType"]}
        ui_obj = {key: value for key, value in ui_obj.items() if bool(value)}
        del props["inputType"]

        props.update(schema)
        props.update({"ui": ui_obj})

        # store filename to make sure it can be accessed at the activity level
        self.filename = filename

        props = {key: value for key, value in props.items() if bool(value)}

        reordered_dict = reorder_dict_skip_missing(props, SCHEMA_ORDER)

        with open(os.path.join(output_dir, filename), "w") as ff:
            json.dump(reordered_dict, ff, indent=4)


def reorder_dict_skip_missing(old_dict, key_list):
    """
    reorders dictionary according to ``key_list``
    removing any key with no associated value
    or that is not in the key list
    """
    return OrderedDict((k, old_dict[k]) for k in key_list if k in old_dict)


# # from .base import SchemaBase
# from reproschema.models.base import SchemaBase
# # import base
#
# DEFAULT_LANG = "en"
#
#
#     def set_filename(self, name, ext=".jsonld"):
#         """
#         Note there is no _schema suffix for items names
#         """
#         name = name.replace(" ", "_")
#         self.schema_file = name + ext
#         self.schema["@id"] = name + ext
#
#     def set_question(self, question, lang=DEFAULT_LANG):
#         # TODO add test to check adding several questions to an item
#         self.schema["question"][lang] = question
#
#     """
#     CREATE DIFFERENT ITEMS
#     """
#     # TODO: items not yet covered
#     # audioCheck: AudioCheck/AudioCheck.vue
#     # audioRecord: WebAudioRecord/Audio.vue
#     # audioPassageRecord: WebAudioRecord/Audio.vue
#     # audioImageRecord: WebAudioRecord/Audio.vue
#     # audioRecordNumberTask: WebAudioRecord/Audio.vue
#     # audioAutoRecord: AudioCheckRecord/AudioCheckRecord.vue
#     # documentUpload: DocumentUpload/DocumentUpload.vue
#     # save: SaveData/SaveData.vue
#     # static: Static/Static.vue
#     # StaticReadOnly: Static/Static.vue
#
#     """
#     input types with 'different response choices'
#
#     Those methods require an instance of ResponseOptions as input and
#     it will replace the one initialized in the construction.
#
#     Most likely a bad idea and a confusing API from the user perpective:
#     probably better to set the input type and then let the user construct
#     the response choices via calls to the methods of
#
#         self.response_options
#     """
#
#     def set_input_type_as_radio(self, response_options):
#         self.set_input_type("radio")
#         response_options.set_type("integer")
#         self.response_options = response_options
#
#     def set_input_type_as_select(self, response_options):
#         self.set_input_type("select")
#         response_options.set_type("integer")
#         self.response_options = response_options
#
#     def set_input_type_as_slider(self, response_options):
#         self.set_input_type("slider")
#         response_options.set_type("integer")
#         self.response_options = response_options
#
#     """
#     UI
#     """
#     # are input_type and read_only specific properties to items
#     # or should they be brought up into the base class?
#     # or be made part of an UI class?
#
#
#
#     def set_read_only_value(self, value):
#         self.schema["ui"]["readonlyValue"] = value
#
#     """
#     writing, reading, sorting, unsetting
#     """
#
#     def set_response_options(self):
#         """
#         Passes the content of the response options to the schema of the item.
#         To be done before writing the item
#         """
#         self.schema["responseOptions"] = self.response_options.options
#
#     def unset(self, keys):
#         """
#         Mostly used to remove some empty keys from the schema. Rarely used.
#         """
#         for i in keys:
#             self.schema.pop(i, None)
#
#     def write(self, output_dir):
#         self.sort()
#         self.set_response_options()
#         self._SchemaBase__write(output_dir)
#
#     def sort(self):
#         schema_order = [
#             "@context",
#             "@type",
#             "@id",
#             "prefLabel",
#             "description",
#             "schemaVersion",
#             "version",
#             "ui",
#             "question",
#             "responseOptions",
#         ]
#         self.sort_schema(schema_order)
#
#
# class ResponseOption(SchemaBase):
#     """
#     class to deal with reproschema response options
#     """
#
#     # TODO
#     # the dictionnary that keeps track of the content of the response options should
#     # be called "schema" and not "options" so as to be able to make proper use of the
#     # methods of the parent class and avoid copying content between
#     #
#     # self.options and self.schema
#
#     schema_type = "reproschema:ResponseOption"
#
#     def __init__(self):
#         self.options = {
#             "valueType": "",
#             "minValue": 0,
#             "maxValue": 0,
#             "choices": [],
#             "multipleChoice": False,
#         }
#
#     def set_defaults(self, name="valueConstraints", version=None):
#         super().__init__(version)
#         self.options["@context"] = self.schema["@context"]
#         self.options["@type"] = self.schema_type
#         self.set_filename(name)
#
#     def set_filename(self, name, ext=".jsonld"):
#         name = name.replace(" ", "_")
#         self.schema_file = name + ext
#         self.options["@id"] = name + ext
#
#     def unset(self, keys):
#         if type(keys) == str:
#             keys = [keys]
#         for i in keys:
#             self.options.pop(i, None)
#
#     def set_type(self, type):
#         self.options["valueType"] = "xsd:" + type
#
#     # TODO a nice thing to do would be to read the min and max value
#     # from the rest of the content of self.options
#     # could avoid having the user to input those
#     def set_min(self, value):
#         self.options["minValue"] = value
#
#     def set_max(self, value):
#         self.options["maxValue"] = value
#
#     def set_length(self, value):
#         self.options["maxLength"] = value
#
#     def set_multiple_choice(self, value):
#         self.options["multipleChoice"] = value
#
#     def use_preset(self, URI):
#         """
#         In case the list response options are read from another file
#         like for languages, country, state...
#         """
#         self.options["choices"] = URI
#
#     def add_choice(self, choice, value, lang=DEFAULT_LANG):
#         self.options["choices"].append({"name": {lang: choice}, "value": value})
#
#     def sort(self):
#         options_order = [
#             "@context",
#             "@type",
#             "@id",
#             "valueType",
#             "minValue",
#             "maxValue",
#             "multipleChoice",
#             "choices",
#         ]
#         reordered_dict = reorder_dict_skip_missing(self.options, options_order)
#         self.options = reordered_dict
#
#     def write(self, output_dir):
#         self.sort()
#         self.schema = self.options
#         self._SchemaBase__write(output_dir)
