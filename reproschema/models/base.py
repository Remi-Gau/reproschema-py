import json
import os
from collections import OrderedDict

DEFAULT_LANG = "en"


class SchemaBase:
    """
    class to deal with reproschema schemas
    """

    schema_type = None

    def __init__(self, version):

        URL = "https://raw.githubusercontent.com/ReproNim/reproschema/"
        VERSION = version or "1.0.0-rc4"

        self.schema = {
            "@type": self.schema_type,
            "schemaVersion": VERSION,
            "version": "0.0.1",
        }

        self.set_context(URL + VERSION + "/contexts/generic")

    def __set_defaults(self, name):
        self.set_filename(name)
        self.set_directory(name)
        self.set_pref_label(name.replace("_", " "))
        self.set_description(name.replace("_", " "))

    """
        setters
    """

    def set_directory(self, output_directory):
        self.dir = output_directory

    def set_URI(self, URI):
        self.URI = URI

    """
        schema related setters
    """

    def set_context(self, context):
        self.schema["@context"] = context

    def set_preamble(self, preamble="", lang=DEFAULT_LANG):
        self.schema["preamble"] = {lang: preamble}

    def set_citation(self, citation):
        self.schema["citation"] = citation

    def set_image(self, image):
        self.schema["image"] = image

    def set_filename(self, name, ext=".jsonld"):
        self.schema_file = name + "_schema" + ext
        self.schema["@id"] = name + "_schema" + ext

    def set_pref_label(self, pref_label):
        self.schema["prefLabel"] = pref_label

    def set_description(self, description):
        self.schema["description"] = description

    """
        getters
    """

    def get_name(self):
        return self.schema_file.replace("_schema", "")

    def get_filename(self):
        return self.schema_file

    def get_URI(self):
        return self.URI

    """
    writing, reading, sorting, unsetting
    """

    def sort_schema(self, schema_order):

        reordered_dict = reorder_dict_skip_missing(self.schema, schema_order)
        self.schema = reordered_dict

    def sort_ui(self, ui_order):

        reordered_dict = reorder_dict_skip_missing(self.schema["ui"], ui_order)
        self.schema["ui"] = reordered_dict

    def __write(self, output_dir):
        with open(os.path.join(output_dir, self.schema_file), "w") as ff:
            json.dump(self.schema, ff, sort_keys=False, indent=4)

    @classmethod
    def from_data(cls, data):
        if cls.schema_type is None:
            raise ValueError("SchemaBase cannot be used to instantiate class")
        if cls.schema_type != data["@type"]:
            raise ValueError(f"Mismatch in type {data['@type']} != {cls.schema_type}")
        klass = cls()
        klass.schema = data
        return klass

    @classmethod
    def from_file(cls, filepath):
        with open(filepath) as fp:
            data = json.load(fp)
        if "@type" not in data:
            raise ValueError("Missing @type key")
        return cls.from_data(data)


def reorder_dict_skip_missing(old_dict, key_list):
    return OrderedDict((k, old_dict[k]) for k in key_list if k in old_dict)
