from ply import lex, yacc

primitive_types = {
    'float': 'FLOAT',
    'int': 'INT',
    'name': 'NAME',
    'bool': 'BOOL',
    'string': 'STRING',
    'byte': 'BYTE'
}

function_modifiers = [
    'EXEC',
    'FINAL',
    'ITERATOR',
    'LATENT',
    'NATIVE',
    'SIMULATED',
    'SINGULAR',
    'STATIC'
]

struct_modifers = [
    'TRANSIENT'
    'EXPORT'
    'INIT'
    'NATIVE'
]

class_modifiers = {
    'abstract': 'ABSTRACT',
    'cacheexempt': 'CACHEEXEMPT',
    'collapsecategories': 'COLLAPSECATEGORIES',
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
    'cache': 'CACHE',
    'config': 'CONFIG',
    'const': 'CONST',
    'deprecated': 'DEPRECATED',
    'edfindable': 'EDFINDABLE',
    'editconst': 'EDITCONST',
    'editconstarray': 'EDITCONSTARRAY',
    'editinline': 'EDITINLINE',
    'editinlinenotify': 'EDITINLINENOTIFY',
    'editinlineuse': 'EDITINLINEUSE',
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
    'if': 'IF',
    'ignores': 'IGNORES',
    'import': 'IMPORT',
    'init': 'INIT',
    'input': 'INPUT',
    #'insert': 'INSERT',
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
    #'remove': 'REMOVE',
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
    'HEX',
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
    'UFLOAT',
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


def t_DIRECTIVE(t):
    r'\#(\w+)\s+(.+)'


def t_REFERENCE(t):
    r'([a-zA-Z0-9_\-]+)\s*\'([a-zA-Z0-9_\-\.]+)\''
    return t


def t_UNAME(t):
    r'\'([a-zA-Z0-9_\- ]*)\''
    return t


def t_USTRING(t):
    r'"((\\{2})*|(.*?[^\\](\\{2})*))"'
    return t


def t_UFLOAT(t):
    r'[-+]?\d*?[.]\d+'
    t.value = float(t.value)
    return t


def t_HEX(t):
    r'0[xX][0-9a-fA-F]+'
    t.type = 'INTEGER'
    t.value = int(t.value, 0)
    return t


def t_INTEGER(t):
    r'[-+]?\d+'
    t.value = int(t.value)
    return t


def t_COMMENT(t):
    r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    pass

lexer = lex.lex()

start = 'class_declaration'


def p_empty(p):
    'empty :'
    p[0] = None


def p_arrayindex(p):
    'arrayindex : LSQUARE INTEGER RSQUARE'
    p[0] = p[2]


def p_arrayindex_opt(p):
    '''arrayindex_opt : arrayindex
                      | empty'''
    p[0] = p[1]


def p_var_name(p):
    'var_name : ID arrayindex_opt'
    p[0] = p[1], p[2]


def p_var_names(p):
    'var_names : var_name'


def p_var(p):
    'var : VAR type var_name'
    p[0] = p[2], p[3]


def p_generic_type(p):
    'generic_type : ID LANGLE type_list RANGLE'
    p[0] = p[1], p[3]


def p_array(p):
    'array : ARRAY LANGLE type RANGLE'
    p[0] = p[1], p[3]


def p_primitive_type(p):
    '''primitive_type : BOOL
                      | BYTE
                      | INT
                      | FLOAT
                      | STRING
                      | VECT
                      | ROT
                      | NAME'''
    p[0] = p[1]


def p_type(p):
    '''type : primitive_type
            | array
            | generic_type
            | ID'''
    p[0] = p[1]


def p_type_list(p):
    '''type_list : type
                 | type COMMA type_list'''
    if not isinstance(p[0], list):
        p[0] = list()
    p[0].append(p[1])
    if len(p) == 4:
        p[0] += p[3]


def p_template(p):
    'template : TEMPLATE LPAREN type_list RPAREN'
    p[0] = ('template', p[3])


def p_class_modifiers(p):
    '''class_modifiers : class_modifier
                       | class_modifier class_modifiers'''
    if not isinstance(p[0], list):
        p[0] = list()
    p[0].append(p[1])
    if len(p) == 3:
        p[0] += p[2]


def p_class_modifiers_opt(p):
    '''class_modifiers_opt : class_modifiers
                           | empty'''
    p[0] = p[1]


def p_class_modifier(p):
    '''class_modifier : ABSTRACT
                      | template'''
    p[0] = p[1]


def p_number(p):
    '''number : INTEGER
              | UFLOAT'''
    p[0] = p[1]


def p_constexpr(p):
    '''constexpr : number'''
    p[0] = p[1]


def p_extends(p):
    '''extends : EXTENDS ID
               | empty'''
    if p[1] is None:
        p[0] = None
    else:
        p[0] = p[2]


def p_class_declaration(p):
    'class_declaration : CLASS ID extends class_modifiers_opt SEMICOLON'
    print p[2], p[3], p[4]


def p_error(p):
    print 'error'
    print p

parser = yacc.yacc()

while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    parser.parse(s)

# for root, dirs, files in os.walk('C:\Users\colin_000\Documents\GitHub\DarkestHourDev\darkesthour'):
#     classes = files

#     for file in files:
#         if os.path.splitext(file)[1] != '.uc':
#             continue
#         with open(os.path.join(root, file), 'rU') as f:
#             content = f.read()
#             lexer = UnrealLexer()
#             try:
#                 lexer.input(content)
#             except LexError as e:
#                 print 'Error: {} ({}, {})'.format(e, file, lexer.lexer.lineno)
#             except Exception as e:
#                 print 'Error: {} ({}, {})'.format(e, file, lexer.lexer.lineno)
