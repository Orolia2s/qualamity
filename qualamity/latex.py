from typing import TextIO


class Font:

    @staticmethod
    def typewriter(text :str):
        return r'\texttt{%s}' % text

    @staticmethod
    def small_caps(text :str):
        return r'\textsc{%s}' % text

    @staticmethod
    def verbatim_typewriter(text: str, delimiter: str = '|', fancy: bool = True):
        return r'\texttt{\%cerb%c%s%c}' % ('vV'[fancy], delimiter, text, delimiter)


class Symbols:
    envelope = r'\Letter{}'
    phone = r'\Telefon{}'
    ensure_space = r'\enspace{}'
    new_line = r'\\'
    page_break = r'\pagebreak{}'
    copyright = r'\copyright{}'


class Environment:
    name = None
    args = None

    def __init__(self, parent: TextIO):
        self.parent = parent

    def __enter__(self):
        args = [self.name]
        if self.args:
            args += self.args
        self.parent.write(r'\begin{' + '}{'.join(args) + '}\n')
        return self

    def write(self, string: str):
        self.parent.write(f'\t{string}')

    def write_line(self, line: str):
        self.write(f'{line}\n')

    def __exit__(self, exception_type, exception_value, traceback):
        self.parent.write(r'\end{' + self.name + '}\n')

class Document(Environment):
    name = 'document'

class Landscape(Environment):
    name = 'landscape'

class Small(Environment):
    name = 'small'

class Center(Environment):
    name = 'center'

class Enumerate(Environment):
    name = 'enumerate'

    def __init__(self, parent: TextIO | Environment):
        super().__init__(parent)

    def add(self, item):
        self.write_line(r'\item ' + str(item))

class Itemize(Enumerate):
    name = 'itemize'

class Multicols(Environment):
    name = "multicols"

    def __init__(self, parent: TextIO | Environment, columns_count: int):
        self.args = [columns_count]
        super().__init__(out)

class Table(Environment):
    name = 'table'

    def __init__(self, parent: TextIO | Environment, placement: str, caption: str):
        self.placement = placement
        self.caption = caption
        super().__init__(parent)

    def __enter__(self):
        self.parent.write(r'\begin' +'{%s}[%s]\n' % (self.name, self.placement))
        self.write_line(r'\caption{%s}' % self.caption)
        return self

class BookTabular(Environment):
    name = 'tabular'

    def __init__(self, parent: TextIO | Environment, alignment: str, header: list[str]):
        self.args = [alignment]
        self.header = header
        self.columns_count = len(header)
        super().__init__(parent)

    def add_line(self, line: list[str]):
        if len(line) != self.columns_count:
            raise Exception('Invalid number of columns in a tabular')
        self.write_line(' & '.join(map(str, line)) + f' {Symbols.new_line}')

    def __enter__(self):
        super().__enter__()
        self.write_line(r'\toprule')
        self.add_line(self.header)
        self.write_line(r'\midrule')
        return self

    def __exit__(self, *args):
        self.write_line(r'\bottomrule')
        super().__exit__(*args)

class BookTabularX(BookTabular):
    name = 'tabularx'

    TEXT_WIDTH = r'\textwidth'

    def __init__(self, parent: TextIO | Environment, alignment: str, header: list[str], width: str):
        self.args = [width, alignment]
        self.header = header
        self.columns_count = len(header)
        Environment.__init__(self, parent)


def section(name :str, depth :int = 0, indexed :bool = True):
    return r'\%ssection%s{%s}' % ('sub' * depth, '' if indexed else '*', name) + '\n'

def chapter(name :str, indexed :bool = True):
    return r'\chapter%s{%s}' % ('' if indexed else '*', name) + '\n'
