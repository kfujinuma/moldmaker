from dataclasses import dataclass
from pathlib import Path

from moldmaker.parameter import Parameter, Parameters
from moldmaker.replacer import Replacer, SingleReplacer


@dataclass
class MoldMaker:
    r4c: Replacer
    r4p: Replacer

    def replace_dir(self, target_dir: Path, dist_dir: Path) -> None:
        target_root = target_dir.resolve().parent
        for p in target_dir.glob("**/*"):
            if p.is_file():
                relative = p.resolve().relative_to(target_root)
                dist = self.r4p.replace_path(relative, dist_dir)
                self.r4c.replace_file(p, dist)

    @classmethod
    def from_parameters(cls, parameters: Parameters) -> "MoldMaker":
        p_list = sorted(parameters.params, key=(lambda p: len(p.value)), reverse=True)
        r4c = Replacer([cls.sr_for_content(p) for p in p_list])
        r4p = Replacer([cls.sr_for_path(p) for p in p_list])
        return MoldMaker(r4c, r4p)

    @staticmethod
    def sr_for_content(prm: Parameter) -> SingleReplacer:
        return SingleReplacer(prm.value, f"{{{{ {prm.param_name} }}}}")

    @staticmethod
    def sr_for_path(prm: Parameter) -> SingleReplacer:
        return SingleReplacer(prm.value, f"{{{{{prm.param_name}}}}}")


def make_mold(param_file: Path, source_dir: Path, dist_dir: Path):
    mm = MoldMaker.from_parameters(Parameters.load_json(param_file))
    mm.replace_dir(source_dir, dist_dir)
