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


class CollectionTests(unittest.TestCase):
    """

    """
    abstract_xml = pymods.MODSReader(join(test_dir_path, 'tests/abstract_xml.xml'))
    collection_dict = abstract_xml.record_list[0].collection()

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
    """
    
    """
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


class GeographicCodeTests(unittest.TestCase):
    """
    
    """
    subject_xml = pymods.MODSReader(join(test_dir_path, 'tests/subject_xml.xml'))

    def test_mods_geographicCode(self):
        '''checks subject/geographicCode'''
        expected = ['7013331',
                    '7013938']
        result = self.subject_xml.record_list[0].geographic_code()
        self.assertTrue(all(x in result for x in expected))


class IdentifierTests(unittest.TestCase):
    """

    """
    identifier_xml = pymods.MODSReader(join(test_dir_path, 'tests/identifier_xml.xml'))

    def test_mods_purl_search(self):
        '''checks PURL service'''
        purl = 'http://purl.flvc.org/fsu/fd/FSU_MSS0204_B03_F10_13'
        result = self.identifier_xml.record_list[0].purl_search()
        self.assertEqual(result, purl)

    def test_mods_pid_search(self):
        '''checks fedora PID service'''
        pid = 'fsu:1028'
        result = self.identifier_xml.record_list[0].pid_search()
        self.assertEqual(result, pid)

    def test_mods_local_identifier(self):
        '''checks IID service'''
        iid = 'FSU_MSS0204_B03_F10_13'
        result = self.identifier_xml.record_list[0].local_identifier()
        self.assertEqual(result, iid)

    def test_mods_doi_search(self):
        '''checks fedora pid service'''
        doi = '10.3389/fmicb.2016.00458'
        result = self.identifier_xml.record_list[0].doi_search()
        self.assertEqual(result, doi)


class LanguageTests(unittest.TestCase):
    """
    
    """
    language_xml = pymods.MODSReader(join(test_dir_path, 'tests/language_xml.xml'))

    def test_mods_lang_text(self):
        '''checks languageTerm@type="text"'''
        expected = 'English'
        result = self.language_xml.record_list[0].language()
        self.assertEqual(result[0]['text'], expected)

    def test_mods_lang_code(self):
        '''checks languageTerm@type="code"'''
        expected = 'eng'
        result = self.language_xml.record_list[0].language()
        self.assertEqual(result[0]['code'], expected)

    def test_mods_lang_untyped(self):
        '''checks untyped languageTerm elements'''
        expected = 'Klingon'
        result = self.language_xml.record_list[1].language()
        self.assertEqual(result[0]['untyped'], expected)

    def test_mods_lang_none(self):
        '''checks lang None value'''
        expected = None
        result = self.language_xml.record_list[2].language()
        self.assertEqual(result, expected)


class NameTests(unittest.TestCase):
    """
    
    """
    name_xml = pymods.MODSReader(join(test_dir_path, 'tests/name_xml.xml'))

    def test_mods_names_pers_text(self):
        '''checks reformatting of name elements'''
        expected_names = ['Delp, Roy',
                          'Miguez, Matthew Roland, 1984-',
                          'Olsen, Stanford',
                          'Steinbeck, John, 1902-1968']
        for name in self.name_xml.record_list[0].name_constructor():
            if 'type' in name.keys() and name['type'] == 'personal':
                self.assertTrue(name['text'] in expected_names)

    def test_mods_names_corp_text(self):
        '''checks reformatting of name elements'''
        expected_names = ['College of Music',
                          'Florida State University',
                          'Florida, Legislature, House of Representatives, Office of the Clerk']
        for name in self.name_xml.record_list[0].name_constructor():
            if 'type' in name.keys() and name['type'] == 'corporate':
                self.assertTrue(name['text'] in expected_names)


class NoteTests(unittest.TestCase):
    """
    
    """
    abstract_xml = pymods.MODSReader(join(test_dir_path, 'tests/abstract_xml.xml'))

    def test_mods_note_typed(self):
        '''checks typed note'''
        expected = 'Pulled from garbage.'
        for note in self.abstract_xml.record_list[0].note():
            if 'acquisition' in note.keys():
                result = note['acquisition']
        self.assertEqual(result, expected)

    def test_mods_note_labelled(self):
        '''checks labelled note'''
        expected = '0234.234.532'
        for note in self.abstract_xml.record_list[0].note():
            if 'Related burial(s)' in note.keys():
                result = note['Related burial(s)']
        self.assertEqual(result, expected)

    def test_mods_note_untyped(self):
        '''checks untyped note'''
        expected = 'Stick it in a note.'
        for note in self.abstract_xml.record_list[0].note():
            if 'untyped' in note.keys():
                result = note['untyped']
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


class RightsTests(unittest.TestCase):
    """
    
    """
    rights_xml = pymods.MODSReader(join(test_dir_path, 'tests/rights_xml.xml'))

    def test_mods_rights_text(self):
        '''checks rights text'''
        expected = 'Cue legalese'
        result = self.rights_xml.record_list[0].rights()['text']
        self.assertEqual(result, expected)

    def test_mods_rights_uri(self):
        '''checks rights URI'''
        expected = 'http://rightsstatements.org/vocab/InC/1.0/'
        result = self.rights_xml.record_list[0].rights()['URI']
        self.assertEqual(result, expected)

    def test_mods_rights_camelCased(self):
        '''checks camel-cased @type'''
        expected = 'camelCasedCamelHump'
        result = self.rights_xml.record_list[2].rights()['text']
        self.assertEqual(result, expected)


class SubjectTests(unittest.TestCase):
    """
    
    """
    subject_xml = pymods.MODSReader(join(test_dir_path, 'tests/subject_xml.xml'))

    def test_mods_subject_simple_text(self):
        '''checks simple subject text'''
        expected = ['Poetry',
                    'Childhood and youth',
                    'Architectural design']
        results = []
        for subject in self.subject_xml.record_list[1].subject():
            results.append(subject['children'][0]['term'])
        self.assertTrue(all(x in results for x in expected))

    def test_mods_subject_simple_authority(self):
        '''checks simple subject text'''
        expected = ['lctgm', 'fast', 'lcsh']
        results = []
        for subject in self.subject_xml.record_list[1].subject():
            results.append(subject['authority'])
        self.assertTrue(all(x in results for x in expected))

    def test_mods_subject_simple_uri(self):
        '''checks simple subject text'''
        expected = ['http://id.loc.gov/vocabulary/graphicMaterials/tgm007948',
                    'http://id.loc.gov/authorities/subjects/sh99004940',
                    'http://id.worldcat.org/fast/813184']
        results = []
        for subject in self.subject_xml.record_list[1].subject():
            if 'valueURI' in subject.keys():
                if subject['valueURI'] is not None:
                    results.append(subject['valueURI'])
            else:
                for child in subject['children']:
                    if child['valueURI'] is not None:
                        results.append(child['valueURI'])
        self.assertTrue(all(x in results for x in expected))

    def test_mods_subject_complex_text(self):
        '''checks complex subject text'''
        expected = 'United States--History--Civil War, 1861-1865'
        result = self.subject_xml.record_list[2].subject_constructor()[0]
        self.assertEqual(result, expected)

    def test_mods_subject_name(self):
        '''checks reformatting of name subject'''
        expected = 'Lincoln, Abraham, 1809-1865--Assassination'
        result = self.subject_xml.record_list[3].subject()[0]['text']
        self.assertEqual(result, expected)

    def test_mods_subject_name_no_authority_text(self):
        '''checks handling of subject w/ no @authority'''
        expected = 'Baruch, Bernard M. (Bernard Mannes), 1870-1965'
        result = self.subject_xml.record_list[4].subject()[0]['text']
        self.assertEqual(result, expected)


class TitleTests(unittest.TestCase):
    """
    
    """
    title_xml = pymods.MODSReader(join(test_dir_path, 'tests/title_xml.xml'))

    def test_mods_title_simple(self):
        '''checks simple title formatting'''
        expected = "Gravity's Rainbow"
        result = self.title_xml.record_list[0].title_constructor()[0]
        self.assertEqual(result, expected)

    def test_mods_title_subtitle(self):
        '''checks title & subtitle formatting'''
        expected = "Homer Simpson: A retrospective"
        result = self.title_xml.record_list[1].title_constructor()[0]
        self.assertEqual(result, expected)

    def test_mods_title_complex(self):
        '''checks complex formatting'''
        expected = "A Title: Should never be alone"
        result = self.title_xml.record_list[2].title_constructor()[0]
        self.assertEqual(result, expected)


class TypeOfResourceTests(unittest.TestCase):
    """
    
    """
    resourceType_xml = pymods.MODSReader(join(test_dir_path, 'tests/resourceType_xml.xml'))

    def test_mods_resourceType_text(self):
        '''checks typeOfResource element'''
        expected = 'still image'
        result = self.resourceType_xml.record_list[0].type_of_resource()
        self.assertEqual(result, expected)

    def test_mods_resourceType_none(self):
        '''checks typeOfResource None value'''
        expected = None
        result = self.resourceType_xml.record_list[1].type_of_resource()
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
