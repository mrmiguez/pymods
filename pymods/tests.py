from os.path import abspath, dirname, join
import unittest
import pymods

test_dir_path = abspath(dirname(__file__))


class AbstractTests(unittest.TestCase):
    """
    abstract text values return as a list or exception raised if none
    """

    abstract_xml = pymods.MODSReader(join(test_dir_path, 'tests/abstract_xml.xml'))

    def test_mods_abstract_text(self):
        expected_text = ['Remain calm! This is only a test!']
        result = self.abstract_xml.record_list[0].abstract()
        self.assertTrue(all(x in result for x in expected_text))


class ClassificationTests(unittest.TestCase):
    """
    classification text values return as a list or exception raised if none
    """

    abstract_xml = pymods.MODSReader(join(test_dir_path, 'tests/abstract_xml.xml'))

    def test_mods_classification_text(self):
        '''checks element value'''
        expected_classifications = ['PS3566.Y55 G7',
                                    'Y 4.B 22/3:S.PRT.109-8']
        results = []
        for classification in self.abstract_xml.record_list[0].classification():
            results.append(classification)
        self.assertTrue(all(x in expected_classifications for x in results))


class OriginInfoTests(unittest.TestCase):

    originInfo_xml = pymods.MODSReader(join(test_dir_path, 'tests/originInfo_xml.xml'))

    def test_mods_date_range(self):
        '''checks date range reformatting'''
        expected = '1776-07-04 - today'
        result = self.originInfo_xml.record_list[0].date_constructor()
        self.assertEqual(expected, result)

    def test_mods_date_single(self):
        '''checks single date'''
        expected = '1984-10-14'
        result = self.originInfo_xml.record_list[1].date_constructor()
        self.assertEqual(expected, result)

    def test_mods_date_none(self):
        '''dates not in date_list should return None'''
        expected = None
        result = self.originInfo_xml.record_list[2].date_constructor()
        self.assertEqual(expected, result)

    def test_mods_edition(self):
        '''checks edition'''
        expected = 'Pre-print'
        result =self.originInfo_xml.record_list[3].edition()
        self.assertEqual(result, expected)

    def test_mods_issuance(self):
        '''checks issuance'''
        expected = 'integrating resource'
        result = self.originInfo_xml.record_list[4].issuance()
        self.assertEqual(result[0], expected)

    def test_mods_place(self):
        '''checks place of publication'''
        expected = [{'code': 'hgz',
                    'untyped': 'Hogwartz'}]
        result = self.originInfo_xml.record_list[5].publication_place()
        self.assertEqual(result, expected)

    def test_mods_publisher(self):
        '''checks publisher'''
        expected = 'Image Comics'
        result = self.originInfo_xml.record_list[6].publisher()
        self.assertEqual(result[0], expected)


class PhysicalDescriptionTests(unittest.TestCase):

    physicalDesc_xml = pymods.MODSReader(join(test_dir_path, 'tests/physicalDesc_xml.xml'))

    def test_mods_digital_origin(self):
        '''checks digital origin'''
        expected = 'reformatted digital'
        result = self.physicalDesc_xml.record_list[0].digital_origin()
        self.assertEqual(result, expected)

    def test_mods_extent(self):
        '''checks extent'''
        expected = ['5 pieces', '2 tonnes']
        result = self.physicalDesc_xml.record_list[1].extent()
        self.assertTrue(all(x in result for x in expected))

    def test_mods_form(self):
        '''checks form'''

    def test_mods_physdesk_note(self):
        '''checks physicalDescription/note'''
        expected = ['Battered & bruised',
                    'Infinite summer']
        results = []
        for note in self.physicalDesc_xml.record_list[3].physical_description_note():
            results.append(note)
        self.assertTrue(all(x in results for x in expected))


class GenreTests(unittest.TestCase):

    genre_xml = pymods.MODSReader(join(test_dir_path, 'tests/genre_xml.xml'))

    def test_mods_genre_text(self):
        '''checks genre term values'''
        expected = ['Personal correspondence',
                    'receipts (financial records)']
        results = []
        for record in self.genre_xml.record_list:
            if record.genre() is not None:
                results.append(record.genre()[0]['term'])
        self.assertTrue(all(x in results for x in expected))

    def test_mods_genre_authority(self):
        '''checks genre authority value'''
        expected = ['aat', 'lcgft']
        results = []
        for record in self.genre_xml.record_list:
            if record.genre() is not None:
                results.append(record.genre()[0]['authority'])
        self.assertTrue(all(x in results for x in expected))

    def test_mods_genre_authorityURI(self):
        '''checks genre authorityURI'''
        expected = ['http://vocab.getty.edu/aat']
        results = []
        for record in self.genre_xml.record_list:
            if record.genre() is not None and 'authorityURI' in record.genre()[0].keys():
                results.append(record.genre()[0]['authorityURI'])
        self.assertTrue(all(x in results for x in expected))

    def test_mods_genre_valueURI(self):
        '''checks genre valueURI'''
        expected = ['http://id.loc.gov/authorities/genreForms/gf2014026141',
                    'http://vocab.getty.edu/page/aat/300027015']
        results = []
        for record in self.genre_xml.record_list:
            if record.genre() is not None:
                results.append(record.genre()[0]['valueURI'])
        self.assertTrue(all(x in results for x in expected))

    def test_mods_genre_none(self):
        '''checks for None value for missing element'''
        expected = None
        result = self.genre_xml.record_list[2].genre()
        self.assertEqual(result, expected)


class PhysicalLocationTests(unittest.TestCase):
    """
    location text values return as a list or exception raised if none
    """

    location_xml = pymods.MODSReader(join(test_dir_path, 'tests/location_xml.xml'))

    def test_mods_physical_location(self):
        expected = ['The Circus', 'The Zoo',
                    'The Snow']
        results = []
        for location in self.location_xml.record_list[0].physical_location():
            results.append(location)
        self.assertTrue(all(x in results for x in expected))


if __name__ == '__main__':
    unittest.main()
