from ply import yacc
from lux import tokens
import os

constants = dict()
start = 'start'


def error(p, s):
    print p.lexer.lineno, s
    raise SyntaxError


def p_empty(p):
    'empty :'
    p[0] = None


def p_arrayindex(p):
    'arrayindex : LSQUARE INTEGER RSQUARE'
    p[0] = p[2]


def p_arrayindex_or_empty(p):
    '''arrayindex_or_empty : arrayindex
                           | empty'''
    p[0] = p[1]


def p_var_names_1(p):
    'var_names : var_name'
    p[0] = [p[1]]


def p_var_names_2(p):
    'var_names : var_names COMMA var_name'
    p[0] = p[1] + [p[3]]


def p_var_name(p):
    'var_name : ID arrayindex_or_empty'
    p[0] = p[1], p[2]


def p_var_modifier(p):
    '''var_modifier     : AUTOMATED
                        | CACHE
                        | config
                        | CONST
                        | DEPRECATED
                        | EDFINDABLE
                        | EDITCONST
                        | EDITCONSTARRAY
                        | EDITINLINE
                        | EDITINLINENOTIFY
                        | EDITINLINEUSE
                        | EXPORT
                        | NOEXPORT
                        | GLOBALCONFIG
                        | INPUT
                        | LOCALIZED
                        | NATIVE
                        | PRIVATE
                        | PROTECTED
                        | TRANSIENT
                        | TRAVEL'''
    p[0] = p[1]


def p_var_modifiers_1(p):
    'var_modifiers : var_modifier'
    p[0] = [p[1]]


def p_var_modifiers_2(p):
    'var_modifiers : var_modifiers var_modifier'
    p[0] = p[1] + [p[2]]


def p_var_modifiers_or_empty(p):
    '''var_modifiers_or_empty : var_modifiers
                              | empty'''
    p[0] = p[1]


def p_var_declaration(p):
    'var_declaration : VAR var_modifiers_or_empty type var_names SEMICOLON'
    p[0] = ('var-declaration', (p[3], p[4], p[2]))
    print p[0]


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


def p_type_or_empty(p):
    '''type_or_empty : type
                     | empty'''
    p[0] = p[1]


def p_id_list_1(p):
    'id_list : ID'
    p[0] = [p[1]]


def p_id_list_2(p):
    'id_list : id_list COMMA ID'
    p[0] = p[1] + [p[3]]


def p_type_list_1(p):
    'type_list : type'
    p[0] = [p[1]]


def p_type_list_2(p):
    'type_list : type_list COMMA type'
    p[0] = p[1] + [p[3]]


def p_id_or_empty(p):
    '''id_or_empty : ID
                   | empty'''
    p[0] = p[1]


def p_paren_id_or_empty(p):
    '''paren_id_or_empty : LPAREN id_or_empty RPAREN
                         | empty'''
    if p[1] is None:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_config(p):
    '''config : CONFIG paren_id_or_empty'''
    p[0] = p[1], p[2]


def p_template(p):
    'template : TEMPLATE LPAREN id_list RPAREN'
    if len(p[3]) > len(set(p[3])):
        error(p, 'Template parameters must be unique.')
        raise SyntaxError
    p[0] = ('template', p[3])


def p_class_modifier(p):
    '''class_modifier : ABSTRACT
                      | config
                      | NOTPLACEABLE
                      | PLACEABLE
                      | NATIVE
                      | NATIVEREPLICATION
                      | NONATIVEREPLICATION
                      | PEROBJECTCONFIG
                      | TRANSIENT
                      | NOEXPORT
                      | dependson
                      | within
                      | template'''
    p[0] = p[1]


def p_class_modifiers_1(p):
    'class_modifiers : class_modifiers class_modifier'
    p[0] = p[1] + [p[2]]


def p_class_modifiers_2(p):
    'class_modifiers : class_modifier'
    p[0] = [p[1]]


def p_class_modifiers_or_empty(p):
    '''class_modifiers_or_empty : class_modifiers
                                | empty'''
    p[0] = p[1]


def p_within(p):
    'within : WITHIN ID'
    p[0] = p[1], p[2]


def p_dependson(p):
    'dependson : DEPENDSON LPAREN ID RPAREN'
    p[0] = p[1], p[3]
    p[0] = p[1]


def p_number(p):
    '''number : INTEGER
              | UFLOAT'''
    p[0] = p[1]


def p_const_declaration(p):
    'const_declaration : CONST ID ASSIGN constexpr SEMICOLON'
    global constants
    #constants[p[2]] = p[4]
    p[0] = ('const-declaration' (p[2], p[4]))


def p_constexpr(p):
    '''constexpr : number
                 | USTRING
                 | TRUE
                 | FALSE'''
    p[0] = p[1]


def p_extends_1(p):
    'extends : empty'


def p_extends_2(p):
    'extends : EXTENDS ID'
    p[0] = p[2]


def p_class_declaration(p):
    'class_declaration : CLASS ID extends class_modifiers_or_empty SEMICOLON'
    if p[2] == p[3]:
        error(p, 'Classes cannot extend themselves.')
        raise SyntaxError
    p[0] = ('class-declaration', (p[2], p[3], p[4]))
    print p[0]


def p_struct_declaration(p):
    '''struct_declaration : STRUCT ID extends LCURLY RCURLY'''
    p[0] = p[2], p[3]


def p_function_modifier(p):
    '''function_modifier : EXEC
                         | FINAL
                         | ITERATOR
                         | LATENT
                         | NATIVE
                         | SIMULATED
                         | SINGULAR
                         | STATIC'''
    p[0] = p[1]


def p_function_modifiers_1(p):
    'function_modifiers : function_modifiers function_modifier'
    p[0] = p[1] + [p[2]]


def p_function_modifiers_2(p):
    'function_modifiers : function_modifier'
    p[0] = [p[1]]


def p_function_modifiers_or_empty(p):
    '''function_modifiers_or_empty : function_modifiers
                                   | empty'''
    p[0] = p[1]


def p_function_type(p):
    '''function_type : DELEGATE
                     | FUNCTION
                     | EVENT'''
    p[0] = p[1]


def p_function_argument_modifier(p):
    '''function_argument_modifier : OPTIONAL
                                  | COERCE
                                  | OUT
                                  | SKIP'''
    p[0] = p[1]


def p_function_argument_modifier_or_empty(p):
    '''function_argument_modifier_or_empty : function_argument_modifier
                                           | empty'''
    p[0] = p[1]


def p_function_argument(p):
    '''function_argument : function_argument_modifier_or_empty type ID'''
    p[0] = p[3], p[2], p[1]


def p_function_arguments_1(p):
    'function_arguments : function_argument'
    p[0] = [p[1]]


def p_function_arguments_2(p):
    'function_arguments : function_arguments COMMA function_argument'
    p[0] = p[1] + [p[3]]


def p_function_arguments_or_empty(p):
    '''function_arguments_or_empty : function_arguments
                                   | empty'''
    p[0] = p[1]


def p_local_declaration(p):
    'local_declaration : LOCAL type var_names SEMICOLON'
    p[0] = ('local-declaration', (p[2], p[3]))


def p_local_declarations_1(p):
    'local_declarations : local_declaration'
    p[0] = [p[1]]


def p_local_declarations_2(p):
    'local_declarations : local_declarations local_declaration'
    p[0] = p[1] + [p[2]]


def p_function_declaration(p):
    '''function_declaration : function_modifiers_or_empty function_type type ID LPAREN function_arguments_or_empty RPAREN
                            | function_modifiers_or_empty function_type ID LPAREN function_arguments_or_empty RPAREN'''
    if len(p) == 8:  # return type
        p[0] = ('function-declaration', (p[4], p[3], p[2], p[1], p[6]))
    else:            # no return type
        p[0] = ('function-declaration', (p[3], None, p[2], p[1], p[5]))

    print p[0]


def p_function_definition(p):
    '''function_definition : function_declaration SEMICOLON
                           | function_declaration LCURLY function_body RCURLY'''
    if len(p) == 2:  # no body
        p[0] = ('function-definition', p[1])
    else:
        p[0] = ('function-definition', (p[1], p[2]))


def p_declaration(p):
    '''declaration : const_declaration
                   | function_definition
                   | var_declaration'''


def p_declarations_1(p):
    'declarations : declaration'
    p[0] = [p[1]]


def p_declarations_2(p):
    'declarations : declarations declaration'
    p[0] = p[1] + [p[2]]


#def p_defaultproperties_object(p):
    #'defaultproperties_object : BEGIN OBJECT CLASS ASSIGN type NAME ASSIGN ID defaultproperties_object_assignments_or_empty END OBJECT'


def p_defaultproperties_assignment_value(p):
    '''defaultproperties_assignment_value : constexpr'''
    p[0] = p[1]


def p_defaultproperties_assignment(p):
    'defaultproperties_assignment : var_name ASSIGN defaultproperties_assignment_value'
    p[0] = ('defaultproperties-assignment', (p[1], p[3]))


def p_defaultproperties_assignments_1(p):
    'defaultproperties_assignments : defaultproperties_assignment'
    p[0] = [p[1]]


def p_defaultproperties_assignments_2(p):
    'defaultproperties_assignments : defaultproperties_assignments defaultproperties_assignment'
    p[0] = p[1] + [p[2]]


def p_defaultproperties_assignments_or_empty(p):
    '''defaultproperties_assignments_or_empty : defaultproperties_assignments
                                              | empty'''
    p[0] = p[1]


def p_defaultproperties(p):
    'defaultproperties : DEFAULTPROPERTIES LCURLY defaultproperties_assignments_or_empty RCURLY'
    p[0] = ('defaultproperties', (p[3]))


def p_local_declarations_or_empty(p):
    '''local_declarations_or_empty : local_declarations
                                   | empty'''
    p[0] = p[1]


def p_function_body(p):
    'function_body : local_declarations_or_empty expressions'
    p[0] = ('function-body', (p[1], p[2]))


def p_expression(p):
    '''expression : constexpr'''
    print p[1]
    p[0] = p[1]


def p_expressions_1(p):
    'expressions : expression'
    p[0] = [p[1]]


def p_expressions_2(p):
    'expressions : expressions expression'
    p[0] = p[1] + [p[2]]


def p_return_statement(p):
    'return_statement : RETURN expression'
    p[0] = ('return-statement', p[2])


def p_start(p):
    'start : class_declaration declarations'
    print p[1]
    p[0] = p[1]


def p_error(p):
    print p
    pass


def p_for_block(p):
    '''for_block : FOR LPAREN assignments_or_empty SEMICOLON expression_or_empty SEMICOLON expression_or_empty RPAREN LCURLY statements_or_empty RCURLY'''
    p[0] = ('for-block', (p[3], p[5], p[7]))

def p_while_block(p):
    '''while_block : WHILE LPAREN expression_or_empty RPAREN'''
    p[0] = ('while-block', ())


parser = yacc.yacc()

for root, dirs, files in os.walk('C:\Users\colin_000\Documents\GitHub\DarkestHourDev\darkesthour\UCore\Classes'):
    for file in files:
        with open(os.path.join(root, file), 'rb') as f:
            parser.parse(f.read())
