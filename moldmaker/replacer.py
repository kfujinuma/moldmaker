from dataclasses import dataclass
from pathlib import Path


@dataclass
class SingleReplacer:
    before: str
    after: str

    def replace(self, target: str) -> str:
        return target.replace(self.before, self.after)


@dataclass
class Replacer:
    replacer: list[SingleReplacer]

    def replace(self, target: str) -> str:
        replacing = target
        for sr in self.replacer:
            replacing = sr.replace(replacing)
        return replacing

    def replace_path(self, target_relative: Path, dist_root: Path) -> Path:
        relative_str = str(target_relative).replace("\\", "/")
        return dist_root / self.replace(relative_str)

    def replace_file(self, target: Path, dist: Path) -> None:
        dist.parent.mkdir(parents=True, exist_ok=True)
        with open(target) as f:
            s = f.read()
        with open(dist, mode="w") as f:
            f.write(self.replace(s))