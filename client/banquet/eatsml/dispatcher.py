"""Module for talking to an EATS server."""

__docformat__ = 'restructuredtext'

import cookielib
from copy import deepcopy
from os.path import abspath, dirname, join
from StringIO import StringIO
import sys
import urllib
import urllib2
import urlparse

from lxml import etree

from MultipartPostHandler import MultipartPostHandler
import parser


# Full path to this directory.
PATH = abspath(dirname(__file__))


# See http://bugs.python.org/issue9639 for the bug this is working
# around.
if sys.version_info[:2] == (2, 6) and sys.version_info[2] >= 6:
    def fixed_http_error_401(self, req, fp, code, msg, headers):
        url = req.get_full_url()
        response = self.http_error_auth_reqed('www-authenticate', url, req,
                                              headers)
        self.retried = 0
        return response

    urllib2.HTTPBasicAuthHandler.http_error_401 = fixed_http_error_401


class Dispatcher (object):

    __urls = {
        'base_document': 'export/eatsml/base/',
        'edit_entity': 'entity/%s/edit/',
        'import': 'edit/import/',
        'lookup_name': 'search/eatsml/?%s'}
    
    def __init__ (self, base_url, username, password, http_username=None,
                  http_password=None):
        self.__base_url = base_url
        self.__username = username
        self.__password = password
        self.__base_doc = None
        self.__csrf_token = None
        self.cj = cookielib.CookieJar()
        handlers = [urllib2.HTTPCookieProcessor(self.cj),
                    MultipartPostHandler]
        if http_username is not None:
            password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
            # Since the base URL may not encompass the login URL
            # (since the base URL is for the EATS application, and not
            # the Django installation as a whole), just use the domain
            # name as the authentication super URL.
            url_pieces = urlparse.urlparse(self.base_url)
            url = urlparse.urlunparse(url_pieces[0:2] + ('', '', '', ''))
            password_manager.add_password(None, url, http_username,
                                          http_password)
            basic_auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
            handlers.append(basic_auth_handler)
        opener = urllib2.build_opener(*handlers)
        urllib2.install_opener(opener)
        self.__prune_infrastructure_transform = self.__create_XSLT_transformer(
            'remove-redundant-eatsml-infrastructure-data.xsl')
        self.__prune_system_parts_transform = self.__create_XSLT_transformer(
            'remove-redundant-eatsml-system-name-parts.xsl')

    @property
    def base_url (self):
        """Return the base URL for the EATS server."""
        return self.__base_url

    @property
    def username (self):
        """Return the username."""
        return self.__username

    @property
    def password (self):
        """Return the password."""
        return self.__password

    def __create_XSLT_transformer (self, xslt_filename):
        """Return an XSLT transformer from the XSLT in
        `xslt_filename`.

        Arguments:

        - `xslt_filename`: string filename of XSLT

        """
        xslt_doc = etree.parse(join(PATH, xslt_filename))
        return etree.XSLT(xslt_doc)
    
    def login (self):
        """Log in to the EATS server.

        Raise an exception if authentication is not successful.

        """
        # Try first to get the base document, which should only be
        # available once logged in. If not logged in, it will redirect
        # to the login page.
        url = urlparse.urljoin(self.base_url, self.__urls['base_document'])
        handle = urllib2.urlopen(url)
        login_url = handle.geturl()
        xml_tree = etree.parse(handle, parser.parser)
        login = xml_tree.getroot()
        try:
            self.__csrf_token = login.xpath('//*[@name = "csrfmiddlewaretoken"][1]/@value')[0]
        except IndexError:
            # No csrfmiddlewaretoken input found, which may simply be
            # because the server is pre-Django 1.2. Whatever the
            # reason, do not fail here.
            self.__csrf_token = ''
        data = {'username': self.username, 'password': self.password,
                'csrfmiddlewaretoken': self.__csrf_token}
        encoded_data = urllib.urlencode(data)
        handle = urllib2.urlopen(login_url, encoded_data)
        if handle.geturl() == login_url:
            # A successful login redirects to a different page.
            raise Exception('Failed to authenticate to EATS server')
    
    def get_base_document (self):
        """Return an `eatsml.Document` instance containing only the
        infrastructural elements."""
        url = urlparse.urljoin(self.base_url, self.__urls['base_document'])
        self.__base_doc = self.__get_xml_from_server(url)
        return self.__base_doc

    def get_base_document_copy (self):
        """Return a deep copy of the base document."""
        return deepcopy(self.__base_doc)

    def __prune_eatsml (self, document):
        """Return `doc` with all redundant elements removed.

        Arguments:

        - `document`: EATSML document

        """
        tree = etree.ElementTree(document)
        result_tree = self.__prune_infrastructure_transform(tree)
        result_tree = self.__prune_system_parts_transform(result_tree)
        return result_tree.getroot()

    def import_document (self, document, import_message):
        """Import `document` into EATS. Return the URL of the
        resulting page.

        Arguments:

        - `document`: EATSML document
        - `import_message`: string description of import

        """
        document = self.__prune_eatsml(document)
        fh = StringIO(etree.tostring(document, encoding='utf-8',
                                     pretty_print=True))
        params = {'description': import_message,
                  'import_file': fh,
                  'csrfmiddlewaretoken': self.__csrf_token}
        url = urlparse.urljoin(self.base_url, self.__urls['import'])
        handle = urllib2.urlopen(url, params)
        return handle.geturl()

    def get_processed_import (self, base_url):
        """Return a `CollectionElementClass` instance of processed for
        of the import at `base_url`.

        Arguments:

        - `base_url`: string URL of the import

        """
        url = urlparse.urljoin(base_url, 'processed/')
        return self.__get_xml_from_server(url)

    def look_up_name (self, name):
        """Return a `CollectionElementClass` instance of the results of
        looking up `name` on the EATS server.

        Arguments:
        
        - `name`: a unicode string to look up

        """
        parameters = {'name': name.encode('utf-8')}
        encoded_parameters = urllib.urlencode(parameters)
        url = urlparse.urljoin(self.base_url, self.__urls['lookup_name'] %
                               encoded_parameters)
        return self.__get_xml_from_server(url)

    def look_up_record (self, record_id, authority_id):
        """Return a `CollectionElementClass` instance of the results
        of looking up `record_id` and `authority_id` on the EATS server.

        Arguments:

        - `record_id`: unicode string record ID to look up
        - `authority_id`: string authority ID for `key`

        """
        parameters = {'record_id': record_id.encode('utf-8'),
                      'authority': authority_id}
        encoded_parameters = urllib.urlencode(parameters)
        url = urlparse.urljoin(self.base_url, self.__urls['lookup_name'] %
                               encoded_parameters)
        return self.__get_xml_from_server(url)                      

    def get_edit_url (self, entity):
        """Return the full URL for the edit page for entity.

        Arguments:

        - `entity`: `etree.Element` of the EATSML entity

        """
        url = urlparse.urljoin(self.base_url, self.__urls['edit_entity'] %
                               entity.eats_id)
        return url

    def __get_xml_from_server (self, url):
        """Return an `lxml.Element` instance from the results of
        requesting `url` from the EATS server.

        In the case of EATSML being returned from the server, the
        element returned is a `parser.CollectionElementClass`
        instance.
        
        Arguments:

        - `url`: string URL

        """
        handle = urllib2.urlopen(url)
        xml_tree = etree.parse(handle, parser.parser)
        return xml_tree.getroot()
