from yucc import parser
from lux import lexer
import re


class xuccparser():
    def __init__(self):
        self.ast = None
        self.generic_types = []
        self.template_parameters = []
        self.template_arguments = []
        self.classname = ''
        self.indentation = 0

    def compile(self, s, template_parameters=[]):
        self.template_parameters = template_parameters
        # TODO: set lineno?
        lexer.lineno = 1
        self.ast = parser.parse(s)
        self.classname = self.ast[1][0][1][1]
        s = render(self.ast)
        with open('okay.uc', 'w+') as f:
            # print s
            f.write(s)
        return s


xucc = xuccparser()


def r_indentation():
    global xucc
    return '  ' * xucc.indentation


def r_constructor(p):
    return 'function %s ctor(%s)\n%s' % (xucc.classname, render(p[1]), render(p[2]))


def r_string_parameterized(p):
    return p[1]


def r_function_modifiers(p):
    return ' '.join(render(q) for q in p[1])


def r_if_statement(p):
    return 'if (%s)\n{\n%s\n}' % (render(p[1]), render(p[2]))


def r_pre_unary_operation(p):
    return '{}{}'.format(render(p[1]), render(p[2]))


def r_post_unary_operation(p):
    return '{}{}'.format(render(p[1]), render(p[2]))


def r_unary_operation(p):
    return '{}{}'.format(render(p[1]), render(p[2]))


def r_string_parameterized(p):
    s = '"' + re.sub('{(.+?)}', lambda x: '" $ %s $ "' % x.groups()[0], p[1]) + '"'
    return s


def r_for_statement(p):
    return 'for ({}; {}; {})\n{{\n{}\n}}'.format(render(p[1]), render(p[2]), render(p[3]), render(p[4]))


def r_binary_operation(p):
    return ' '.join([render(p[2]), render(p[1]), render(p[3])])


def r_return_statement(p):
    if p[1] is None:
        return 'return'
    return 'return %s' % render(p[1])


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
    if p[1] is None:
        return ''
    return '\n'.join(render(q) for q in p[1])


def r_function_body(p):
    s = '\n\n'.join([render(p[1]), render(p[2])]).strip()
    return '{\n%s\n}' % s


def r_local_declaration(p):
    return 'local %s %s;' % (render(p[1]), render(p[2]))


def r_local_declarations(p):
    if p[1] is None:
        return ''
    return '\n'.join(render(q) for q in p[1])


def r_var_name(p):
    if p[2] is None:
        return render(p[1])
    else:
        return '%s[%s]' % (render(p[1]), render(p[2]))


def r_array(p):
    return 'array<{}>'.format(render(p[1]))


def r_arraycount(p):
    return 'arraycount(%s)' % render(p[1])


def r_var_name_list(p):
    return ', '.join(render(q) for q in p[1])


def r_var_declaration(p):
    return 'var %s %s;' % (render(p[1]), render(p[2]))


def r_function_declaration(p):
    return '%s(%s)' % (' '.join(filter(None, [render(q) for q in (p[1], p[4], p[3], p[2])])), render(p[5]))


def r_function_definition(p):
    if p[2] is None:
        return '{};'.format(render(p[1]))
    else:
        return '{}\n{}'.format(render(p[1]), render(p[2]))


def r_config(p):
    print p[0]
    return p[0]


def r_function_argument(p):
    return '{} {}'.format(render(p[1]), render(p[3]))


def r_function_arguments(p):
    return ', '.join(render(q) for q in p[1])


def r_declarations(p):
    if p[1] is None:
        return ''
    return '\n\n'.join(render(q) for q in p[1])


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
    # TODO: do a look-up for template parameters, in scope
    try:
        i = xucc.template_parameters.index(s)
        return render(xucc.template_arguments[i])
    except ValueError:
        return s


def r_defaultproperties(p):
    if p[1] is None:
        return ''
    return 'defaultproperties\n{\n%s\n}' % '\n'.join(render(k) for k in p[1])


def r_defaultproperties_assignment(p):
    return '%s=%s' % (render(p[1]), render(p[2]))


def r_defaultproperties_key(p):
    if p[2] is not None:
        return '%s(%s)' % (render(p[1]), p[2])
    else:
        return render(p[1])


def r_defaultproperties_object(p):
    return 'Begin Object Class=%s Name=%s\n%s\nEnd Object' % (render(p[1]), render(p[2]), '\n'.join(render(k) for k in p[3]))


def r_class_declaration(p):
    global xucc
    return 'class {} extends {}\n{};'.format(xucc.classname, render(p[2]), render(p[3]))


def r_defaultproperties_object_construction(p):
    return '(%s)' % ','.join(render(k) for k in p[1])


def r_struct_definition(p):
    return '%s;' % render(p[1])


def r_enum_values(p):
    return ',\n'.join(p[1])


def r_expression_parenthesized(p):
    return '(%s)' % render(p[1])


def r_enum_definition(p):
    return '%s;' % render(p[1])


def r_enum_declaration(p):
    return 'enum %s\n{\n%s\n}' % (p[1], render(p[2]))


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


def r_default(p):
    return 'default.%s' % render(p[1])


def r_default_case(p):
    return 'default:'


def r_super_call(p):
    if p[1] is None:
        return 'super.%s' % render(p[2])
    else:
        return 'super(%s).%s' % (render(p[1]), render(p[2]))


def r_reference(p):
    return render(p[1])


def r_foreach_statement(p):
    return 'foreach %s(%s)\n{\n%s\n}' % (render(p[1]), render(p[2]), render(p[3]))


def r_vect(p):
    return 'vect(%s, %s, %s)' % tuple(map(render, p[1:4]))


def r_codeline(p):
    return '%s;' % render(p[1])


def r_start(p):
    return '\n\n'.join(render(q) for q in p[1])


def r_break_statement(p):
    return 'break'


def r_continue_statement(p):
    return 'continue'


def r_switch_statement(p):
    return 'switch (%s)\n{\n%s\n}' % (render(p[1]), '\n'.join(render(q) for q in p[2]))


def r_switch_case(p):
    return 'case %s:\n%s' % (render(p[1]), render(p[2]))


def r_do_statement(p):
    s = 'do\n{\n%s\n}' % render(p[1])
    if p[2] is not None:
        s = ' '.join([s, 'until (%s);' % render(p[2])])
    return s


def r_static_call(p):
    return '%s.static.%s' % (render(p[1]), render(p[2]))


def r_state_definition(p):
    return 'state %s\n{\n%s\n}' % (render(p[2]), render(p[3]))


def r_while_statement(p):
    return 'while (%s)\n{\n%s\n}' % (render(p[1]), render(p[2]))


def r_global_call(p):
    return 'global.%s' % render(p[1])


def r_allocation(p):
    return 'new %s' % render(p[1])


def r_construction(p):
    return '(new %s).ctor(%s)' % (render(p[1]), render(p[2]))


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
            u = eval('r_{}'.format(q[0]))
            s += u(q)
    elif type(p) is tuple:
        u = eval('r_{}'.format(p[0]))
        s += u(p)
    return s
