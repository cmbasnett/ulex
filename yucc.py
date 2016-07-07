from ply import yacc
from lux import tokens
import pprint

start = 'start'


def p_pre_unary_operator(p):
    '''pre_unary_operator : MINUS
                          | NOT
                          | INCREMENT
                          | DECREMENT
                          | BITWISE_NOT'''
    p[0] = p[1]


def p_post_unary_operator(p):
    '''post_unary_operator : INCREMENT
                           | DECREMENT'''
    p[0] = p[1]


def p_unary_operation_1(p):
    'unary_operation : pre_unary_operator expression'
    p[0] = ('pre_unary_operation', p[1], p[2])


def p_unary_operation_2(p):
    'unary_operation : expression post_unary_operator'
    p[0] = ('post_unary_operation', p[1], p[2])


def p_binary_operator(p):
    '''binary_operator : EQUAL
                       | NEQUAL
                       | LEQUAL
                       | GEQUAL
                       | SEQUAL
                       | MODULUS
                       | MULTIPLY
                       | DIVIDE
                       | ADD
                       | MINUS
                       | LANGLE
                       | RANGLE
                       | SCONCAT
                       | SCONCATSPACE
                       | OR
                       | IASSIGN
                       | DASSIGN
                       | AND'''
    p[0] = p[1]


def p_vect(p):
    'vect : VECT LPAREN number COMMA number COMMA number RPAREN'
    p[0] = ('vect', p[3], p[5], p[7])


def p_arraycount(p):
    'arraycount : ARRAYCOUNT LPAREN expression RPAREN'
    p[0] = ('arraycount', p[3])


def p_default(p):
    'default : DEFAULT PERIOD identifier'
    p[0] = ('default', p[3])


def p_allocation_1(p):
    'allocation : NEW REFERENCE'
    p[0] = ('allocation', p[2])


def p_allocation_2(p):
    'allocation : NEW generic_type'
    p[0] = ('allocation', generic_type_to_reference(p[2]))


def generic_type_to_reference(p):
    assert(p[0] == 'generic_type')
    s = '_'.join([p[1][1], '_'.join([q[1][1] for q in p[2]])])
    return ('reference', 'class\'%s\'' % s)


def p_binary_operation(p):
    'binary_operation : expression binary_operator expression'
    p[0] = ('binary_operation', p[2], p[1], p[3])


def p_identifier(p):
    '''identifier : ID
                  | INIT
                  | CLASS
                  | primitive_type
                  | SELF'''
    p[0] = ('identifier', p[1])


def p_reference(p):
    'reference : REFERENCE'
    p[0] = ('reference', p[1])


def p_atom(p):
    '''atom : identifier
            | literal
            | reference
            | allocation'''
    p[0] = p[1]


def p_subscription(p):
    'subscription : primary LSQUARE expression RSQUARE'
    p[0] = ('subscription', p[1], p[3])


def p_string_parameterized(p):
    'string_parameterized : PSTRING'
    p[0] = ('string_parameterized', p[1])


def p_primary(p):
    '''primary : atom
               | attribute
               | default
               | subscription
               | super_call
               | static_call
               | global_call
               | call
               | unary_operation
               | binary_operation'''
    p[0] = p[1]


def p_argument_list_1(p):
    'argument_list : expression_or_empty'
    p[0] = [p[1]]


def p_argument_list_2(p):
    'argument_list : argument_list COMMA expression_or_empty'
    p[0] = p[1] + [p[3]]


def p_argument_list_or_empty(p):
    '''argument_list_or_empty : argument_list
                              | empty'''
    if p[1] is None:
        p[1] = []
    p[0] = ('argument_list', p[1])


def p_call(p):
    '''call : primary LPAREN argument_list_or_empty RPAREN'''
    p[0] = ('call', p[1], p[3])


def p_attribute(p):
    'attribute : primary PERIOD primary'
    p[0] = ('attribute', p[1], p[3])


def p_target(p):
    '''target : identifier
              | attribute
              | default
              | subscription'''
    p[0] = p[1]


def p_assignment_statement(p):
    'assignment_statement : target ASSIGN expression'
    p[0] = ('assignment_statement', p[1], p[3])


def p_string_literal(p):
    'string_literal : USTRING'
    p[0] = p[1]


def p_name_literal(p):
    'name_literal : UNAME'
    p[0] = p[1]


def p_boolean_literal(p):
    '''boolean_literal : FALSE
                       | TRUE'''
    p[0] = p[1]


def p_literal(p):
    '''literal : string_literal
               | name_literal
               | number
               | vect
               | arraycount
               | boolean_literal
               | NONE'''
    p[0] = p[1]


def error(p, s):
    print p
    raise SyntaxError


def p_empty(p):
    'empty :'
    p[0] = None


def p_arrayindex(p):
    '''arrayindex : LSQUARE INTEGER RSQUARE
                  | LSQUARE identifier RSQUARE'''
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


def p_var_name_list(p):
    'var_name_list : var_names'
    p[0] = ('var_name_list', p[1])


def p_var_name(p):
    'var_name : identifier arrayindex_or_empty'
    p[0] = ('var_name', p[1], p[2])


#TODO: varnames with AST identifier properly please


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
    'var_declaration : VAR paren_id_or_empty var_modifiers_or_empty var_type var_name_list SEMICOLON'
    p[0] = ('var_declaration', p[4], p[5], p[3], p[2])


def p_struct_var_declaration(p):
    'struct_var_declaration : VAR type var_name_list SEMICOLON'
    p[0] = ('struct_var_declaration', p[2], p[3])


def p_struct_var_declarations_1(p):
    'struct_var_declarations : struct_var_declaration'
    p[0] = [p[1]]


def p_struct_var_declarations_2(p):
    'struct_var_declarations : struct_var_declarations struct_var_declaration'
    p[0] = p[1] + [p[2]]


def p_struct_var_declarations_or_empty(p):
    '''struct_var_declarations_or_empty : struct_var_declarations
                                        | empty'''
    p[0] = ('struct_var_declarations', p[1])


def p_generic_type(p):
    'generic_type : identifier LANGLE type_list RANGLE'
    p[0] = ('generic_type', p[1], p[3])


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


def p_typeof(p):
    'typeof : TYPEOF LPAREN identifier RPAREN'
    p[0] = ('typeof', p[3])


def p_class_type(p):
    'class_type : CLASS LANGLE identifier RANGLE'
    p[0] = ('class_type', p[3])


def p_var_type(p):
    '''var_type : type
                | struct_declaration'''
    p[0] = p[1]


def p_type(p):
    '''type : primitive_type
            | array
            | generic_type
            | class_type
            | identifier'''
    p[0] = ('type', p[1])


def p_type_or_empty(p):
    '''type_or_empty : type
                     | empty'''
    p[0] = p[1]


def p_identifier_list_1(p):
    'identifier_list : identifier'
    p[0] = [p[1]]


def p_identifier_list_2(p):
    'identifier_list : identifier_list COMMA identifier'
    p[0] = p[1] + [p[3]]

def p_identifier_list_or_empty(p):
    '''identifier_list_or_empty : identifier_list
                                | empty'''
    p[0] = ('identifier_list', p[1])


def p_type_list_1(p):
    'type_list : type'
    p[0] = [p[1]]


def p_type_list_2(p):
    'type_list : type_list COMMA type'
    p[0] = p[1] + [p[3]]


def p_id_or_empty(p):
    '''id_or_empty : identifier
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
    'template : TEMPLATE LPAREN identifier_list_or_empty RPAREN'
    if len(p[3][1]) > len(set(p[3][1])):
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
    if p[1] is None:
        p[1] = []
    p[0] = ('class_modifiers', p[1])


def p_within(p):
    'within : WITHIN identifier'
    p[0] = p[1], p[2]


def p_dependson(p):
    'dependson : DEPENDSON LPAREN identifier RPAREN'
    p[0] = ('dependson', p[3])


def p_number(p):
    '''number : INTEGER
              | UFLOAT'''
    p[0] = ('number', p[1])


def p_const_declaration(p):
    'const_declaration : CONST identifier ASSIGN literal SEMICOLON'
    p[0] = ('const_declaration', p[2], p[4])


def p_extends_1(p):
    'extends : empty'


def p_extends_2(p):
    'extends : EXTENDS type'
    p[0] = p[2]


def p_class_declaration(p):
    'class_declaration : CLASS identifier extends class_modifiers_or_empty SEMICOLON'
    p[0] = ('class_declaration', p[2], p[3], p[4])


def p_struct_declaration(p):
    '''struct_declaration : STRUCT identifier LCURLY struct_var_declarations_or_empty RCURLY'''
    p[0] = ('struct_declaration', p[2], p[4])


def p_function_modifier(p):
    '''function_modifier : EXEC
                         | FINAL
                         | ITERATOR
                         | LATENT
                         | NATIVE
                         | SIMULATED
                         | SINGULAR
                         | STATIC
                         | PRIVATE'''
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
    if p[1] is None:
        p[1] = []

    p[0] = ('function_modifiers', p[1])


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


def p_function_argument_modifiers_1(p):
    'function_argument_modifiers : function_argument_modifier'
    p[0] = [p[1]]


def p_function_argument_modifiers_2(p):
    'function_argument_modifiers : function_argument_modifiers function_argument_modifier'
    p[0] = p[1] + [p[2]]


def p_function_argument_modifiers_or_empty(p):
    '''function_argument_modifiers_or_empty : function_argument_modifiers
                                            | empty'''
    p[0] = p[1]


def p_function_argument(p):
    '''function_argument : function_argument_modifiers_or_empty type identifier'''
    p[0] = ('function_argument', p[2], p[1], p[3])


def p_function_arguments_1(p):
    'function_arguments : function_argument'
    p[0] = [p[1]]


def p_function_arguments_2(p):
    'function_arguments : function_arguments COMMA function_argument'
    p[0] = p[1] + [p[3]]


def p_function_arguments_or_empty(p):
    '''function_arguments_or_empty : function_arguments
                                   | empty'''
    if p[1] is None:
        p[1] = []

    p[0] = ('function_arguments', p[1])


def p_local_declaration(p):
    'local_declaration : LOCAL type var_name_list SEMICOLON'
    p[0] = ('local_declaration', p[2], p[3])


def p_local_declarations_1(p):
    'local_declarations : local_declaration'
    p[0] = [p[1]]


def p_local_declarations_2(p):
    'local_declarations : local_declarations local_declaration'
    p[0] = p[1] + [p[2]]


def p_constructor_declaration(p):
    'constructor : CONSTRUCTOR LPAREN function_arguments_or_empty RPAREN LCURLY function_body RCURLY'
    p[0] = ('constructor', p[3], p[6])


# TODO: split in _1 and _2
def p_function_declaration(p):
    '''function_declaration : function_modifiers_or_empty function_type function_modifiers_or_empty type identifier LPAREN function_arguments_or_empty RPAREN
                            | function_modifiers_or_empty function_type function_modifiers_or_empty identifier LPAREN function_arguments_or_empty RPAREN'''
    # TODO: this is ugly
    function_modifiers = p[1]
    function_modifiers[1] + p[3][1]
    if len(p) == 9:  # return type
        p[0] = ('function_declaration', p[2], p[5], p[4], function_modifiers, p[7])
    else:            # no return type
        p[0] = ('function_declaration', p[2], p[4], None, function_modifiers, p[6])


def p_function_definition(p):
    '''function_definition : function_declaration SEMICOLON
                           | function_declaration LCURLY function_body RCURLY'''
    if len(p) == 3:  # no body
        p[0] = ('function_definition', p[1], None)
    else:            # body
        p[0] = ('function_definition', p[1], p[3])

    if p[0][1][0].lower() == 'delegate' and p[0][2] is not None:
        raise SyntaxError


def p_declaration(p):
    '''declaration : const_declaration
                   | function_definition
                   | constructor
                   | var_declaration
                   | state_definition'''
    p[0] = p[1]


def p_declarations_1(p):
    'declarations : declaration'
    p[0] = [p[1]]


def p_declarations_2(p):
    'declarations : declarations declaration'
    p[0] = p[1] + [p[2]]


def p_declarations_or_empty(p):
    '''declarations_or_empty : declarations
                             | empty'''
    p[0] = ('declarations', p[1])


#def p_defaultproperties_object(p):
    #'defaultproperties_object : BEGIN OBJECT CLASS ASSIGN type NAME ASSIGN ID defaultproperties_object_assignments_or_empty END OBJECT'


def p_defaultproperties_assignment_value(p):
    '''defaultproperties_assignment_value : literal'''
    p[0] = p[1]


def p_defaultproperties_assignment(p):
    'defaultproperties_assignment : var_name ASSIGN defaultproperties_assignment_value'
    p[0] = ('defaultproperties-assignment', p[1], p[3])


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
    p[0] = ('defaultproperties', p[3])


def p_local_declarations_or_empty(p):
    '''local_declarations_or_empty : local_declarations
                                   | empty'''
    p[0] = ('local_declarations', p[1])


def p_function_body(p):
    'function_body : local_declarations_or_empty statements_or_empty'
    p[0] = ('function_body', p[1], p[2])


def p_expression_1(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_2(p):
    'expression : primary'
    p[0] = p[1]


def p_expression_or_empty(p):
    '''expression_or_empty : expression
                           | empty'''
    p[0] = p[1]


def p_simple_statement(p):
    '''simple_statement : return_statement
                        | break_statement
                        | continue_statement
                        | assignment_statement
                        | expression'''
    p[0] = p[1]


def p_simple_statement_list_1(p):
    'simple_statement_list : simple_statement'
    p[0] = [p[1]]


def p_simple_statement_list_2(p):
    'simple_statement_list : simple_statement_list COMMA simple_statement'
    p[0] = p[1] + [p[2]]


def p_simple_statement_list_or_empty(p):
    '''simple_statement_list_or_empty : simple_statement_list
                                      | empty'''
    p[0] = p[1]


def p_return_statement(p):
    'return_statement : RETURN expression_or_empty'
    p[0] = ('return_statement', p[2])


def p_start(p):
    'start : class_declaration declarations_or_empty'
    p[0] = ('start', [p[1]] + [p[2]])


def p_break_statement(p):
    'break_statement : BREAK'
    p[0] = ('break_statement', p[1])


def p_continue_statement(p):
    'continue_statement : CONTINUE'
    p[0] = ('continue_statement', p[1])


def p_error(p):
    raise SyntaxError((p.lexer.lineno, p))


def p_codeline(p):
    '''codeline : simple_statement SEMICOLON'''
    p[0] = ('codeline', p[1])


def p_statement(p):
    '''statement : codeline
                 | compound_statement'''
    p[0] = p[1]


def p_statements_1(p):
    'statements : statement'
    p[0] = [p[1]]


def p_statements_2(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]


def p_statements_or_empty(p):
    '''statements_or_empty : statements
                           | empty'''
    p[0] = ('statements', p[1])


def p_compound_statement(p):
    '''compound_statement : for_statement
                          | foreach_statement
                          | while_statement
                          | if_statement
                          | switch_statement
                          | do_statement'''
    p[0] = p[1]


def p_foreach_statement(p):
    'foreach_statement : FOREACH identifier LPAREN argument_list_or_empty RPAREN statement_block'
    p[0] = ('foreach_statement', p[2], p[4], p[6])


def p_for_statement(p):
    '''for_statement : FOR LPAREN simple_statement_list_or_empty SEMICOLON expression_or_empty SEMICOLON simple_statement RPAREN statement_block'''
    p[0] = ('for_statement', p[3], p[5], p[7], p[9])


def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN statement
                       | WHILE LPAREN expression RPAREN statement_block'''
    p[0] = ('while_statement', p[3], p[5])


def p_elif_statement(p):
    '''elif_statement : ELSE IF LPAREN expression RPAREN statement
                      | ELSE IF LPAREN expression RPAREN statement_block'''
    p[0] = (p[4], p[6])


def p_elif_statements(p):
    '''elif_statements : elif_statements elif_statement'''
    p[0] = p[1] + [p[2]]


def p_elif_statements_or_empty(p):
    '''elif_statements_or_empty : elif_statements
                                | empty'''
    p[0] = p[1]


def p_else_statement(p):
    '''else_statement : ELSE statement
                      | ELSE statement_block'''
    p[0] = p[2]


def p_else_statement_or_empty(p):
    '''else_statement_or_empty : else_statement
                               | empty'''
    p[0] = p[1]


def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement       elif_statements_or_empty else_statement_or_empty
                    | IF LPAREN expression RPAREN statement_block elif_statements_or_empty else_statement_or_empty'''
    p[0] = ('if_statement', p[3], p[5], p[6], p[7])


def p_reliability(p):
    '''reliability : RELIABLE
                   | UNRELIABLE'''
    p[0] = p[1]


def p_replication_statement(p):
    'replication_statement : reliability IF LPAREN expression RPAREN identifier_list SEMICOLON'
    p[0] = p[3], p[5]


def p_replication_statements_1(p):
    'replication_statements : replication_statement'
    p[0] = [p[1]]


def p_replication_statements_2(p):
    'replication_statements : replication_statements replication_statement'
    p[0] = p[1] + [p[2]]


def p_replication_statements_or_empty(p):
    '''replication_statements_or_empty : replication_statements
                                       | empty'''
    p[0] = p[1]


def p_replication_block(p):
    '''replication_block : REPLICATION LCURLY replication_statements RCURLY'''
    p[0] = ('replication_block', p[3])


def p_statement_block(p):
    '''statement_block : LCURLY statements_or_empty RCURLY'''
    p[0] = p[2]


def p_elif_empty(p):
    '''elif_statements :
       else_statement :'''
    p[0] = []


def p_super_call(p):
    'super_call : SUPER paren_id_or_empty PERIOD call'
    p[0] = ('super_call', p[2], p[4])


def p_global_call(p):
    'global_call : GLOBAL PERIOD call'
    p[0] = ('global_call', p[3])


def p_static_call(p):
    'static_call : primary PERIOD STATIC PERIOD call'
    p[0] = ('static_call', p[1], p[5])


def p_switch_statement(p):
    'switch_statement : SWITCH LPAREN expression RPAREN LCURLY switch_cases RCURLY'
    p[0] = ('switch_statement', p[3], p[6])


def p_switch_case_1(p):
    'switch_case : CASE primary COLON statements_or_empty'
    p[0] = ('switch_case', p[2], p[4])


def p_switch_case_2(p):
    'switch_case : DEFAULT COLON statements_or_empty'
    p[0] = ('default_case', p[3])


def p_switch_cases_1(p):
    'switch_cases : switch_cases switch_case'
    p[0] = p[1] + [p[2]]


def p_switch_cases_2(p):
    'switch_cases : switch_case'
    p[0] = [p[1]]


def p_switch_cases_or_empty(p):
    '''switch_cases_or_empty : switch_cases
                             | empty'''
    p[0] = p[1]


def p_do_statement_1(p):
    'do_statement : DO statement_block'
    p[0] = ('do_statement', p[2], None)


def p_do_statement_2(p):
    'do_statement : DO statement_block UNTIL LPAREN expression RPAREN SEMICOLON'
    p[0] = ('do_statement', p[2], p[5])


def p_state_modifier(p):
    '''state_modifier : SIMULATED'''
    p[0] = p[1]


def p_state_modifiers_1(p):
    'state_modifiers : state_modifier'
    p[0] = [p[1]]


def p_state_modifiers_2(p):
    'state_modifiers : state_modifiers state_modifier'
    p[0] = p[1] + [p[2]]


def p_state_modifiers_or_empty(p):
    '''state_modifiers_or_empty : state_modifiers
                                | empty'''
    p[0] = p[1]


def p_state_definition(p):
    'state_definition : state_modifiers_or_empty STATE identifier LCURLY declarations_or_empty RCURLY'
    p[0] = ('state_definition', p[1], p[3], p[5])


precedence = (
    ('left', 'ADD', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

parser = yacc.yacc(debug=True)
