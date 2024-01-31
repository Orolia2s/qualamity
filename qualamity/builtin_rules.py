import re
import subprocess
from pathlib import Path

from pycparser import c_ast
from pycparser.plyparser import Coord

from .config import assets
from .doxygen import Undocumented
from .linter import CLinter, Linter


class FunctionDefinedInHeader(CLinter):
    name = 'Implementation de fonctions dans un header'
    reference = '[CERT] : DCL31-C'
    description = 'Il ne faut pas definir de fonction dans un header, seulement les declarer.'
    extension = '*.h'

    def scan_ast(self, ast):
        class FunctionDefinitionVisitor(c_ast.NodeVisitor):
            def visit_FuncDef(slf, node):
                self.report(node.decl.coord, f'La fonction `{node.decl.name}` est définie dans un header')
        FunctionDefinitionVisitor().visit(ast)

class GlobalDefinedInHeader(CLinter):
    name = 'Definition de variables dans un header'
    reference = '[MISRA-C++] : 3-1-1'
    description = "Il ne faut pas definir la valeur d'une variable dans un header, seulement la declarer en tant qu'externe."
    extension = '*.h'

    def scan_ast(self, ast):
        class FunctionDeclarationVisitor(c_ast.NodeVisitor):
            def visit_Decl(slf, node):
                if node.init:
                    self.report(node.coord, f'La constante `{node.name}` est définie dans un header')
        FunctionDeclarationVisitor().visit(ast)

class UsingForbiddenEnvironmentFunctions(CLinter):
    name = "Utilisation de system ou getenv"
    reference = ['[CERT] : ENV01-C', '[CERT] : ENV02-C', '[CERT] : ENV33-C', '[MISRA-C] : 21.8']
    description = "Ne pas utiliser getenv ou system"
    forbidden = {'getenv', 'system'}

    def scan_ast(self, ast):
        class FunctionCallVisitor(c_ast.NodeVisitor):
            def visit_FuncCall(slf, node):
                if node.name.name in self.forbidden:
                    self.report(node.coord, f'La fonction `{node.name.name}` est appelée')
        FunctionCallVisitor().visit(ast)

class UsingForbiddenExitFunctions(UsingForbiddenEnvironmentFunctions):
    name = "Utilisation de abort ou _Exit"
    reference = ['[CERT] : ENV32-C', '[CERT] : ERR00-C', '[CERT] : ERR04-C', '[CERT] : ERR06-C']
    description = "Ne pas utiliser abort ou _Exit pour que les fonctions enregistrés avec atexit soient executés."
    forbidden = {'abort', '_Exit'}

class UsingUnsafeTimeFunctions(UsingForbiddenEnvironmentFunctions):
    name = "Il faut utiliser les versions securisées des fonctions de time.h"
    reference = ['[CERT] : MSC33-C', '[MISRA-C] : 21.10']
    description = "Utiliser asctime_s au lieu de asctime, idem pour ctime, gmtime et localtime"
    forbidden = {'asctime', 'ctime', 'gmtime', 'localtime'}

class UsingUnsafeFunctions(UsingForbiddenEnvironmentFunctions):
    name = "Il faut utiliser la version securisée de memset"
    reference = ['[CERT] : MSC06-C']
    description = "Utiliser memset_s au lieu de memset"
    forbidden = {'memset'}

class UsingUnsafeParseFunctions(UsingForbiddenEnvironmentFunctions):
    name = "Utilisation de atoi et dérivées"
    reference = ['[CERT] : ERR07-C', '[CERT] : ERR34-C', '[MISRA-C] : 21.7']
    description = "Préférer strtol à atoi"
    forbidden = {'atof', 'atoi', 'atol', 'atoll'}

class RedefiningStandardFunctions(CLinter):
    name = 'Ne pas redéfinir les fonctions standards'
    reference = ['[MISRA-C] : 21.1', '[MISRA-C] : 21.2']
    description = "Ne pas utiliser le nom d'une fonction standard pour nommer ses fonctions"
    forbidden = {line.removesuffix('\n') for line in assets.joinpath('standard_functions.txt').open('r')}

    def scan_ast(self, ast):
        class FunctionDefinitionVisitor(c_ast.NodeVisitor):
            def visit_FuncDef(slf, node):
                if node.decl.name in self.forbidden:
                    self.report(node.decl.coord, f'Redéfinition de la fonction `{node.decl.name}`')
        FunctionDefinitionVisitor().visit(ast)

class UncompletedTodos(Linter):
    name = 'Ne pas laisser de TODOs'
    description = "Ne pas laisser dans le code des commentaires du type TODO."
    extension = '*.[ch]'

    expression = re.compile(r'todo', re.IGNORECASE)

    def scan_file(self, path: Path):
        with path.open() as f:
            for i, line in enumerate(f, 1):
                match = re.search(self.expression, line)
                if match:
                    self.report(Coord(path, i, match.start()), f'à faire: `{line[match.start():-1]}`')

__all__ = [FunctionDefinedInHeader, GlobalDefinedInHeader, UsingForbiddenEnvironmentFunctions,
           UsingForbiddenExitFunctions, UsingUnsafeTimeFunctions, UsingUnsafeFunctions,
           UsingUnsafeParseFunctions, RedefiningStandardFunctions, UncompletedTodos, Undocumented]
