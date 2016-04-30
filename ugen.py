from yucc import generic_types, asts
from pprint import pprint

#TODO: pre-increment vs post-increment

classname = ''
template_parameters = []
template_arguments = []

def u_string_parameterized(p):
    return p[1]

def u_function_modifiers(p):
    return ' '.join(q for q in p[1])

def u_if_statement(p):
    return 'if ({})\n{{\n{}\n}}'.format(unpack(p[1]), unpack(p[2]), unpack(p[3]))

def u_pre_unary_operation(p):
    return '{}{}'.format(unpack(p[1]), unpack(p[2]))

def u_post_unary_operation(p):
    return '{}{}'.format(unpack(p[1]), unpack(p[2]))

def u_unary_operation(p):
    return '{}{}'.format(unpack(p[1]), unpack(p[2]))

def u_for_statement(p):
    return 'for ({}; {}; {})\n{{\n{}\n}}'.format(unpack(p[1]), unpack(p[2]), unpack(p[3]), unpack(p[4]))

def u_binary_operation(p):
    return '{} {} {}'.format(unpack(p[2]), unpack(p[1]), unpack(p[3]))

def u_return_statement(p):
    return 'return {};'.format(unpack(p[1]))

def u_number(p):
    return str(p[1])

def u_argument_list(p):
    return ', '.join(unpack(q) for q in p[1])

def u_call(p):
    return '{}({})'.format(unpack(p[1]), unpack(p[2]))

def u_attribute(p):
    return '{}.{}'.format(unpack(p[1]), unpack(p[2]))

def u_assignment_statement(p):
    return '{} = {}'.format(unpack(p[1]), unpack(p[2]))

def u_subscription(p):
    return '{}[{}]'.format(unpack(p[1]), unpack(p[2]))

def u_statements(p):
    return '\n'.join(unpack(q) for q in p[1])

def u_function_body(p):
    return '{{\n{0}\n{1}\n}}'.format(unpack(p[1]), unpack(p[2]))

def u_local_declaration(p):
    return 'local {} {};'.format(unpack(p[1]), unpack(p[2]))

def u_local_declarations(p):
    return '\n'.join(unpack(q) for q in p[1:])

def u_var_name(p):
    if p[2] is None:
        return unpack(p[1])
    else:
        return '{}[{}]'.format(unpack(p[1]), unpack(p[2]))

def u_array(p):
    return 'array<{}>'.format(unpack(p[1]))

def u_var_names(p):
    return ', '.join(p[1])

def u_var_declaration(p):
    return 'var {} {};'.format(unpack(p[1]), unpack(p[2]))

def u_function_declaration(p):
    return '{} {} {} {}({})'.format(unpack(p[1]), unpack(p[4]), unpack(p[3]), unpack(p[2]), unpack(p[5]))

def u_function_definition(p):
    if p[2] is None:
        return '{};'.format(unpack(p[1]))
    else:
        return '{}\n{}'.format(unpack(p[1]), unpack(p[2]))

#TODO: modifiers
def u_function_argument(p):
    return '{} {}'.format(unpack(p[1]), unpack(p[3]))

def u_function_arguments(p):
    return ', '.join(unpack(q) for q in p[1])

def u_declarations(p):
    return '\n\n'.join(unpack(q) for q in p[1])

def u_identifier_list(p):
    return ', '.join(unpack(q) for q in p[1])

def u_template(p):
    global template_parameters
    template_parameters = [unpack(q) for q in p[1][1]]
    return ''

def u_generic_type(p):
    return '{}_{}'.format(unpack(p[1]), '_'.join(unpack(q) for q in p[2]))

def u_type(p):
    return unpack(p[1])

def u_class_modifiers(p):
    return '\n'.join(unpack(q) for q in p[1])

def u_identifier(p):
    global template_arguments
    s = unpack(p[1])
    #TODO: do a look-up for template parameters, in scope
    try:
        i = template_parameters.index(s)
        return unpack(template_arguments[i])
    except ValueError:
        return s

def u_class_declaration(p):
    global classname
    s = 'class {} extends {}\n{};'.format(classname, unpack(p[2]), unpack(p[3]))
    return s

def u_start(p):
    return '\n\n'.join(unpack(q) for q in p[1])

def unpack(p):
    s = ''
    if p is None:
        return ''
    elif type(p) is str:
        return p
    elif type(p) is list:
        for q in p:
            #pprint(q)
            u = eval('u_{}'.format(q[0]))
            s += u(q)
    elif type(p) is tuple:
        u = eval('u_{}'.format(p[0]))
        s += u(p)
    return s

# foreach unique generic type encountered
for generic_type in generic_types:
    template_parameters = []
    garbage, identifier, template_arguments = generic_type
    template_arguments = [unpack(q) for q in template_arguments]
    #print template_arguments
    classname = identifier[1]

    if len(template_arguments) > 0:
        classname = '_'.join([classname, '_'.join(template_arguments)])

    if identifier[1] not in asts.keys():
        raise Exception
    contents = unpack(asts[identifier[1]])

    print contents
