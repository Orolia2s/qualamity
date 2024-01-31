import importlib.resources
from collections import namedtuple

Program = namedtuple('Program', ['executable', 'arguments', 'includes'])

assets = importlib.resources.files(__package__).joinpath('assets')

def get_program(config: dict, name: str, default: str) -> Program:
    sub = config.get(name, {})
    program = sub.get('program', default)
    args = sub.get('arguments', [])
    include = sub.get('includes', [])
    return Program(program, args, include)

def get_preprocessor(config: dict) -> Program:
    return get_program(config, 'preprocessor', 'cpp')

def get_clang_tidy(config: dict) -> Program:
    return get_program(config, 'clang-tidy', 'clang-tidy')

def get_doxygen(config: dict) -> Program:
    return get_program(config, 'doxygen', 'doxygen')
