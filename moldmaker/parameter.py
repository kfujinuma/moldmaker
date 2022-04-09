from dataclasses import dataclass
from pathlib import Path
from typing import Collection, Mapping
import json


@dataclass
class Parameter:
    param_name: str
    value: str


@dataclass
class Parameters:
    params: Collection[Parameter]

    @classmethod
    def load(cls, target: Mapping) -> "Parameters":
        unnested: Mapping = unnest(target)
        return Parameters([Parameter(k, v) for k, v in unnested.items()])

    @classmethod
    def load_json(cls, path: Path) -> "Parameters":
        with open(path) as f:
            return cls.load(json.load(f))


def unnest(obj: Mapping, name: str = ""):
    unnested: dict = {}
    for k, v in obj.items():
        itemname = name + k
        if isinstance(v, Mapping):
            unnested |= unnest(v, itemname + ".")
        else:
            unnested[itemname] = v
    return unnested
