"""
Package allowing the definition and usage of simple Linters.
"""

__version__ = '0.1'

from .config import (Program, assets, get_clang_tidy, get_doxygen,
                     get_preprocessor)
from .doxygen import Undocumented
from .linter import CLinter, Linter
from .loader import load_linters
from .log_formatter import ColoredFormatter
from .report import (Report, report_list_to_csv, report_list_to_json,
                     report_list_to_markdown, report_to_latex)
