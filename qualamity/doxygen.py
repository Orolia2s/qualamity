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
    code = 'EX_CS_DOCUMENT_C'
    description = "il faut documenter les fonctions, structures, membres, enumerations et types"
    extension = '*.c'
    expression = re.compile(r'[^:]*?:(\d+):[^:]*?:\s*\w+\s+(\w+)(\[\d+\]|\([^)]*\))?\s+\((\w+)\)')
    translate = {
        'function': 'La fonction',
        'variable': 'La variable',
        'enumeration': "L'énumération"
    }

    def __init__(self, doxygen: Program):
        super().__init__()
        self.doxygen = doxygen

    def scan_file(self, path: Path):
        os.environ['INPUT'] = str(path)
        warnings = run([self.doxygen.executable, assets.joinpath('doxygen.conf')], check=True, stdout=DEVNULL, stderr=PIPE, encoding='utf8').stderr
        for warning in warnings.split('\n'):
            match = self.expression.match(warning)
            if match:
                self.report(Coord(path, int(match[1])), f"{self.translate[match[4]]} `{match[2]}` n'est pas documentée")
