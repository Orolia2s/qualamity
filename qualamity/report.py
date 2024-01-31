import csv
import platform
import re
import shlex
from collections import defaultdict, namedtuple
from subprocess import check_output, getoutput
from typing import TextIO

import distro

from .config import Program, assets
from .latex import (BookTabular, BookTabularX, Center, Document, Font, Itemize,
                    Landscape, Small, Symbols, Table, chapter, section)

Report = namedtuple('Report', ['location', 'rule', 'details'])

def report_order(report: Report):
    return (report.rule.name, report.location.file, report.location.line, report.location.column)

def report_list_to_markdown(output: TextIO, reports: list[Report]) -> str:
    def write_line(line: list):
        output.write('| ' + ' | '.join(map(str, line)) + ' |\n')
    output.write('## Static analysis report\n\n')
    output.write(f'{len(reports)} violations identified:\n\n')
    write_line(['Name', 'Location', 'Details'])
    write_line([':--'] * 3)
    for report in sorted(reports, key = report_order):
        write_line([report.rule.name, f'`{report.location}`', report.details ])

def to_latex(string: str) -> str:
    def process_match(match) -> str:
        return Font.verbatim_typewriter(match[0][1:-1], fancy = False)
    return re.sub('`[^`]*`', process_match, string)

def report_list_to_latex(output: TextIO, reports: list[Report]):
    with BookTabularX(output, 'llrrX', ['Name', 'File', 'L.', 'C.', r"Details"], '25.5cm') as tabular:
        prev_code = prev_file = None
        i = 0
        for report in sorted(reports, key = report_order):
            code = file = ''
            if report.location.file != prev_file or report.rule.name != prev_code:
                prev_file = report.location.file
                file = Font.verbatim_typewriter(report.location.file, fancy = False)
                if report.rule.name != prev_code:
                    prev_code = report.rule.name
                    code = Font.verbatim_typewriter(report.rule.name, fancy = False)
                    i += 1
            if i % 2:
                tabular.write_line(r'\rowcolor{gray!10}')
            col = report.location.column if report.location.column else ''
            tabular.add_line([code, file, report.location.line, col, to_latex(report.details)])

def report_to_latex(output: TextIO, reports: list[Report], cpp: Program, ctidy: Program, doxy: Program):
    with open(assets.joinpath('preambule.tex')) as preambule:
        output.write(preambule.read()) #.replace('ASSETS', str(assets)))
    with Document(output) as out:
        out.write_line(r'\maketitle')
        out.write_line(r'\tableofcontents')
        out.write_line(chapter("Environment"))
        with Table(out, 'h', "Machine") as table:
            with Center(table) as center:
                with BookTabular(center, 'cccc', ['Architecture', 'OS', 'Distribution', 'Version']) as tabular:
                    tabular.add_line(list(map(Font.verbatim_typewriter, [platform.machine().replace('_', r'\_'), platform.system(), distro.name(), distro.version()])))
        with Table(out, 'h', "Tools") as table:
            with Center(table) as center:
                with BookTabular(center, 'lll', ['Description', 'Command', 'Version']) as tabular:
                    tabular.add_line(['C Preprocessor', Font.verbatim_typewriter(cpp), Font.verbatim_typewriter(getoutput(f'{cpp.executable} --version | head -1'))])
                    tabular.add_line(['C Linter', Font.verbatim_typewriter(ctidy), Font.verbatim_typewriter(getoutput(f'{ctidy.executable} --version | head -2 | tail -1').strip())])
                    tabular.add_line(['Documentation parser', Font.verbatim_typewriter(doxy), Font.verbatim_typewriter(getoutput(f'{doxy.executable} --version').strip())])
        out.write_line(chapter("Result"))
        out.write_line(f'A total of {len(reports)} violations were identified:')
        with Landscape(out) as out:
            with Small(out) as out:
                with Center(out) as out:
                    report_list_to_latex(out, reports)

def report_list_to_csv(output: TextIO, reports: list[Report]):
    writer = csv.writer(output, quoting = csv.QUOTE_NONNUMERIC)
    writer.writerow(['Code', 'Rule', 'File', 'Line', 'Column', 'Details', 'Rule Comment'])
    for report in sorted(reports, key = report_order):
        writer.writerow([report.rule.__name__, report.rule.name, report.location.file, report.location.line,
                         report.location.column, report.details, report.rule.description])

def report_list_to_json(output: TextIO, reports: list[Report]):
    result = []
    for report in reports:
        result.append({
            'check_name': report.rule.name,
            'content': {'body': report.rule.description},
        })
