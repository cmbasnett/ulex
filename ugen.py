from yucc import parser
import pprint


class xuccparser():
    def __init__(self):
        self.ast = None
        self.generic_types = []
        self.template_parameters = []
        self.template_arguments = []
        self.classname = ''

    def compile(self, s, template_parameters=[]):
        self.template_parameters = template_parameters

        self.ast = parser.parse(s)

        # determine classname from AST

        #pprint.pprint(self.ast)
        print render(self.ast)

xucc = xuccparser()

        # for generic_type in self.generic_types:
        #     template_parameters = []
        #     garbage, identifier, template_arguments = generic_type
        #     template_arguments = [render(q) for q in template_arguments]
        #     #print template_arguments
        #     classname = identifier[1]

        #     if len(template_arguments) > 0:
        #         classname = '_'.join([classname, '_'.join(template_arguments)])

        #     if identifier[1] not in asts.keys():
        #         raise Exception('Class \'{}\' cannot be found.'.format(identifier[1]))
        #     contents = render(asts[identifier[1]])

        #     print contents


def r_string_parameterized(p):
    return p[1]


def r_function_modifiers(p):
    return ' '.join(render(q) for q in p[1])


def r_if_statement(p):
    return 'if ({})\n{{\n{}\n}}'.format(render(p[1]), render(p[2]), render(p[3]))


def r_pre_unary_operation(p):
    return '{}{}'.format(render(p[1]), render(p[2]))


def r_post_unary_operation(p):
    return '{}{}'.format(render(p[1]), render(p[2]))


def r_unary_operation(p):
    return '{}{}'.format(render(p[1]), render(p[2]))


def r_for_statement(p):
    return 'for ({}; {}; {})\n{{\n{}\n}}'.format(render(p[1]), render(p[2]), render(p[3]), render(p[4]))


def r_binary_operation(p):
    return '{} {} {}'.format(render(p[2]), render(p[1]), render(p[3]))


def r_return_statement(p):
    return 'return {};'.format(render(p[1]))


def r_number(p):
    return str(p[1])


def r_argument_list(p):
    return ', '.join(render(q) for q in p[1])


def r_call(p):
    return '{}({})'.format(render(p[1]), render(p[2]))


def r_attribute(p):
    return '{}.{}'.format(render(p[1]), render(p[2]))


def r_assignment_statement(p):
    return '{} = {}'.format(render(p[1]), render(p[2]))


def r_subscription(p):
    return '{}[{}]'.format(render(p[1]), render(p[2]))


def r_statements(p):
    return '\n'.join(render(q) for q in p[1])


def r_function_body(p):
    return '{{\n{0}{1}\n}}'.format(render(p[1]), render(p[2]))


def r_local_declaration(p):
    return 'local {type} {identifier};'.format(type=render(p[1]), identifier=render(p[2]))


def r_local_declarations(p):
    return '\n'.join(render(q) for q in p[1:])


def r_var_name(p):
    if p[2] is None:
        return render(p[1])
    else:
        return '%s[%s]' % (render(p[1]), render(p[2]))


def r_array(p):
    return 'array<{}>'.format(render(p[1]))


def r_var_names(p):
    return ', '.join(p[1])


def r_var_declaration(p):
    return 'var %s %s;' % (render(p[1]), render(p[2]))


def r_function_declaration(p):
    return '{} {} {} {}({})'.format(render(p[1]), render(p[4]), render(p[3]), render(p[2]), render(p[5]))


def r_function_definition(p):
    if p[2] is None:
        return '{};'.format(render(p[1]))
    else:
        return '{}\n{}'.format(render(p[1]), render(p[2]))


#TODO: modifiers
def r_function_argument(p):
    return '{} {}'.format(render(p[1]), render(p[3]))


def r_function_arguments(p):
    return ', '.join(render(q) for q in p[1])


def r_declarations(p):
    return '\n'.join(render(q) for q in p[1])


def r_identifier_list(p):
    return ', '.join(render(q) for q in p[1])


def r_template(p):
    global template_parameters
    template_parameters = [render(q) for q in p[1][1]]
    return ''


def r_generic_type(p):
    return '{}_{}'.format(render(p[1]), '_'.join(render(q) for q in p[2]))


def r_type(p):
    return render(p[1])


def r_class_modifiers(p):
    return '\n'.join(render(q) for q in p[1] if q)


def r_identifier(p):
    global xucc
    s = render(p[1])
    #TODO: do a look-up for template parameters, in scope
    try:
        i = xucc.template_parameters.index(s)
        return render(xucc.template_arguments[i])
    except ValueError:
        return s


def r_class_declaration(p):
    global xucc
    s = 'class {} extends {}\n{};'.format(xucc.classname, render(p[2]), render(p[3]))
    return s


def r_const_declaration(p):
    return 'const %s = %s;' % (render(p[1]), render(p[2]))


def r_class_type(p):
    return 'class<%s>' % render(p[1])


def r_struct_declaration(p):
    name, var_declarations = p[1], p[2]
    s = 'struct %s\n{\n%s\n}' % (render(name), render(var_declarations))
    return s


def r_struct_var_declarations(p):
    return '\n'.join(render(x) for x in p[1])


def r_struct_var_declaration(p):
    return 'var %s %s;' % (render(p[1]), render(p[2]))


def r_start(p):
    return '\n\n'.join(render(q) for q in p[1])


def r_default(p):
    return 'default.%s' % render(p[1])


def render(p):
    s = ''
    if p is None:
        return ''
    elif type(p) is int:
        return str(p)
    elif type(p) is str:
        return p
    elif type(p) is list:
        for q in p:
            #pprint(q)
            u = eval('r_{}'.format(q[0]))
            s += u(q)
    elif type(p) is tuple:
        u = eval('r_{}'.format(p[0]))
        s += u(p)
    return s
