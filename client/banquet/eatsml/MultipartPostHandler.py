#!/usr/bin/python

####
# 02/2006 Will Holcomb <wholcomb@gmail.com>
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
####
#
# Modified by Jamie Norrish:
#
#  * removed unwanted print statement
#  * added support for StringIO instances of XML data
#  * replaced string concatenation with joining a list of strings
#  * modified coding style
#
"""

Usage:
  Enables the use of multipart/form-data for posting forms

Inspirations:
  Upload files in python:
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
  urllib2_file:
    Fabien Seisen: <fabien@seisen.org>

Example:
  import MultipartPostHandler, urllib2, cookielib, StringIO

  cookies = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
                                MultipartPostHandler.MultipartPostHandler)
  params = { "username" : "bob", "password" : "riviera",
             "file" : StringIO.StringIO('<xml/>')}
  opener.open("http://wwww.bobsite.com/upload/", params)

"""

import StringIO
import urllib
import urllib2
import mimetools, mimetypes
import os.path
import sys

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

# Controls how sequences are uncoded. If true, elements may be given
# multiple values by assigning a sequence.
doseq = 1

class MultipartPostHandler (urllib2.BaseHandler):

    # This handler needs to run first.
    handler_order = urllib2.HTTPHandler.handler_order - 10

    def http_request (self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for (key, value) in data.items():
                     if type(value) == file or isinstance(value, StringIO.StringIO):
                         v_files.append((key, value))
                     else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, 'not a valid non-string sequence or mapping object', traceback
            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary
                request.add_unredirected_header('Content-Type', contenttype)
            request.add_data(data)
        return request

    def multipart_encode (vars, files, boundary=None, buffer=None):
        if boundary is None:
            boundary = mimetools.choose_boundary()
        if buffer is None:
            buffer = ''
        buffer_parts = [buffer]
        for (key, value) in vars:
            buffer_parts.append('--%s\r\n' % boundary)
            buffer_parts.append('Content-Disposition: form-data; name="%s"' % key)
            buffer_parts.append('\r\n\r\n%s\r\n' % value)
        for (key, fd) in files:
            if isinstance(fd, StringIO.StringIO):
                filename = 'import_file.xml'
            else:
                filename = os.path.basename(fd.name)
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buffer_parts.append('--%s\r\n' % boundary)
            buffer_parts.append('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename))
            buffer_parts.append('Content-Type: %s\r\n' % contenttype)
            fd.seek(0)
            buffer_parts.append('\r\n' + fd.read() + '\r\n')
        buffer_parts.append('--%s--\r\n\r\n' % boundary)
        return boundary, ''.join(buffer_parts)
    multipart_encode = Callable(multipart_encode)

    https_request = http_request
