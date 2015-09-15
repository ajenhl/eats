from django.test import TestCase

from eats.lib.name_form import abbreviate_name, asciify_name, create_name_forms, demacronise_name, substitute_ascii, unpunctuate_name


class NameFormTestCase (TestCase):

    def test_abbreviate_name (self):
        data = (
            ('en', 'Smith and Smith', 'Smith & Smith'),
            )
        for language_code, original, expected in data:
            actual = abbreviate_name(original, language_code)
            self.assertEqual(actual, expected)

    def test_asciify_name (self):
        """Tests that a name is properly converted to ASCII."""
        data = (
            ('Alan Smith', 'Alan Smith'),
            ('François', 'Francois'),
            ('Ægypt', 'AEgypt'),
            ('Encyclopædia Brittanica', 'Encyclopaedia Brittanica'),
            ('Œdipus', 'OEdipus'),
            ('Schloß', 'Schloss'),
            ('Hawaiʻi', "Hawai'i"),
            ('Paradiſe Loſt', 'Paradise Lost'),
            ('Māori', 'Maori'),
            ('War’s End', "War's End"),
            )
        for original, expected in data:
            actual = asciify_name(original)
            self.assertEqual(actual, expected)

    def test_create_forms (self):
        data = (
            ('Māori', 'mi', 'Latn', set(('Maori', 'Maaori', 'Māori'))),
            ('François', 'fr', 'Latn', set(('François', 'Francois'))),
            ('A. Smith', None, None, set(('A. Smith', 'A Smith'))),
            )
        for original, language_code, script_code, expected in data:
            actual = create_name_forms(original, language_code, script_code)
            self.assertEqual(actual, expected)

    def test_demacronis_name (self):
        data = (
            ('Māori', 'Maaori'),
            )
        for original, expected in data:
            actual = demacronise_name(original)
            self.assertEqual(actual, expected)

    def test_substitute_ascii (self):
        data = (
            ('Alan Smith', 'Alan Smith'),
            ('Ægypt', 'AEgypt'),
            ('Encyclopædia Brittanica', 'Encyclopaedia Brittanica'),
            ('Œdipus', 'OEdipus'),
            ('Schloß', 'Schloss'),
            ('Hawaiʻi', "Hawai'i"),
            ('Paradiſe Loſt', 'Paradise Lost'),
            )
        for original, expected in data:
            actual = substitute_ascii(original)
            self.assertEqual(actual, expected)

    def test_unpunctuate_name (self):
        data = (
            ('Alan Smith', 'Alan Smith'),
            ('A. Smith', 'A Smith'),
            ('Smith, Alan', 'Smith Alan'),
            ('Middle-earth', 'Middleearth'),
            ("War's End", 'Wars End'),
            ('War’s End', 'Wars End'),
            ('Never say never (again)', 'Never say never again'),
            )
        for original, expected in data:
            actual = unpunctuate_name(original)
            self.assertEqual(actual, expected)
