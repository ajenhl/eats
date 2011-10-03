EATSML_NAMESPACE = 'http://eats.artefact.org.nz/ns/eatsml/'
EATSML = '{%s}' % EATSML_NAMESPACE
XML_NAMESPACE = 'http://www.w3.org/XML/1998/namespace'
XML = '{%s}' % (XML_NAMESPACE)
NSMAP = {None: EATSML}
XPATH_NSMAP = {'e': EATSML_NAMESPACE,
               'xml': XML_NAMESPACE}
