# python field encapsulator

import os

# ================================================
# init variables or not
INIT_VARS = True
# generate getters only
GET_ONLY = False
# setter prefix
SET_PREFIX = 'new_'
# getters and setters to CamelCase
SET_CAMEL = False
# ================================================
# indentation
IDNT = '    '
# field prefix
PREFIX = '__'
# ================================================


# delete non-ascii letters
def cleanup(inp_str):
    clear_str = []
    for letter in inp_str[0:-1]:
        if ord(letter) < 127:
            clear_str.append(letter)
    return ''.join(clear_str)


# variable name to camelCase
def camel(inp_str):
    letters = inp_str.split('_')
    for i in range(1, len(letters)):
        letters[i] = letters[i].capitalize()
    return ''.join(letters)


def proc_file(filename):
    with open(filename) as inp_file:
        fields_raw = inp_file.readlines()

    variables = []
    for field in fields_raw:
        if len(field) > 1:
            var = cleanup(field)
            variables.append(var)

    return encap(variables)


def encap(variables):
    idnt2 = IDNT + IDNT

    decl = []
    init = []
    gs = []

    for var in variables:
        field = PREFIX + var
        decl.append('%s%s = None' % (IDNT, field))

        if INIT_VARS:
            init.append('%sself.%s = None' % (idnt2, field))

        if SET_CAMEL:
            proper = camel(var)
        else:
            proper = var

        gs.append('%s@property' % IDNT)
        gs.append('%sdef %s(self):' % (IDNT, proper))
        gs.append('%sreturn self.%s' % (idnt2, field))
        gs.append('')

        if not GET_ONLY:
            gs.append('%s@%s.setter' % (IDNT, proper))
            gs.append('%sdef %s(self, %s%s):' % (IDNT, proper, SET_PREFIX, var))
            gs.append('%sself.%s = %s%s' % (idnt2, field, SET_PREFIX, var))
            gs.append('')

    outp = []

    outp.append('class ClassName(object):')
    outp.extend(decl)
    outp.append('')
    if INIT_VARS:
        outp.append(IDNT + 'def __init(self):')
        outp.extend(init)
        outp.append('')

    outp.extend(gs)

    return os.linesep.join(outp)
    # return outp
