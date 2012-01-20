# -*- coding: utf-8 -*-

import re
import unicodedata


ABBREVIATIONS = {'en': ((' and ', ' & '),)}
ASCII_SUBSTITUTIONS = ((u'Æ', u'AE'), (u'æ', u'ae'), (u'Œ', u'OE'),
                       (u'œ', u'oe'), (u'ß', u'ss'), (u'ſ', u's'),
                       (u'ʻ', "'"), (u'“', u'"'), (u'”', u'"'), (u'‘', u"'"),
                       (u'’', u"'"),)
MACRON_PATTERN = re.compile(u'([aeiou])\N{COMBINING MACRON}', re.UNICODE)


def abbreviate_name (name, language_code):
    """Returns `name` with full elements abbreviated.

    :param name: name to be converted
    :type name: Unicode string
    :param language_code: ISO language code for `name`
    :type language_code: `str`
    :rtype: Unicode string

    """
    for full, abbreviated in ABBREVIATIONS.get(language_code, ()):
        name = name.replace(full, abbreviated)
    return name

def asciify_name (name):
    """Returns `name` converted to ASCII.

    :param name: name to be converted
    :type name: Unicode string
    :rtype: Unicode string

    """
    substituted_form = substitute_ascii(name)
    ascii_form = unicode(substituted_form.encode('ascii', 'ignore'))
    return ascii_form

def create_name_forms (name, language_code=None, script_code=None):
    name_forms = set()
    normalised_name = unicodedata.normalize('NFD', name)
    name_forms.add(normalised_name)
    # script_code will be None for a search query.
    if script_code == 'Latn' or script_code is None:
        asciified_forms = set(map(asciify_name, name_forms))
        name_forms = name_forms | asciified_forms
    demacronised_forms = set(map(demacronise_name, name_forms))
    name_forms = name_forms | demacronised_forms
    # language_code will be None for a search query.
    if language_code is not None:
        abbreviated_forms = set()
        for name in name_forms:
            abbreviated_forms.add(abbreviate_name(name, language_code))
        name_forms = name_forms | abbreviated_forms
    unpunctuated_forms = set(map(unpunctuate_name, name_forms))
    name_forms = name_forms | unpunctuated_forms
    return name_forms

def demacronise_name (name):
    """Returns `name` with macronised vowels schanged into double vowels."""
    demacronised_form = MACRON_PATTERN.sub(r'\1\1', name)
    return demacronised_form

def substitute_ascii (name):
    """Returns `name` with various non-ASCII characters replaced with ASCII
    equivalents.

    :param name: name to be converted
    :type name: Unicode string
    :rtype: Unicode string

    """
    for original, substitute in ASCII_SUBSTITUTIONS:
        name = name.replace(original, substitute)
    return name

def unpunctuate_name (name):
    """Returns `name` with punctuation removed.

    :param name: name to be converted
    :type name: Unicode string
    :rtype: Unicode string

    """
    # QAZ: This does not work well in some cases, such as "On Self
    # Misery.—An Epigram", where "An" ends up joined to "Misery".
    char_array = []
    for character in name:
        category = unicodedata.category(character)
        # Punctuation categories start with 'P'.
        if category[0] != 'P':
            char_array.append(character)
    return u''.join(char_array)
