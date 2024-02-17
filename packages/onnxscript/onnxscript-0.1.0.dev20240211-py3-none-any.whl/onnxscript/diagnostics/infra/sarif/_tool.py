# DO NOT EDIT! This file was generated by jschema_to_python version 0.0.1.dev29,
# with extension for dataclasses and type annotation.

from __future__ import annotations

import dataclasses
from typing import List, Optional

from onnxscript.diagnostics.infra.sarif import _property_bag, _tool_component


@dataclasses.dataclass
class Tool:
    """The analysis tool that was run."""

    driver: _tool_component.ToolComponent = dataclasses.field(
        metadata={"schema_property_name": "driver"}
    )
    extensions: Optional[List[_tool_component.ToolComponent]] = dataclasses.field(
        default=None, metadata={"schema_property_name": "extensions"}
    )
    properties: Optional[_property_bag.PropertyBag] = dataclasses.field(
        default=None, metadata={"schema_property_name": "properties"}
    )


# flake8: noqa
