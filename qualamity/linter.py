import logging
from fnmatch import fnmatch
from pathlib import Path

from pycparser import CParser, parse_file
from pycparser.plyparser import Coord

from .config import Program
from .report import Report


class Linter:
    name = None
    description = None
    extension = '*.*'
    log = logging.getLogger(__package__)

    def __init__(self):
        self.reports = []

    def report(self, location: Coord, details: str):
        self.reports.append(Report(location, self.__class__, details))

    def scan_file(self, path: Path):
        self.log.info('Would scan {path}')

    def scan_directory(self, directory: Path):
        for path in directory.rglob(self.extension):
            self.scan_file(path)

    def scan(self, path: Path | str) -> list[Report]:
        if not isinstance(path, Path):
            path = Path(path)
        if path.is_dir():
            self.scan_directory(path)
        elif fnmatch(path.name, self.extension):
            self.scan_file(path)
        else:
            self.log.info(f'{self.__class__.__name__}: skipping {path}')
        return self.reports

class CLinter(Linter):
    extension = "*.c"

    def __init__(self, preprocessor: Program):
        super().__init__()
        self.preprocessor = preprocessor

    def scan_file(self, path: Path):
        self.scan_ast(parse_file(path, use_cpp = True,
                                 cpp_path = self.preprocessor.executable,
                                 cpp_args = self.preprocessor.arguments + [f'-I{p}' for p in self.preprocessor.includes]))

class ClangLinter(Linter):
    extension = "*.c"
    clang_rule = None

    def __init__(self, clang_tidy: Program):
        super().__init__()
        self.clang_tidy = clang_tidy

    def scan_file(self, path: Path):
        pass
