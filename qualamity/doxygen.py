import os
import re
from importlib import resources
from pathlib import Path
from subprocess import DEVNULL, PIPE, run

from pycparser.plyparser import Coord

from .config import Program, assets
from .linter import Linter


class Undocumented(Linter):
    name = "Documenter l'ensemble des declarations top-level"
    description = "il faut documenter les fonctions, structures, membres, enumerations et types"
    expression = re.compile(r'([^:]*?):(\d+):[^:]*?:\s*\w+\s+(\w+)(\[\d+\]|\([^)]*\))?\s+\((\w+)\)')
    translate = {
        'function': 'La fonction',
        'variable': 'La variable',
        'enumeration': "L'énumération",
        'typedef': 'Le type'
    }

    def __init__(self, doxygen: Program):
        super().__init__()
        self.doxygen = doxygen

    def scan_all(self, paths: list[str]):
        os.environ['INPUT'] = ' '.join(map(str, paths))
        warnings = run([self.doxygen.executable, assets.joinpath('doxygen.conf')], check=True, stdout=DEVNULL, stderr=PIPE, encoding='utf8').stderr
        for warning in warnings.split('\n'):
            match = self.expression.match(warning)
            if match:
                location = Path(match[1]).relative_to(Path('.').absolute())
                self.report(Coord(location, int(match[2])), f"{self.translate[match[5]]} `{match[3]}` n'est pas documentée")
        return self.reports
