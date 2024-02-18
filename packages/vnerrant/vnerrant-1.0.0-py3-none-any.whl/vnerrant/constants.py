from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from vnerrant.utils.utils import load_yml_file

# Replace magic strings with constants
MERGING_RULES = "rules"
MERGING_ALL_SPLIT = "all-split"
MERGING_ALL_MERGE = "all-merge"
MERGING_ALL_EQUAL = "all-equal"


base_dir = Path(__file__).resolve().parent
# Load the data from the YAML file into the dataclass
MAPPING_TYPE_ERROR = load_yml_file(base_dir / "config" / "mapping_type_error.yaml")


@dataclass(frozen=True)
class Operator:
    """
    Error operation types.
    """

    MISSING: str = "M"
    UNNECESSARY: str = "U"
    REPLACE: str = "R"


@dataclass
class SeparatorTypes:
    """
    Separator types.
    """

    HYPHEN: str = "-"
    COMPOUND: str = "+"
    COLON: str = ":"
