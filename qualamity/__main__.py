import logging
import logging.config
import sys
from argparse import ArgumentParser
from pathlib import Path

import yaml

from qualamity import (CLinter, Program, Undocumented, assets, get_clang_tidy,
                       get_doxygen, get_preprocessor, load_linters,
                       report_list_to_csv, report_list_to_github,
                       report_list_to_gitlab, report_list_to_markdown,
                       report_to_latex, report_list_to_sonarqube)

default_logging_file = assets.joinpath('logging.yaml')

def main():
    cli_parser = ArgumentParser(description = 'Scan files to check conformance with coding rules')
    cli_parser.add_argument('paths', metavar='PATH', type=str, nargs='+', help='Files and directories to scan')
    cli_parser.add_argument('-c', '--config', type=str, default='.qualamity.yaml', help='Config file to retrieve lint list from. Defaults to ".qualamity.yaml"')
    cli_parser.add_argument('-l', '--logging-config', type=str, default=default_logging_file, help='Specify a custom config file of the logging library')
    cli_parser.add_argument('-I', '--include', dest='includes', metavar='FILE', type=str, action='append', default=[], help='Add folder to look for headers in')
    cli_parser.add_argument('-f', '--format', type=str, default='markdown', help='Output format: can be markdown, latex, sonarqube, gitlab, github or csv. Defaults to markdown')
    args = cli_parser.parse_args()

    logging_config_file = Path(args.logging_config)
    with logging_config_file.open() as f:
        logging.config.dictConfig(yaml.safe_load(f))
    logger = logging.getLogger(__package__)

    logger.info(f'Starting qualamity, searching headers in {args.includes}')
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
        if Undocumented in linters:
            # While most linters apply to a single file at a time, doxygen needs to parse both headers and sources
            # to know if a fuction is documented. So it is only called once, and will scan all applicable files
            reports += Undocumented(doxygen).scan_all(args.paths)
            linters.remove(Undocumented)
        for path in map(Path, args.paths):
            if not path.exists():
                logger.error(f'No such file or directory: "{path}"')
                continue
            logger.info(f"Scanning {path}")
            for linter in linters:
                if issubclass(linter, CLinter):
                    reports += linter(cpp).scan(path)
                else:
                    reports += linter().scan(path)

        match args.format:
            case 'markdown':
                report_list_to_markdown(sys.stdout, reports)
            case 'latex':
                report_to_latex(sys.stdout, reports, cpp, ctidy, doxygen)
            case 'csv':
                report_list_to_csv(sys.stdout, reports)
            case 'gitlab':
                report_list_to_gitlab(sys.stdout, reports)
            case 'github':
                report_list_to_github(sys.stdout, reports)
            case 'sonarqube':
                report_list_to_sonarqube(linters + [Undocumented], sys.stdout, reports)
            case _:
                raise RuntimeError(f'Unknown format {args.format}')

if __name__ == '__main__':
    main()
