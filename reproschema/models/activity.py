from pathlib import Path
from typing import Dict
from typing import Optional
from typing import Union

from .base import COMMON_SCHEMA_ORDER
from .base import DEFAULT_LANG
from .base import SchemaBase
from .item import Item


class Activity(SchemaBase):
    """
    class to deal with reproschema activities
    """

    def __init__(
        self,
        name: Optional[str] = "activity",
        schemaVersion: Optional[str] = None,
        prefLabel: Optional[str] = "activity",
        altLabel: Optional[Dict[str, str]] = None,
        description: Optional[str] = "",
        preamble: Optional[str] = None,
        citation: Optional[str] = None,
        image: Optional[Union[str, Dict[str, str]]] = None,
        suffix: Optional[str] = "_schema",
        visible: Optional[bool] = True,
        required: Optional[bool] = False,
        skippable: Optional[bool] = True,
        limit: Optional[str] = None,
        ext: Optional[str] = ".jsonld",
        output_dir: Optional[Union[str, Path]] = Path.cwd(),
        lang: Optional[str] = DEFAULT_LANG(),
    ):

        schema_order = COMMON_SCHEMA_ORDER() + [
            "citation",
            "compute",
        ]

        super().__init__(
            at_id=name,
            schemaVersion=schemaVersion,
            at_type="reproschema:Activity",
            prefLabel={lang: prefLabel},
            altLabel=altLabel,
            description=description,
            preamble=preamble,
            citation=citation,
            image=image,
            schema_order=schema_order,
            visible=visible,
            required=required,
            skippable=skippable,
            limit=limit,
            suffix=suffix,
            ext=ext,
            output_dir=output_dir,
            lang=lang,
        )
        self.ui.shuffle = False
        self.update()

    def append_item(self, item: Item):
        self.ui.append(obj=item, variableName=item.get_basename())
