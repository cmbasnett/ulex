from yucc import generic_types, asts
from pprint import pprint

def u_array(p):
    return 'array<{}>'.format(unpack(p[0]))

def u_var_declaration(p):
    d = p[1]
    print 'd'
    print d
    return 'var {} {} {};'.format(unpack(q) for q in d)

def u_function_declaration(p):
    print p
    return str(p)

def u_declarations(p):
    print unpack(p[1])
    #return '\n\n'.join(q for q in unpack())
    return ''

def u_identifier_list(p):
    return '\n    '.join(unpack(q) for q in p[1])

def u_template(p):
    return 'template({})'.format(unpack(p[1]))

def u_type(p):
    #TODO: do check for tuple and arglist
    return unpack(p[1])

def u_class_modifiers(p):
    return '\n'.join(unpack(q) for q in p[1])

def u_identifier(p):
    return unpack(p[1])

def u_class_declaration(p):
    #print p[0]
    s = 'class {} extends {}\n{};'.format(unpack(p[1][0]), unpack(p[1][1]), unpack(p[1][2]))
    s += ', '.join('')
    return s

def u_start(p):
    return unpack(p[1])

def unpack(p):
    #print 'unpacking....{}'.format(p)
    s = ''
    if type(p) is str:
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
    identifier, arguments = generic_type
    classname = identifier[1]
    if classname not in asts.keys():
        raise Exception
    #pprint(asts[classname])
    print unpack(asts[classname])
