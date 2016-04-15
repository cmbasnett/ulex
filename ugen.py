from yucc import generic_types, asts

def g_class_modifier(p):

def g_class_declaration(p):
    s = 'class {} extends {} {};'.format(p[0], p[1])
    s += ','.join(eval('g_{}'.format(p[2])))

def gen(ast):
    for p in ast:
        g = eval('g_{}'.format(p[0]))
        g(p[1])

# foreach unique generic type encountered
for generic_type in generic_types:
    classname, arguments = generic_type
    if classname not in asts.keys():
        raise Exception
    gen(asts[classname])
