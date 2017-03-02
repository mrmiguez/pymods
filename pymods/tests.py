from os.path import abspath, dirname, join
import unittest
from pymods import MODS, FSUDL, OAI

test_dir_path = abspath(dirname(__file__))


class AbstractTests(unittest.TestCase):

    abstract_xml = MODS(join(test_dir_path, 'tests/abstract_xml.xml'))

    def test_mods_abstract_text(self):
        '''checks element value'''
        expected_text = ['Remain calm! This is only a test!']
        result = MODS.abstract(self.abstract_xml.record_list[0])
        self.assertTrue(all(x in result for x in expected_text))


class ClassificationTests(unittest.TestCase):

    abstract_xml = MODS(join(test_dir_path, 'tests/abstract_xml.xml'))

    def test_mods_classification_text(self):
        '''checks element value'''
        expected_classifications = ['PS3566.Y55 G7',
                                    'Y 4.B 22/3:S.PRT.109-8']
        results = []
        for classification in MODS.classification(self.abstract_xml.record_list[0]):
            results.append(classification)
        self.assertTrue(all(x in expected_classifications for x in results))


class CollectionTests(unittest.TestCase):

    abstract_xml = MODS(join(test_dir_path, 'tests/abstract_xml.xml'))
    collection_dict = MODS.collection(abstract_xml.record_list[0])

    def test_mods_collection(self):
        '''checks returned collection object'''
        self.assertIsInstance(self.collection_dict, dict)

    def test_mods_collection_location(self):
        '''checks location text in collection dict'''
        expected_location = 'Special Collections & Archives, Florida State University Libraries, Tallahassee, Florida.'
        result = self.collection_dict['location']
        self.assertEqual(result, expected_location)

    def test_mods_collection_title(self):
        '''checks title text in collection dict'''
        expected_title = 'Pine Hill Plantation Papers, 1832-1926'
        result = self.collection_dict['title']
        self.assertEqual(result, expected_title)

    def test_mods_collection_url(self):
        '''checks url text in collection dict'''
        expected_url = 'http://purl.fcla.edu/fsu/MSS_0-204'
        result = self.collection_dict['url']
        self.assertEqual(result, expected_url)


class DateTests(unittest.TestCase):

    def test_mods_date(self):
        '''temp'''
        return True


#class DigitalOriginTests(unittest.TestCase):


#class ExtentTests(unittest.TestCase):


#class FormTests(unittest.TestCase):


#class GenreTests(unittest.TestCase):


#class GeographicCodeTests(unittest.TestCase):


class IdentifierTests(unittest.TestCase):

    identifier_xml = MODS(join(test_dir_path, 'tests/identifier_xml.xml'))

    def test_fsudl_purl_search(self):
        '''checks PURL service'''
        purl = 'http://purl.flvc.org/fsu/fd/FSU_MSS0204_B03_F10_13'
        result = FSUDL.purl_search(self.identifier_xml.record_list[0])
        self.assertEqual(result, purl)

    def test_fsudl_pid_search(self):
        '''checks fedora PID service'''
        pid = 'fsu:1028'
        result = FSUDL.pid_search(self.identifier_xml.record_list[0])
        self.assertEqual(result, pid)

    def test_fsudl_local_identifier(self):
        '''checks IID service'''
        iid = 'FSU_MSS0204_B03_F10_13'
        result = FSUDL.local_identifier(self.identifier_xml.record_list[0])
        self.assertEqual(result, iid)

    def test_fsudl_doi_search(self):
        '''checks fedora pid service'''
        doi = '10.3389/fmicb.2016.00458'
        result = FSUDL.doi_search(self.identifier_xml.record_list[0])
        self.assertEqual(result, doi)


#class IssuanceTests(unittest.TestCase):


#class LanguageTests(unittest.TestCase):


class NameTests(unittest.TestCase):

    name_xml = MODS(join(test_dir_path, 'tests/name_xml.xml'))

    def test_mods_names_pers_text(self):
        '''checks reformatting of name elements'''
        expected_names = ['Delp, Roy',
                          'Miguez, Matthew Roland, 1984-',
                          'Olsen, Stanford',
                          'Steinbeck, John, 1902-1968']
        for name in MODS.name_constructor(self.name_xml.record_list[0]):
            if 'type' in name.keys() and name['type'] == 'personal':
                self.assertTrue(name['text'] in expected_names)

    def test_mods_names_corp_text(self):
        '''checks reformatting of name elements'''
        expected_names = ['College of Music',
                          'Florida State University',
                          'Florida, Legislature, House of Representatives, Office of the Clerk']
        for name in MODS.name_constructor(self.name_xml.record_list[0]):
            if 'type' in name.keys() and name['type'] == 'corporate':
                self.assertTrue(name['text'] in expected_names)


#class NoteTests(unittest.TestCase):


#class PhysicalDescriptionTests(unittest.TestCase):


#class PhysicalLocationTests(unittest.TestCase):


#class PublicationPlaceTests(unittest.TestCase):


#class PublisherTests(unittest.TestCase):


#class RightsTests(unittest.TestCase):


#class SubjectTests(unittest.TestCase):


#class TitleTests(unittest.TestCase):


#class TypeOfResourceTests(unittest.TestCase):


if __name__ == '__main__':
    unittest.main()