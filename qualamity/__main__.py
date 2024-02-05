import logging
import logging.config
import sys
from argparse import ArgumentParser
from pathlib import Path

import yaml

from qualamity import (CLinter, Program, Undocumented, assets, get_clang_tidy,
                       get_doxygen, get_preprocessor, load_linters,
                       report_list_to_csv, report_list_to_json,
                       report_list_to_markdown, report_to_latex)

default_logging_file = assets.joinpath('logging.yaml')

if __name__ == '__main__':
    cli_parser = ArgumentParser(description = 'Scan files to check conformance with coding rules')
    cli_parser.add_argument('paths', metavar='PATH', type=str, nargs='+', help='Files and directories to scan')
    cli_parser.add_argument('-c', '--config', type=str, default='.qualamity.yaml', help='Config file to retrieve lint list from')
    cli_parser.add_argument('-l', '--logging-config', type=str, default=default_logging_file, help='Config file of the logging library')
    cli_parser.add_argument('-I', '--includes', type=str, nargs='*', default=[], help='Add folder to look for headers in')
    cli_parser.add_argument('-f', '--format', type=str, default='markdown', help='Output format: can be markdown, latex, json, or csv')
    args = cli_parser.parse_args()

    logging_config_file = Path(args.logging_config)
    with logging_config_file.open() as f:
        logging.config.dictConfig(yaml.safe_load(f))
    logger = logging.getLogger(__package__)

    config_file = Path(args.config)
    if not config_file.exists():
        logger.error(f'The specified configuration file "{config_file}" does not exist')
        exit(1)
    with config_file.open() as f:
        config = yaml.safe_load(f)
        linters = load_linters(config)
        cpp = get_preprocessor(config)
        cpp = Program(cpp.executable, cpp.arguments, args.includes + cpp.includes + [str(assets.joinpath('fake_libc_include'))])
        ctidy = get_clang_tidy(config)
        doxygen = get_doxygen(config)

        reports = []
        for path in map(Path, args.paths):
            if not path.exists():
                logger.error(f'No such file or directory: "{path}"')
                continue
            logger.info(f"Scanning {path}")
            for linter in linters:
                if issubclass(linter, CLinter):
                    reports += linter(cpp).scan(path)
                elif issubclass(linter, Undocumented):
                    reports += linter(doxygen).scan(path)
                else:
                    reports += linter().scan(path)

        match args.format:
            case 'markdown':
                report_list_to_markdown(sys.stdout, reports)
            case 'latex':
                report_to_latex(sys.stdout, reports, cpp, ctidy, doxygen)
            case 'csv':
                report_list_to_csv(sys.stdout, reports)
            case 'json':
                report_list_to_json(sys.stdout, reports)
            case _:
                raise RuntimeError(f'Unknown format {args.format}')
