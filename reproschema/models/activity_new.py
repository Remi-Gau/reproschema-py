from reproschema.models.base import SchemaBase

# import base
# import item_new
import attr


@attr.s()
class Activity(SchemaBase):
    """
    class to deal with reproschema activities
    """

    # schema_type = "reproschema:Activity"

    shuffle = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(bool)),
    )
    allow = attr.ib(default=attr.Factory(list))
    order = attr.ib(
        default=attr.Factory(list),
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(str),
            iterable_validator=attr.validators.instance_of(list),
        ),
    )
    addProperties = attr.ib(
        default=attr.Factory(list),
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(dict),
            iterable_validator=attr.validators.instance_of(list),
        ),
    )
    overrideProperties = attr.ib(
        default=attr.Factory(list),
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(dict),
            iterable_validator=attr.validators.instance_of(list),
        ),
    )
    compute = attr.ib(
        default=attr.Factory(list),
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of(dict),
            iterable_validator=attr.validators.instance_of(list),
        ),
    )
    _schemaType = attr.ib(default="reproschema:Activity")

    @allow.validator
    def check_allow(self, attribute, value):
        if not (isinstance(value, list)):
            raise ValueError(f"allow must be a list! got {type(value)}")
        allow_list = [
            "reproschema:AllowExport",
            "reproschema:DisableBack",
            "reproschema:AutoAdvance",
            "reproschema:AllowReplay",
            "reproschema:Skipped",
            "reproschema:DontKnow",
            "reproschema:TimedOut",
        ]
        for e in value:
            if e not in allow_list:
                raise ValueError(
                    f"allow property not a defined property! got {e}, allowed list is {allow_list}"
                )

    # def __init__(self, version=None):
    #     super().__init__(version)
    #     self.schema["ui"] = {"shuffle": [], "order": [], "addProperties": []}
    #
    # def set_ui_shuffle(self, shuffle=False):
    #     self.schema["ui"]["shuffle"] = shuffle

    # def set_URI(self, URI):
    #     self.URI = URI

    # def get_URI(self):
    #     return self.URI

    # TODO
    # preamble
    # compute
    # citation
    # image

    # def set_defaults(self, name):
    #     self._ReproschemaSchema__set_defaults(name)  # this looks wrong
    #     self.set_ui_shuffle(False)
    #
    # def update_activity(self, item_info):
    #
    #     # TODO
    #     # - remove the hard coding on visibility and valueRequired
    #
    #     # update the content of the activity schema with new item
    #
    #     item_info["URI"] = "items/" + item_info["name"]
    #
    #     append_to_activity = {
    #         "variableName": item_info["name"],
    #         "isAbout": item_info["URI"],
    #         "isVis": item_info["visibility"],
    #         "valueRequired": False,
    #     }
    #
    #     self.schema["ui"]["order"].append(item_info["URI"])
    #     self.schema["ui"]["addProperties"].append(append_to_activity)
    #
    # def sort(self):
    #     schema_order = [
    #         "prefLabel",
    #         "description",
    #         "schemaVersion",
    #         "version",
    #         "ui",
    #     ]
    #     self.sort_schema(schema_order)
    #
    #     ui_order = ["shuffle", "order", "addProperties"]
    #     self.sort_ui(ui_order)
    # def write(self, output_dir, filename):
    #     # self.sort()
    #     self._SchemaBase__write(output_dir, filename)

    def append_item(self, item):
        additional_properties = {
            "variableName": "item_1",
            "isAbout": "./item_1",
            "isVis": item.visible,
            "requiredValue": item.required,
        }
        if item.skippable:
            self.allow = ["reproschema:Skipped"]

        self.order.append("./item_1")
        self.addProperties.append(additional_properties)
        attr.validate(self)

    def write(self, output_dir, filename):
        self._SchemaBase__write(output_dir, filename)
