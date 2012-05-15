import os.path

from lxml import etree

from eats.exceptions import EATSMLException


PATH = os.path.abspath(os.path.dirname(__file__))
PRUNE_FILENAME = 'prune-eatsml.xsl'
PRUNE_XSLT = os.path.join(PATH, PRUNE_FILENAME)
RNG_FILENAME = 'eatsml.rng'
RNG_PATH = os.path.join(PATH, RNG_FILENAME)


class EATSMLHandler (object):

    def __init__ (self, topic_map):
        self._topic_map = topic_map
        relaxng_doc = etree.parse(RNG_PATH)
        self._relaxng = etree.RelaxNG(relaxng_doc)
        prune_doc = etree.parse(PRUNE_XSLT)
        self._prune_eatsml = etree.XSLT(prune_doc)
    
    def _validate (self, tree):
        """Validates XML `tree` against the EATSML RelaxNG schema.

        :param tree: XML tree of EATSML document
        :type tree: `ElementTree`

        """
        if not self._relaxng.validate(tree):
            message = 'RelaxNG validation of the EATSML document failed: %s' \
                % (self._relaxng.error_log.last_error)
            raise EATSMLException(message)
            
    
