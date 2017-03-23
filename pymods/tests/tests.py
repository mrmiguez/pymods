import os
import unittest

from pymods.Record import Record
from pymods.Reader import MODSReader

test_dir_path = os.path.abspath(os.path.dirname(__file__))


class AbstractTests(unittest.TestCase):

    def setUp(self):
        self.record = Record(os.path.join(test_dir_path, 'abstract_xml.xml'))
        self.no_abstract = Record(os.path.join(test_dir_path, 'genre_xml.xml'))

    def test_mods_abstract_text(self):
        expected_text = 'Remain calm! This is only a test!'
        self.assertEqual(expected_text, self.record.abstract[0].text)

    def test_mods_abstract_type(self):
        self.assertIsNone(self.record.abstract[0].type)

    def test_mods_abstract_displayLabel(self):
        self.assertIsNone(self.record.abstract[0].displayLabel)

    def test_no_abstract(self):
        self.assertEqual([], self.no_abstract.abstract)


class ClassificationTests(unittest.TestCase):

    def setUp(self):
        self.record = Record(os.path.join(test_dir_path, 'abstract_xml.xml'))
        self.no_class = Record(os.path.join(test_dir_path, 'genre_xml.xml'))

    def test_mods_classification_text(self):
        '''checks element value'''
        expected_classifications = ['PS3566.Y55 G7',
                                    'Y 4.B 22/3:S.PRT.109-8']
        self.assertEqual(expected_classifications, self.record.classification)

    def test_mods_no_classification(self):
        self.assertEqual([], self.no_class.classification)


class CollectionTests(unittest.TestCase):

    def setUp(self):
        self.record = Record(os.path.join(test_dir_path, 'abstract_xml.xml'))
        self.no_class = Record(os.path.join(test_dir_path, 'genre_xml.xml'))

    def test_mods_collections_location(self):
        expected_location = 'Special Collections & Archives, Florida State University Libraries, Tallahassee, Florida.'
        self.assertEqual(self.record.collection.location, expected_location)

    def test_mods_collection_title(self):
        expected_title = 'Pine Hill Plantation Papers, 1832-1926'
        self.assertEqual(self.record.collection.title, expected_title)

    def test_mods_collection_url(self):
        expected_url = 'http://purl.fcla.edu/fsu/MSS_0-204'
        self.assertEqual(self.record.collection.url, expected_url)


class OriginInfoTests(unittest.TestCase):

    def setUp(self):
        records = MODSReader(os.path.join(test_dir_path, 'originInfo_xml.xml'))
        self.first_record = next(records)
        self.second_record = next(records)
        self.third_record = next(records)

    def test_mods_date_range(self):
        '''checks date range reformatting'''
        expected = '1776-07-04 - today'
        self.assertEqual(expected, self.first_record.date_constructor())

    def test_mods_date_single(self):
        '''checks single date'''
        expected = '1984-10-14'
        self.assertEqual(expected, self.second_record.date_constructor())

    def test_mods_date_none(self):
        '''dates not in date_list should return None'''
        expected = None
        self.assertEqual(expected, self.third_record.date_constructor())


class LanguageTests(unittest.TestCase):

    def setUp(self):
        records = MODSReader(os.path.join(test_dir_path, 'language_xml.xml'))
        self.first_record = next(records)
        self.second_record = next(records)
        self.third_record = next(records)

    def test_mods_lang_text(self):
        '''checks languageTerm@type="text"'''
        expected = 'English'
        self.assertEqual(self.first_record.language[0].language, expected)

    def test_mods_lang_code(self):
        '''checks languageTerm@type="code"'''
        expected = 'eng'
        self.assertEqual(self.first_record.language[1].language, expected)

    def test_mods_lang_code_type(self):
        '''checks languageTerm@type="code"'''
        expected = 'code'
        self.assertEqual(self.first_record.language[1].type, expected)

    def test_mods_lang_untyped(self):
        '''checks untyped languageTerm elements'''
        expected = 'Klingon'
        self.assertEqual(self.second_record.language[0].language, expected)

    def test_mods_lang_untyped_type(self):
        '''checks untyped languageTerm elements'''
        expected = None
        self.assertEqual(self.second_record.language[0].type, expected)

    def test_mods_lang_none(self):
        '''checks lang None value'''
        expected = []
        self.assertEqual(self.third_record.language, expected)