EATSML_NAMESPACE = 'http://hdl.handle.net/10063/234'
EATSML = '{%s}' % EATSML_NAMESPACE
XML_NAMESPACE = 'http://www.w3.org/XML/1998/namespace'
XML = '{%s}' % (XML_NAMESPACE)
NSMAP = {None: EATSML}
XPATH_NSMAP = {'e': EATSML_NAMESPACE,
               'xml': XML_NAMESPACE}
