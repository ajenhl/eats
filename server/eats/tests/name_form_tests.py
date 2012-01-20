# -*- coding: utf-8 -*-

from django.test import TestCase

from eats.lib.name_form import abbreviate_name, asciify_name, create_name_forms, demacronise_name, substitute_ascii, unpunctuate_name


class NameFormTestCase (TestCase):

    def test_abbreviate_name (self):
        data = (
            ('en', u'Smith and Smith', u'Smith & Smith'),
            )
        for language_code, original, expected in data:
            actual = abbreviate_name(original, language_code)
            self.assertEqual(actual, expected)
    
    def test_asciify_name (self):
        """Tests that a name is properly converted to ASCII."""
        data = (
            ('Alan Smith', u'Alan Smith'),
            (u'François', u'Francois'),
            (u'Ægypt', u'AEgypt'),
            (u'Encyclopædia Brittanica', u'Encyclopaedia Brittanica'),
            (u'Œdipus', u'OEdipus'),
            (u'Schloß', u'Schloss'),
            (u'Hawaiʻi', u"Hawai'i"),
            (u'Paradiſe Loſt', u'Paradise Lost'),
            (u'Māori', u'Maori'),
            (u'War’s End', u"War's End"),
            )
        for original, expected in data:
            actual = asciify_name(original)
            self.assertEqual(actual, expected)

    def test_create_forms (self):
        data = (
            (u'Māori', 'mi', 'Latn', set((u'Maori', u'Maaori', u'Māori'))),
            (u'François', 'fr', 'Latn', set((u'François', u'Francois'))),
            (u'A. Smith', None, None, set((u'A. Smith', u'A Smith'))),
            )
        for original, language_code, script_code, expected in data:
            actual = create_name_forms(original, language_code, script_code)
            self.assertEqual(actual, expected)

    def test_demacronis_name (self):
        data = (
            (u'Māori', u'Maaori'),
            )
        for original, expected in data:
            actual = demacronise_name(original)
            self.assertEqual(actual, expected)

    def test_substitute_ascii (self):
        data = (
            (u'Alan Smith', u'Alan Smith'),
            (u'Ægypt', u'AEgypt'),
            (u'Encyclopædia Brittanica', u'Encyclopaedia Brittanica'),
            (u'Œdipus', u'OEdipus'),
            (u'Schloß', u'Schloss'),
            (u'Hawaiʻi', u"Hawai'i"),
            (u'Paradiſe Loſt', u'Paradise Lost'),
            )
        for original, expected in data:
            actual = substitute_ascii(original)
            self.assertEqual(actual, expected)

    def test_unpunctuate_name (self):
        data = (
            (u'Alan Smith', u'Alan Smith'),
            (u'A. Smith', u'A Smith'),
            (u'Smith, Alan', u'Smith Alan'),
            (u'Middle-earth', u'Middleearth'),
            (u"War's End", u'Wars End'),
            (u'War’s End', u'Wars End'),
            (u'Never say never (again)', u'Never say never again'),
            )
        for original, expected in data:
            actual = unpunctuate_name(original)
            self.assertEqual(actual, expected)
