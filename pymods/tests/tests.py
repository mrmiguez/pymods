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
