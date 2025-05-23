# Qualamity: Generate reports on coding rule conformance

This is a proof of concept developed in two weeks by a single person.
It can be used to ensure that a given C code conforms to a set of coding rules.

## Requirement

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

```bash
uv tool install git+https://github.com/Orolia2s/qualamity
```

## Usage

The intended usage is from your C project root, with a `.qualamity.yaml` listing the rules you are interested in.

```console
$ qualamity --help

usage: qualamity [-h] [-c CONFIG] [-l LOGGING_CONFIG] [-I [INCLUDES ...]] [-f FORMAT]
                 PATH [PATH ...]

Scan files to check conformance with coding rules

positional arguments:
  PATH                  Files and directories to scan

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file to retrieve lint list from. Defaults to ".qualamity.yaml"
  -l LOGGING_CONFIG, --logging-config LOGGING_CONFIG
                        Specify a custom config file of the logging library
  -I [INCLUDES ...], --includes [INCLUDES ...]
                        Add folder to look for headers in
  -f FORMAT, --format FORMAT
                        Output format: can be markdown, latex, sonarqube, gitlab, github or csv. Defaults to markdown
```

### Example

Code that tries to violate every rule is provided in the `example` directory.

A PDF report can be generated from this directory:
```bash
make pdf
xdg-open example.pdf
```
