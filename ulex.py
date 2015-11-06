import os
from ply import lex
#from ply import yacc
from ply.lex import LexError


class UnrealLexer(object):
    reserved = {
        'abstract': 'ABSTRACT',
        'always': 'ALWAYS',
        'array': 'ARRAY',
        'arraycount': 'ARRAYCOUNT',
        'assert': 'ASSERT',
        'auto': 'AUTO',
        'automated': 'AUTOMATED',
        'bool': 'BOOL',
        'break': 'BREAK',
        'button': 'BUTTON',
        'byte': 'BYTE',
        'case': 'CASE',
        'class': 'CLASS',
        'coerce': 'COERCE',
        'collapsecategories': 'COLLAPSECATEGORIES',
        'config': 'CONFIG',
        'const': 'CONST',
        'continue': 'CONTINUE',
        'default': 'DEFAULT',
        'defaultproperties': 'DEFAULTPROPERTIES',
        'delegate': 'DELEGATE',
        'dependson': 'DEPENDSON',
        'deprecated': 'DEPRECATED',
        'do': 'DO',
        'dontcollapsecategories': 'DONTCOLLAPSECATEGORIES',
        'edfindable': 'EDFINDABLE',
        'editconst': 'EDITCONST',
        'editconstarray': 'EDITCONSTARRAY',
        'editinline': 'EDITINLINE',
        'editinlinenew': 'EDITINLINENEW',
        'editinlinenotify': 'EDITINLINENOTIFY',
        'editinlineuse': 'EDITINLINEUSE',
        'else': 'ELSE',
        'enum': 'ENUM',
        'enumcount': 'ENUMCOUNT',
        'event': 'EVENT',
        'exec': 'EXEC',
        'expands': 'EXPANDS',
        'export': 'EXPORT',
        'exportstructs': 'EXPORTSTRUCTS',
        'extends': 'EXTENDS',
        'false': 'FALSE',
        'final': 'FINAL',
        'float': 'FLOAT',
        'for': 'FOR',
        'foreach': 'FOREACH',
        'function': 'FUNCTION',
        'global': 'GLOBAL',
        'globalconfig': 'GLOBALCONFIG',
        'goto': 'GOTO',
        'guid': 'GUID',
        'hidecategories': 'HIDECATEGORIES',
        'if': 'IF',
        'ignores': 'IGNORES',
        'import': 'IMPORT',
        'init': 'INIT',
        'input': 'INPUT',
        'insert': 'INSERT',
        'instanced': 'INSTANCED',
        'int': 'INT',
        'intrinsic': 'INTRINSIC',
        'invariant': 'INVARIANT',
        'iterator': 'ITERATOR',
        'latent': 'LATENT',
        'length': 'LENGTH',
        'local': 'LOCAL',
        'localized': 'LOCALIZED',
        'name': 'NAME',
        'nativ': 'NATIV',
        'nativereplication': 'NATIVEREPLICATION',
        'new': 'NEW',
        'noexport': 'NOEXPORT',
        'none': 'NONE',
        'noteditinlinenew': 'NOTEDITINLINENEW',
        'notplaceable': 'NOTPLACEABLE',
        'nousercreate': 'NOUSERCREATE',
        'operator': 'OPERATOR',
        'optional': 'OPTIONAL',
        'out': 'OUT',
        'perobjectconfig': 'PEROBJECTCONFIG',
        'placeable': 'PLACEABLE',
        'pointer': 'POINTER',
        'postoperator': 'POSTOPERATOR',
        'preoperator': 'PREOPERATOR',
        'private': 'PRIVATE',
        'protected': 'PROTECTED',
        'reliable': 'RELIABLE',
        'remove': 'REMOVE',
        'replication': 'REPLICATION',
        'return': 'RETURN',
        'rng': 'RNG',
        'rot': 'ROT',
        'safereplace': 'SAFEREPLACE',
        'self': 'SELF',
        'showcategories': 'SHOWCATEGORIES',
        'simulated': 'SIMULATED',
        'singular': 'SINGULAR',
        'skip': 'SKIP',
        'state': 'STATE',
        'static': 'STATIC',
        'stop': 'STOP',
        'string': 'STRING',
        'struct': 'STRUCT',
        'super': 'SUPER',
        'switch': 'SWITCH',
        'transient': 'TRANSIENT',
        'travel': 'TRAVEL',
        'true': 'TRUE',
        'unreliable': 'UNRELIABLE',
        'until': 'UNTIL',
        'var': 'VAR',
        'vect': 'VECT',
        'while': 'WHILE',
        'within': 'WITHIN',
        # the following are keywords added by ulex
        'typeof': 'TYPEOF',
        'sizeof': 'SIZEOF',
        'template': 'TEMPLATE',
        'typedef': 'TYPEDEF'
    }

    tokens = [
        'COMMENT',
        'UNAME',
        'INTEGER',
        'SEMICOLON',
        'LPAREN',
        'RPAREN',
        'LSQUARE',
        'RSQUARE',
        'LANGLE',
        'RANGLE',
        'LCURLY',
        'RCURLY',
        'ASSIGN',
        'COMMA',
        'PERIOD',
        'LQUOTE',
        'RQUOTE',
        'USTRING',
        'EQUAL',
        'NEQUAL',
        'OR',
        'NOT',
        'INCREMENT',
        'ADD',
        'MULTIPLY',
        'AND',
        'MINUS',
        'COLON',
        'SEQUAL',
        'MODULUS',
        'SCONCAT',
        'SCONCATSPACE',
        'DIVIDE',
        'REFERENCE',
        'DIRECTIVE',
        'AMPERSAND',
        'BITWISE_AND',
        'BITWISE_OR',
        'LEFT_SHIFT',
        'RIGHT_SHIFT',
        'XOR',
        'BITWISE_NOT',
        'ID',
        ] + list(reserved.values())

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LSQUARE = r'\['
    t_RSQUARE = r'\]'
    t_LANGLE = r'\<'
    t_RANGLE = r'\>'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    t_LQUOTE = r'\"'
    t_RQUOTE = r'\"'
    t_ignore = '\r\t '
    t_SEMICOLON = r'\;'
    t_ASSIGN = r'\='
    t_COMMA = r','
    t_PERIOD = '\.'
    t_EQUAL = r'=='
    t_NEQUAL = r'!='
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_INCREMENT = r'\+\+'
    t_ADD = r'\+'
    t_MULTIPLY = r'\*'
    t_AND = r'&&'
    t_MINUS = r'-'
    t_COLON = r':'
    t_SEQUAL = r'~='
    t_MODULUS = r'%'
    t_SCONCAT = r'\$'
    t_SCONCATSPACE = r'@'
    t_DIVIDE = r'/'
    t_DIRECTIVE = r'\#(\w+)\s+(.+)'
    t_BITWISE_AND = r'\&'
    t_BITWISE_OR = r'\|'
    t_LEFT_SHIFT = r'<<'
    t_RIGHT_SHIFT = r'>>'
    t_XOR = r'\^'
    t_BITWISE_NOT = r'~'

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_REFERENCE(self, t):
        r'([a-zA-Z0-9_\-]+)\'([a-zA-Z0-9_\-\.]+)\''
        return t

    def t_UNAME(self, t):
        r'\'([a-zA-Z0-9_\- ]*)\''
        return t

    def t_USTRING(self, t):
        r'"((\\{2})*|(.*?[^\\](\\{2})*))"'
        return t

    def t_INTEGER(self, t):
        r'\d+'
        return t

    def t_FLOAT(self, t):
        r'\d+\.\d+'
        return t

    def t_COMMENT(self, t):
        r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        pass

    def input(self, data):
        self.lexer.input(data)

        #print len(list(iter(lex.token, None)))
        UnrealClass(iter(lex.token, None))


class UnrealPackage(object):
    def __init__(self):
        self.classes = dict()


class UnrealClass(dict):
    def __init__(self, token_iter):
        self.name = None
        self.super = None
        self.enums = dict()
        self.structs = dict()
        self.variables = dict()
        self.functions = dict()

        token = token_iter.next()

        if token.type != 'CLASS':
            raise Exception()

        token = token_iter.next()

        # class name
        if token.type != 'ID':
            raise Exception()

        self.name = token.value

        token = token_iter.next()

        if token.type != 'EXTENDS':
            raise Exception()

        # super
        token = token_iter.next()

        if token.type != 'ID':
            raise Exception()

        self.super = token.value

        print self.name, self.super

        # modifiers
        while True:
            token = token_iter.next()

            if token.type == 'SEMICOLON':
                break

            print token


class UnrealEnum(dict):
    def __init__(self):
        pass


class UnrealStruct(dict):
    def __init__(self):
        self.variables = []


class UnrealVariable(dict):
    def __init__(self):
        self.type = None
        self.name = ''
        self.access = 'public'


class UnrealLocal(dict):
    def __init__(self):
        pass


class UnrealFunction(dict):
    def __init__(self):
        self.name = ''
        self.acess = 'public'
        self.return_type = None
        self.static = False
        self.parameters = []
        self.simulated = False
        self.final = False
        self.iterator = False
        self.latent = False
        self.native = False
        self.singular = False
        self.exec_ = False


class UnrealFunctionParameter(dict):
    def __init__(self):
        self.type = None
        self.name = None
        self.optional = False
        self.out = False
        self.coerce = False
        self.skip = False

for root, dirs, files in os.walk('C:\Users\Colin\Documents\darkesthour'):
    for file in files:
        if os.path.splitext(file)[1] != '.uc':
            continue
        with open(os.path.join(root, file), 'rU') as f:
            content = f.read()
            lexer = UnrealLexer()
            try:
                lexer.input(content)
            except LexError as e:
                print 'Error: {} ({}, {})'.format(e, file, lexer.lexer.lineno)
