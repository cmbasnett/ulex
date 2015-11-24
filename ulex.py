import os
from ply import lex
#from ply import yacc
from ply.lex import LexError
from more_itertools import peekable
import sys
import pprint


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
        'begin': 'BEGIN',
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
        'end': 'END',
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

    def t_FLOAT(self, t):
        r'[-+]?\d*?[.]\d+'
        return t

    def t_INTEGER(self, t):
        r'\d+'
        return t

    def t_COMMENT(self, t):
        r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value.lower(), 'ID')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        pass

    def input(self, data):
        self.lexer.input(data)

        #print len(list(iter(lex.token, None)))
        return UnrealClass(peekable(iter(lex.token, None)))


def assert_next_token_type(token_iter, type):
    token = token_iter.next()

    if token.type != type:
        raise Exception('Unexpected token \'{}\''.format(token.value))

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
        if token.type == 'LANGLE':  # template parameters are optional when deducing class types!
            template_parameters = parse_template_parameters(token_iter)
        return token.value, template_parameters
    elif token.type == 'ENUM':
        return parse_enum(token_iter)
    elif token.type == 'ID':
        value = token.value
        token = token_iter.peek()
        template_parameters = None
        if token.type == 'LANGLE':  # template parameters are optional on types!
            template_parameters = parse_template_parameters(token_iter)
            return value, template_parameters
        return value
    else:
        raise Exception('Malformed type (unexpected token {})'.format(token.type))


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


def parse_property(token_iter):
    token = token_iter.next()

    if token.type == 'LPAREN':
        values = dict()

        while True:
            key = assert_next_token_type(token_iter, 'ID').value

            # check for redundant data
            if key in values.keys():
                raise Exception('Redundant sub-object property ({})'.format(key))

            assert_next_token_type(token_iter, 'ASSIGN')
            value = parse_property(token_iter)

            values[key] = value

            token = token_iter.next()

            if token.type == 'COMMA':
                continue
            elif token.type == 'RPAREN':
                break
            else:
                raise Exception('Unexpected token {} (expected COMMA or RPAREN)'.format(token))

        return values
    else:
        return token.value


def parse_function(token_iter, modifiers):
    function = dict()
    function['modifiers'] = modifiers

    token = token_iter.next()

    if token.type == 'FUNCTION' or token.type == 'EVENT':
        function['type'] = token.value
    else:
        raise Exception('Unexpected token {}'.format(token))

    # function return types can be absent...parsing this is going to be crazy
    temp = parse_type(token_iter)

    # if next token is not an LPAREN, previous one was a return type and next is the function name
    token = token_iter.peek()

    if token.type == 'LPAREN':
        print type(temp)
        if not isinstance(temp, str):
            raise Exception('missing function name')
        function['name'] = temp
        # previous token was not a type, ensure
    elif token.type == 'ID':
        function['return-type'] = temp
        function['name'] = assert_next_token_type(token_iter, 'ID').value
    else:
        raise Exception('unexpected token {} (expected LPAREN or ID)'.format(token))

    assert_next_token_type(token_iter, 'LPAREN')

    function['parameters'] = []

    while True:
        token = token_iter.peek()

        if token.type == 'RPAREN':
            token_iter.next()
            break

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

    # TODO: parse local variables types

    # parse everything until a matching brace is found
    assert_next_token_type(token_iter, 'LCURLY')

    i = 0

    while True:
        token = token_iter.next()

        if token.type == 'LCURLY':
            i = i + 1
        elif token.type == 'RCURLY':
            i = i - 1
            if i < 0:
                break

    return function


class UnrealClass(dict):

    def parse_defaultproperties(self, token_iter):
        assert_next_token_type(token_iter, 'DEFAULTPROPERTIES')
        assert_next_token_type(token_iter, 'LCURLY')

        objects = dict()
        key = ''

        while True:
            token = token_iter.next()

            if token.type == 'RCURLY':
                break
            elif token.type == 'BEGIN':
                token = assert_next_token_type(token_iter, 'ID')

                if token.value != 'Object':  # object should be treated as a reserved word
                    raise Exception('unexpected')

                assert_next_token_type(token_iter, 'CLASS')
                assert_next_token_type(token_iter, 'ASSIGN')
                classname = assert_next_token_type(token_iter, 'ID').value
                assert_next_token_type(token_iter, 'NAME')
                assert_next_token_type(token_iter, 'ASSIGN')
                name = assert_next_token_type(token_iter, 'ID').value

                while True:
                    token = token_iter.next()

                    if token.type == 'END':
                        token = assert_next_token_type(token_iter, 'ID')

                        if token.value.upper() != 'OBJECT':
                            raise Exception('Unexpected token {} (expected \'OBJECT\''.format(token))

                        break
                    if token.type == 'ID':
                        key = token.value

                        token = token_iter.peek()

                        if token.type == 'LPAREN':
                            # array index indicator
                            token_iter.next()   # consume lparen

                            token = token_iter.next()

                            if token.type != 'INTEGER':
                                raise Exception('Unexpected token (expected integer)')

                            assert_next_token_type(token_iter, 'RPAREN')

                        assert_next_token_type(token_iter, 'ASSIGN')

                        value = parse_property(token_iter)
            elif token.type == 'ID':
                key = token.value

                token = token_iter.peek()

                if token.type == 'LPAREN':
                    # array index indicator
                    token_iter.next()   # consume lparen

                    token = token_iter.next()

                    if token.type != 'INTEGER':
                        raise Exception('Unexpected token (expected integer)')

                    assert_next_token_type(token_iter, 'RPAREN')

                assert_next_token_type(token_iter, 'ASSIGN')

                value = parse_property(token_iter)

                self.defaultproperties[key] = value
            else:
                raise Exception('Unexpected token {}'.format(token))

    def parse_var(self, token_iter):
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

                token = token_iter.peek()

                if token.type == 'ID':
                    token_iter.next()
                    # look-up constant value
                    if token.value in self.constants.keys():
                        var['length'] = self.constants[token.value]
                    else:
                        raise Exception('Array length for variable {} does not name a known constant'.format(token.value))
                elif token.type == 'INTEGER':
                    var['length'] = assert_next_token_type(token_iter, 'INTEGER').value

                assert_next_token_type(token_iter, 'RSQUARE')

            token = token_iter.next()

            if token.type == 'COMMA':
                self.variables[var['name']] = var
                continue
            elif token.type == 'SEMICOLON':
                self.variables[var['name']] = var
                break
            else:
                raise Exception('Unexpected token {}'.format(token))

    def parse_const(self, token_iter):
        assert_next_token_type(token_iter, 'CONST')
        name = assert_next_token_type(token_iter, 'ID').value
        assert_next_token_type(token_iter, 'ASSIGN')
        value = token_iter.next().value
        assert_next_token_type(token_iter, 'SEMICOLON')
        self.constants[name] = value

    def parse_state(self, token_iter, modifiers):
        assert_next_token_type(token_iter, 'STATE')

        token = token_iter.peek()

        if token.type == 'LPAREN':
            token_iter.next()  # consume LPAREN
            assert_next_token_type(token_iter, 'RPAREN')

        name = assert_next_token_type(token_iter, 'ID').value

        token = token_iter.peek()

        if token.type == 'EXTENDS':
            token_iter.next()  # consume EXTENDS
            superclass = assert_next_token_type(token_iter, 'ID').value

        assert_next_token_type(token_iter, 'LCURLY')

        # iterate until matching curly is found
        i = 0

        while True:
            token = token_iter.next()

            if token.type == 'LCURLY':
                i = i + 1
            elif token.type == 'RCURLY':
                i = i - 1
                if i < 0:
                    break

        print name

    def __init__(self, token_iter):
        self.super = None
        self.enums = dict()
        self.structs = dict()
        self.variables = dict()
        self.functions = dict()
        self.constants = dict()
        self.defaultproperties = dict()

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

        modifiers = []

        while True:
            try:
                token = token_iter.peek()
            except StopIteration:
                return

            if token.type == 'VAR':
                self.parse_var(token_iter)
            elif token.type in UnrealLexer.function_modifers.values():
                modifiers = []
                while True:
                    token = token_iter.peek()
                    if token.type in UnrealLexer.function_modifers.values():
                        modifiers.append(token.value)
                        token_iter.next()
                    elif token.type == 'FUNCTION' or token.type == 'EVENT':
                        parse_function(token_iter, modifiers)  # make member of class
                        break
                    elif token.type == 'STATE':
                        self.parse_state(token_iter, modifiers)
                    else:
                        raise Exception('Unexpected token {}'.format(token))
                    modifiers.append(token.value)
            elif token.type == 'FUNCTION' or token.type == 'EVENT':
                parse_function(token_iter, [])
            elif token.type == 'STATE':
                self.parse_state(token_iter, [])
            elif token.type == 'DEFAULTPROPERTIES':
                self.parse_defaultproperties(token_iter)
            elif token.type == 'CONST':
                self.parse_const(token_iter)
            else:
                print token.type
                break

        pprint.pprint(self.defaultproperties)

i = 0

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
            except Exception as e:
                print 'Error: {} ({}, {})'.format(e, file, lexer.lexer.lineno)

        i = i + 1

        if i > 50:
            sys.exit(0)
