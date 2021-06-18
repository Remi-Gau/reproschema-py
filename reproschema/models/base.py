import json
import os
import attr
from pathlib import Path
from collections import OrderedDict
# import item_new

"""
For any key that can be 'translated' we set english as the default language
in case the user does not provide it.
"""
DEFAULT_LANG = "en"
"""
"""
DEFAULT_VERSION = "1.0.0-rc4"

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
    "preamble",
    "citation",
    "image",
    "audio",
    "video",
    "ui",
    "compute",
]

# def default_context(version):
#     """
#     For now we assume that the github repo will be where schema will be read from.
#     """
#     URL = "https://raw.githubusercontent.com/ReproNim/reproschema/"
#     VERSION = version or DEFAULT_VERSION
#     return URL + VERSION + "/contexts/generic"

@attr.s
class SchemaBase:
    """
    base class to deal with reproschema schemas.
    """
    # TODO might be more convenient to have some of the properties not centrlized in a single dictionnary
    #
    # Could be more practical to only create part or all of the dictionnary when write is called
    #

    def check_labels(self, attribute, value):
        if not isinstance(value, (str, dict)):
            raise ValueError(f'{attribute.name} must be a string or a dict! got {type(value)}')

    prefLabel = attr.ib(kw_only=True, validator=check_labels)
    altLabel = attr.ib(default=None, validator=attr.validators.optional(check_labels))
    description = attr.ib(default=None, validator=attr.validators.optional(attr.validators.instance_of(str)))
    schemaVersion = attr.ib(default="1.0.0-rc4", validator=attr.validators.instance_of(str))
    version = attr.ib(default="0.0.1", validator=attr.validators.instance_of(str))
    preamble = attr.ib(default=None, validator=attr.validators.optional(check_labels))
    # citation - string/uri ?
    citation = attr.ib(default=None)
    # image - iri/mediaobject
    image = attr.ib(default=None)
    audio = attr.ib(default=None)
    video = attr.ib(default=None)
    about = attr.ib(default=None)
    _schemaType = attr.ib(default=None)

    def __write(self, output_dir, filename):
        """
            Reused by the write method of the children classes
        """
        schema = {
            "@context": "https://raw.githubusercontent.com/ReproNim/reproschema//contexts/generic",
            "@type": str(self._schemaType),
            "@id": filename
        }
        props = self.__dict__.copy()
        ui_obj = {
            "order": props['order'],
            "addProperties": props['addProperties'],
            "allow": props['allow'],
            "shuffle": props['shuffle']
        }
        ui_obj = {key: value for key, value in ui_obj.items() if bool(value)}
        print(ui_obj)
        del props['order'], props['addProperties'], props['shuffle'], props['allow']
        props.update(schema)
        props.update({'ui': ui_obj})
        props = {key: value for key, value in props.items() if bool(value)}
        reordered_dict = reorder_dict_skip_missing(props, SCHEMA_ORDER)
        with open(os.path.join(output_dir, filename), "w") as ff:
            json.dump(reordered_dict, ff, indent=4)


    # schema_type = None
    #
    # def __init__(self, version):
    #
    #     # TODO the version handling could probably be refactored
    #     VERSION = version or DEFAULT_VERSION
    #
    #     self.schema = {
    #         "@type": self.schema_type,
    #         "schemaVersion": VERSION,
    #         "version": "0.0.1",
    #     }
    #
    #     URL = self.get_default_context(version)
    #     self.set_context(URL)

    # This probably needs some cleaning but is at the moment necessary to pass
    # the context to the ResponseOption class


def reorder_dict_skip_missing(old_dict, key_list):
    """
    reorders dictionary according to ``key_list``
    removing any key with no associated value
    or that is not in the key list
    """
    return OrderedDict((k, old_dict[k]) for k in key_list if k in old_dict)


# aa = SchemaBase(prefLabel='testing pref', description='trial', altLabel='testing alt',
#                 preamble= {"en": 'this is a preamble', "es": "spanish string"},
#                 citation='https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1495268/',
#                 image={"@type": "AudioObject", "contentUrl": "http://example.com/sample-image.png"})
# aa.prefLabel = 'new pref label'
# item_1 = item.Item()
# aa.append_item(item_1)
# print(aa.write('./', 'base_schema.jsonld'))


# aa = SchemaBase(prefLabel='testing pref', description='trial',
#                 preamble={"en": 'this is a preamble', "es": "spanish string"},
#                 citation='https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1495268/',
#                 image={"@type": "AudioObject", "contentUrl": "http://example.com/sample-image.png"})
#
#
# # # aa.prefLabel = 'new pref label'
# item_1 = item_new.Item()
# aa.append_item(item_1)
# print(112, aa)
# #
# print(aa.write('./', 'activity3_schema.jsonld'))

