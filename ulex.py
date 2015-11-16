import os
from ply import lex
#from ply import yacc
from ply.lex import LexError
from more_itertools import peekable
import sys


class UnrealLexer(object):

    primitive_types = {
        'float': 'FLOAT',
        'int': 'INT',
        'name': 'NAME',
        'bool': 'BOOL',
        'string': 'STRING',
        'byte': 'BYTE'
    }

    function_modifers = {
        'final': 'FINAL',
        'iterator': 'ITERATOR',
        'latent': 'LATENT',
        'native': 'NATIVE',
        'simulated': 'SIMULATED',
        'singular': 'SINGULAR'
    }

    class_modifiers = {
        'abstract': 'ABSTRACT',
        'cacheexempt': 'CACHEEXEMPT',
        'config': 'CONFIG',
        'dependson': 'DEPENDSON',
        'dontcollapsecategories': 'DONTCOLLAPSECATEGORIES',
        'editinlinenew': 'EDITINLINENEW',
        'exportstructs': 'EXPORTSTRUCTS',
        'hidecategories': 'HIDECATEGORIES',
        'hidedropdown': 'HIDEDROPDOWN',
        'instanced': 'INSTANCED',
        'native': 'NATIVE',
        'nativereplication': 'NATIVEREPLICATION',
        'noexport': 'NOEXPORT',
        'nonativereplication': 'NONATIVEREPLICATION',
        'noteditinlinenew': 'NOTEDITINLINENEW',
        'notplaceable': 'NOTPLACEABLE',
        'parseconfig': 'PARSECONFIG',
        'perobjectconfig': 'PEROBJECTCONFIG',
        'placeable': 'PLACEABLE',
        'safereplace': 'SAFEREPLACE',
        'showcategories': 'SHOWCATEGORIES',
        'transient': 'TRANSIENT',
        'within': 'WITHIN',
        'template': 'TEMPLATE'
    }

    access_modifiers = {
        'private': 'PRIVATE',
        'protected': 'PROTECTED'
    }

    function_parameter_modifiers = {
        'skip': 'SKIP',
        'out': 'OUT',
        'optional': 'OPTIONAL',
        'coerce': 'COERCE'
    }

    variable_modifiers = {
        'automated': 'AUTOMATED',
        'config': 'CONFIG',
        'const': 'CONST',
        'deprecated': 'DEPRECATED',
        'edfindable': 'EDFINDABLE',
        'editconst': 'EDITCONST',
        'editconstarray': 'EDITCONSTARRAY',
        'editinline': 'EDITINLINE',
        'export': 'EXPORT',
        'noexport': 'NOEXPORT',
        'globalconfig': 'GLOBALCONFIG',
        'input': 'INPUT',
        'localized': 'LOCALIZED',
        'native': 'NATIVE',
        #'pointer': 'POINTER',
        'private': 'PRIVATE',
        'protected': 'PROTECTED',
        'transient': 'TRANSIENT',
        'travel': 'TRAVEL',
    }

    reserved = {
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
        'continue': 'CONTINUE',
        'default': 'DEFAULT',
        'defaultproperties': 'DEFAULTPROPERTIES',
        'delegate': 'DELEGATE',
        'do': 'DO',
        'editinlinenotify': 'EDITINLINENOTIFY',
        'editinlineuse': 'EDITINLINEUSE',
        'else': 'ELSE',
        'enum': 'ENUM',
        'enumcount': 'ENUMCOUNT',
        'event': 'EVENT',
        'exec': 'EXEC',
        'expands': 'EXPANDS',
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
        'if': 'IF',
        'ignores': 'IGNORES',
        'import': 'IMPORT',
        'init': 'INIT',
        'input': 'INPUT',
        'insert': 'INSERT',
        'int': 'INT',
        'intrinsic': 'INTRINSIC',
        'invariant': 'INVARIANT',
        'iterator': 'ITERATOR',
        'latent': 'LATENT',
        'length': 'LENGTH',
        'local': 'LOCAL',
        'localized': 'LOCALIZED',
        'name': 'NAME',
        'new': 'NEW',
        'none': 'NONE',
        'nousercreate': 'NOUSERCREATE',
        'operator': 'OPERATOR',
        'optional': 'OPTIONAL',
        'out': 'OUT',
        #'pointer': 'POINTER',
        'postoperator': 'POSTOPERATOR',
        'preoperator': 'PREOPERATOR',
        'reliable': 'RELIABLE',
        'remove': 'REMOVE',
        'replication': 'REPLICATION',
        'return': 'RETURN',
        'rng': 'RNG',
        'rot': 'ROT',
        'self': 'SELF',
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
        'true': 'TRUE',
        'unreliable': 'UNRELIABLE',
        'until': 'UNTIL',
        'var': 'VAR',
        'vect': 'VECT',
        'while': 'WHILE',
        # the following are keywords added by ulex
        'typeof': 'TYPEOF',
        'sizeof': 'SIZEOF',
        'typedef': 'TYPEDEF'
    }

    reserved.update(class_modifiers)
    reserved.update(variable_modifiers)

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
    t_BITWISE_AND = r'\&'
    t_BITWISE_OR = r'\|'
    t_LEFT_SHIFT = r'<<'
    t_RIGHT_SHIFT = r'>>'
    t_XOR = r'\^'
    t_BITWISE_NOT = r'~'

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_DIRECTIVE(self, t):
        r'\#(\w+)\s+(.+)'

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
        UnrealClass(peekable(iter(lex.token, None)))


class UnrealPackage(object):
    def __init__(self):
        self.classes = dict()


def assert_next_token_type(token_iter, type):
    token = token_iter.next()

    if token.type != type:
        raise Exception('unexpected token \'{}\''.format(token.value))

    return token


def parse_template_parameters(token_iter):
    arguments = []

    assert_next_token_type(token_iter, 'LANGLE')

    while True:
        token = token_iter.next()

        if token.type == 'ARRAY':
            parse_template_parameters(token_iter)
        if token.type == 'ID':
            arguments.append(token.value)
        if token.type == 'RANGLE':
            break

    return arguments


def parse_modifier_arguments(token_iter):
    arguments = []

    assert_next_token_type(token_iter, 'LPAREN')

    while True:
        token = token_iter.next()

        if token.type == 'ID':
            arguments.append(token.value)
        if token.type == 'RPAREN':
            break

    return arguments


def parse_type(token_iter):
    token = token_iter.next()

    if token.type in UnrealLexer.primitive_types.values():
        return token.value
    elif token.type == 'ARRAY':  # array type must have one template parameter
        template_parameters = parse_template_parameters(token_iter)
        return token.value, template_parameters
    elif token.type == 'CLASS':
        token = token_iter.peek()
        template_parameters = None
        if token.type == 'LANGLE': # template parameters are optional when deducing class types!
            template_parameters = parse_template_parameters(token_iter)
        return token.value, template_parameters
    elif token.type == 'ENUM':
        return parse_enum(token_iter)
    elif token.type == 'ID':
        value = token.value
        token = token_iter.peek()
        template_parameters = None
        if token.type == 'LANGLE': # template parameters are optional on types!
            template_parameters = parse_template_parameters(token_iter)
        return value, template_parameters
    else:
        raise Exception('Unexpected token {}'.format(token))


def parse_enum(token_iter):
    token = assert_next_token_type(token_iter, 'ID')
    name = token.value
    values = []
    assert_next_token_type(token_iter, 'LCURLY')

    while True:
        token = token_iter.next()
        if token.type == 'ID':
            values.append(token.value)
        if token.type == 'RCURLY':
            break

    return name, values


def parse_function(token_iter):
    function = dict()
    modifiers = []

    while True:
        token = token_iter.next()

        if token.type in UnrealLexer.function_modifers.values():
            modifiers.append(token.value)
        elif token.type == 'FUNCTION' or token.type == 'EVENT':
            function['type'] = token.value
            break
        else:
            raise Exception('Unexpected token {}'.format(token))

    function['modifiers'] = modifiers

    # function return types can be absent...parsing this is going to be crazy
    tokens = []

    while True:
         token_iter.next()

    function['name'] = assert_next_token_type(token_iter, 'ID').value

    assert_next_token_type(token_iter, 'LPAREN')

    function['parameters'] = []

    while True:
        parameter = dict()
        parameter['modifiers'] = []

        # function parameter modifiers
        while True:
            token = token_iter.peek()
            if token.type in UnrealLexer.function_parameter_modifiers.values():
                token = token_iter.next()
                parameter['modifiers'].append(token.value)
            else:
                break

        parameter['type'] = parse_type(token_iter)
        parameter['name'] = assert_next_token_type(token_iter, 'ID')

        function['parameters'].append(parameter)

    return function

def parse_var(token_iter):
    vars = []

    assert_next_token_type(token_iter, 'VAR')

    token = token_iter.peek()

    # group (optional)
    if token.type == 'LPAREN':
        token_iter.next()  # consume LPAREN
        token = token_iter.peek()

        if token.type == 'ID':
            # group name
            token = token_iter.next()
            assert_next_token_type(token_iter, 'RPAREN')
            pass
        elif token.type == 'RPAREN':
            token = token_iter.next()  # consume RPAREN
            pass

    modifiers = []

    # modifiers
    while True:
        token = token_iter.peek()

        if token is None or token.value not in UnrealLexer.variable_modifiers.keys():
            break

        modifiers.append(token.value)

        token = token_iter.next()

        #print token.value

    # type
    var = dict()
    var['type'] = parse_type(token_iter)

    # name(s)
    while True:
        var['modifiers'] = modifiers
        var['name'] = assert_next_token_type(token_iter, 'ID').value

        # array length (optional)
        token = token_iter.peek()

        if token.type == 'LSQUARE':
            token_iter.next()  # consume LSQUARE
            var['length'] = assert_next_token_type(token_iter, 'INTEGER').value
            assert_next_token_type(token_iter, 'RSQUARE')

        token = token_iter.next()

        if token.type == 'COMMA':
            vars.append(var)
            continue
        elif token.type == 'SEMICOLON':
            vars.append(var)
            break
        else:
            raise Exception('Unexpected token {}'.format(token))

    return var


class UnrealClass(dict):
    def __init__(self, token_iter):
        self.super = None
        self.enums = dict()
        self.structs = dict()
        self.variables = dict()
        self.functions = dict()

        assert_next_token_type(token_iter, 'CLASS')

        token = assert_next_token_type(token_iter, 'ID')
        self['name'] = token.value

        token = token_iter.peek()

        if token.type == 'EXTENDS':
            token_iter.next()  # consume extends
            token = assert_next_token_type(token_iter, 'ID')
            self['super'] = token.value

        # modifiers
        while True:
            token = token_iter.next()

            if token.type == 'SEMICOLON':
                break

            elif token.type == 'CONFIG':
                token = token_iter.peek()
                if token.type == 'LPAREN':
                    token_iter.next()
                    token = assert_next_token_type(token_iter, 'ID')
                    self['config'] = token.value
                    assert_next_token_type(token_iter, 'RPAREN')
                else:
                    self['config'] = self['name']
            elif token.type == 'HIDECATEGORIES':
                self['hidecategories'] = parse_modifier_arguments(token_iter)
            elif token.type == 'SHOWCATEGORIES':
                self['showcategories'] = parse_modifier_arguments(token_iter)
            elif token.type == 'WITHIN':
                token = assert_next_token_type(token_iter, 'ID')
                self['within'] = token.value
            elif token.type == 'TEMPLATE':
                self['template'] = parse_modifier_arguments(token_iter)
            elif token.type not in UnrealLexer.class_modifiers.values():
                raise Exception(token.type)
            else:
                self[token.value] = True

        while True:
            try:
                token = token_iter.peek()
            except StopIteration:
                return

            if token.type == 'VAR':
                print parse_var(token_iter)
            elif token.type in UnrealLexer.function_modifers.values():
                print parse_function(token_iter)
            else:
                print token.type
                break


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

i = 0

for root, dirs, files in os.walk('C:\Program Files (x86)\Steam\SteamApps\common\Red Orchestra'):
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
            except Exception as e:
                print 'Error: {} ({}, {})'.format(e, file, lexer.lexer.lineno)

        i = i + 1

        if i > 100:
            sys.exit(0)
