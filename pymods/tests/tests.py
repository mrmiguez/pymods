import os
import unittest

from pymods.reader import MODSReader

test_dir_path = os.path.abspath(os.path.dirname(__file__))


class AbstractTests(unittest.TestCase):
    def setUp(self):
        self.record = next(MODSReader(os.path.join(test_dir_path, 'abstract_xml.xml')))
        self.no_abstract = next(MODSReader(os.path.join(test_dir_path, 'genre_xml.xml')))

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
        self.record = next(MODSReader(os.path.join(test_dir_path, 'abstract_xml.xml')))
        self.no_class = next(MODSReader(os.path.join(test_dir_path, 'genre_xml.xml')))

    def test_mods_classification_text(self):
        '''checks element value'''
        expected_classifications = ['PS3566.Y55 G7',
                                    'Y 4.B 22/3:S.PRT.109-8']
        self.assertEqual(expected_classifications, self.record.classification)

    def test_mods_no_classification(self):
        self.assertEqual([], self.no_class.classification)


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.record = next(MODSReader(os.path.join(test_dir_path, 'abstract_xml.xml')))

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
        self.fourth_record = next(records)
        self.fifth_record = next(records)
        self.sixth_record = next(records)
        self.seventh_record = next(records)

    def test_mods_date_range(self):
        '''checks date range reformatting'''
        expected = '1776-07-04 - today'
        self.assertEqual(expected, self.first_record.dates[0].text)

    def test_mods_date_single(self):
        '''checks single date'''
        expected = '1984-10-14'
        self.assertEqual(expected, self.second_record.dates[0].text)

    def test_mods_date_none(self):
        '''dates not in date_list should return None'''
        expected = None
        self.assertEqual(expected, self.third_record.dates)

    def test_mods_edition(self):
        '''checks edition'''
        expected = 'Pre-print'
        self.assertEqual(expected, self.fourth_record.edition)

    def test_mods_issuance(self):
        '''checks issuance'''
        expected = 'integrating resource'
        self.assertEqual(expected, self.fifth_record.issuance[0])

    def test_mods_place(self):
        '''checks place of publication'''
        expected = [('Hogwartz', None),
                    ('hgz', 'code')]
        self.assertEqual(expected, self.sixth_record.publication_place)

    def test_mods_publisher(self):
        '''checks publisher'''
        expected = 'Image Comics'
        self.assertEqual(expected, self.seventh_record.publisher[0])


class LanguageTests(unittest.TestCase):
    def setUp(self):
        records = MODSReader(os.path.join(test_dir_path, 'language_xml.xml'))
        self.first_record = next(records)
        self.second_record = next(records)
        self.third_record = next(records)

    def test_mods_lang_text(self):
        '''checks languageTerm@type="text"'''
        expected = 'English'
        self.assertEqual(self.first_record.language[0].text, expected)

    def test_mods_lang_code(self):
        '''checks languageTerm@type="code"'''
        expected = 'eng'
        self.assertEqual(self.first_record.language[1].text, expected)

    def test_mods_lang_code_type(self):
        '''checks languageTerm@type="code"'''
        expected = 'code'
        self.assertEqual(self.first_record.language[1].type, expected)

    def test_mods_lang_untyped(self):
        '''checks untyped languageTerm elements'''
        expected = 'Klingon'
        self.assertEqual(self.second_record.language[0].text, expected)

    def test_mods_lang_untyped_type(self):
        '''checks untyped languageTerm elements'''
        expected = None
        self.assertEqual(self.second_record.language[0].type, expected)

    def test_mods_lang_none(self):
        '''checks lang None value'''
        expected = None
        self.assertEqual(self.third_record.text, expected)


class NameTests(unittest.TestCase):
    def setUp(self):
        self.record = next(MODSReader(os.path.join(test_dir_path, 'name_xml.xml')))

    def test_mods_names_pers_text(self):
        '''checks reformatting of name elements'''
        expected_names = ['Delp, Roy',
                          'Miguez, Matthew Roland, 1984-',
                          'Olsen, Stanford',
                          'Steinbeck, John, 1902-1968']
        self.assertEqual(sorted([name.text for name in self.record.get_pers_names]), sorted(expected_names))

    def test_mods_names_corp_text(self):
        '''checks reformatting of name elements'''
        expected_names = ['College of Music',
                          'Florida State University',
                          'Florida, Legislature, House of Representatives, Office of the Clerk']
        self.assertEqual(sorted([name.text for name in self.record.get_corp_names]), sorted(expected_names))


class PhysicalDescriptionTests(unittest.TestCase):
    def setUp(self):
        records = MODSReader(os.path.join(test_dir_path, 'physicalDesc_xml.xml'))
        self.first_record = next(records)
        self.second_record = next(records)
        self.third_record = next(records)
        self.fourth_record = next(records)
        self.fifth_record = next(records)

    def test_mods_digital_origin(self):
        '''checks digital origin'''
        expected = 'reformatted digital'
        self.assertEqual(expected, self.first_record.digital_origin)

    def test_mods_extent(self):
        '''checks extent'''
        expected = ['5 pieces', '2 tonnes']
        self.assertTrue(expected, self.second_record.extent)

    def test_mods_form(self):
        '''checks form'''
        expected = ['pancakes']
        self.assertTrue(expected, self.third_record.extent)

    def test_mods_physdesc_note(self):
        '''checks physicalDescription/note'''
        expected = ['Battered & bruised',
                    'Infinite summer']
        self.assertTrue(expected, self.fourth_record.physical_description_note)

    def test_mods_internet_media_type(self):
        '''checks form'''
        expected = ['food/pancakes']
        self.assertTrue(expected, self.fifth_record.internet_media_type)


class GenreTests(unittest.TestCase):
    def setUp(self):
        records = MODSReader(os.path.join(test_dir_path, 'genre_xml.xml'))
        self.first_record = next(records)
        self.second_record = next(records)
        self.no_genre = next(MODSReader(os.path.join(test_dir_path, 'originInfo_xml.xml')))

    def test_mods_genre_text(self):
        '''checks genre term values'''
        expected = ['Personal correspondence',
                    'receipts (financial records)']
        results = []
        for genre in (self.first_record.genre, self.second_record.genre):
            results.append(genre[0].text)
        self.assertEqual(expected, results)

    def test_mods_genre_authority(self):
        '''checks genre authority value'''
        expected = ['aat', 'lcgft']
        results = []
        for genre in (self.first_record.genre, self.second_record.genre):
            results.append(genre[0].authority)
        self.assertEqual(expected, sorted(results))

    def test_mods_genre_authorityURI(self):
        '''checks genre authorityURI'''
        expected = [None, 'http://vocab.getty.edu/aat']
        results = []
        for genre in (self.first_record.genre, self.second_record.genre):
            results.append(genre[0].authorityURI)
        self.assertEqual(expected, results)

    def test_mods_genre_valueURI(self):
        '''checks genre valueURI'''
        expected = ['http://id.loc.gov/authorities/genreForms/gf2014026141',
                    'http://vocab.getty.edu/page/aat/300027015']
        results = []
        for genre in (self.first_record.genre, self.second_record.genre):
            results.append(genre[0].valueURI)
        self.assertEqual(expected, results)

    def test_mods_genre_none(self):
        '''checks for None value for missing element'''
        expected = []
        self.assertEqual(expected, self.no_genre.genre)


class GeographicCodeTests(unittest.TestCase):
    """

    """

    def setUp(self):
        self.record = next(MODSReader(os.path.join(test_dir_path, 'subject_xml.xml')))

    def test_mods_geographicCode(self):
        '''checks subject/geographicCode'''
        expected = ['7013331',
                    '7013938']
        self.assertEqual(expected, self.record.geographic_code)


class IdentifierTests(unittest.TestCase):
    def setUp(self):
        self.record = next(MODSReader(os.path.join(test_dir_path, 'identifier_xml.xml')))

    def test_mods_purl_search(self):
        '''checks PURL service'''
        purl = 'http://purl.flvc.org/fsu/fd/FSU_MSS0204_B03_F10_13'
        self.assertEqual(purl, self.record.purl[0])

    def test_mods_pid_search(self):
        '''checks fedora PID service'''
        pid = 'fsu:1028'
        self.assertEqual(pid, self.record.pid)

    def test_mods_local_identifier(self):
        '''checks IID service'''
        iid = 'FSU_MSS0204_B03_F10_13'
        self.assertEqual(iid, self.record.iid)

    def test_mods_doi_search(self):
        '''checks DOI service'''
        doi = '10.3389/fmicb.2016.00458'
        self.assertEqual(doi, self.record.doi)


class NoteTests(unittest.TestCase):
    """

    """

    def setUp(self):
        self.record = next(MODSReader(os.path.join(test_dir_path, 'abstract_xml.xml')))

    def test_mods_note_typed(self):
        '''checks typed note'''
        expected = 'Pulled from garbage.'
        self.assertEqual(expected, self.record.get_notes(type='acquisition')[0].text)

    def test_mods_note_labelled(self):
        '''checks labelled note'''
        expected = '0234.234.532'
        self.assertEqual(expected, self.record.get_notes(displayLabel='Related burial(s)')[0].text)

    def test_mods_note_untyped(self):
        '''checks untyped note'''
        expected = 'Stick it in a note.'
        self.assertEqual(expected, self.record.get_notes(type=None)[0].text)


class PhysicalLocationTests(unittest.TestCase):
    """
    location text values return as a list or exception raised if none
    """

    def setUp(self):
        self.record = next(MODSReader(os.path.join(test_dir_path, 'location_xml.xml')))

    def test_mods_physical_location(self):
        expected = ['The Circus', 'The Zoo',
                    'The Snow']
        self.assertTrue(all(x in expected for x in self.record.physical_location))


class RightsTests(unittest.TestCase):
    """

    """

    def setUp(self):
        records = MODSReader(os.path.join(test_dir_path, 'rights_xml.xml'))
        self.first_record = next(records)
        self.second_record = next(records)
        self.third_record = next(records)

    def test_mods_rights_text(self):
        '''checks rights text'''
        expected = 'Cue legalese'
        self.assertEqual(expected, self.first_record.rights[0].text)

    def test_mods_rights_uri(self):
        '''checks rights URI'''
        expected = 'http://rightsstatements.org/vocab/InC/1.0/'
        self.assertEqual(expected, self.first_record.rights[0].uri)

    def test_mods_rights_camelCased(self):
        '''checks camel-cased @type'''
        expected = 'camelCasedCamelHump'
        self.assertEqual(expected, self.third_record.rights[0].text)


class SubjectTests(unittest.TestCase):
    """

    """

    def setUp(self):
        records = MODSReader(os.path.join(test_dir_path, 'subject_xml.xml'))
        self.first_record = next(records)
        self.second_record = next(records)
        self.third_record = next(records)
        self.fourth_record = next(records)
        self.fifth_record = next(records)

    def test_mods_subject_simple_text(self):
        '''checks simple subject text'''
        expected = ['Poetry',
                    'Childhood and youth',
                    'Architectural design']
        results = []
        for subject in self.second_record.subjects:
            results.append(subject.text)
        self.assertEqual(sorted(expected), sorted(results))

    def test_mods_subject_simple_authority(self):
        '''checks simple subject text'''
        expected = ['lctgm', 'fast', 'lcsh']
        results = []
        for subject in self.second_record.subjects:
            results.append(subject.authority)
        self.assertEqual(sorted(expected), sorted(results))

    def test_mods_subject_simple_uri(self):
        '''checks simple subject text'''
        expected = ['http://id.loc.gov/vocabulary/graphicMaterials/tgm007948',
                    'http://id.loc.gov/authorities/subjects/sh99004940',
                    'http://id.worldcat.org/fast/813184']
        results = []
        for subject in self.second_record.subjects:
            results.append(subject.uri)
        self.assertEqual(sorted(expected), sorted(results))

    def test_mods_subject_complex_text(self):
        '''checks complex subject text'''
        expected = 'United States--History--Civil War, 1861-1865'
        self.assertEqual(expected, self.third_record.subjects[0].text)

    def test_mods_subject_name(self):
        '''checks reformatting of name subject'''
        expected = 'Lincoln, Abraham, 1809-1865--Assassination'
        self.assertEqual(expected, self.fourth_record.subjects[0].text)

    def test_mods_subject_name_no_authority_text(self):
        '''checks handling of subject w/ no @authority'''
        expected = 'Baruch, Bernard M. (Bernard Mannes), 1870-1965'
        self.assertEqual(expected, self.fifth_record.subjects[0].text)


class TitleTests(unittest.TestCase):
    """

    """

    def setUp(self):
        records = MODSReader(os.path.join(test_dir_path, 'title_xml.xml'))
        self.first_record = next(records)
        self.second_record = next(records)
        self.third_record = next(records)

    def test_mods_title_simple(self):
        '''checks simple title formatting'''
        expected = "Gravity's Rainbow"
        self.assertEqual(expected, self.first_record.titles[0])

    def test_mods_title_subtitle(self):
        '''checks title & subtitle formatting'''
        expected = "Homer Simpson: A retrospective"
        self.assertEqual(expected, self.second_record.titles[0])

    def test_mods_title_complex(self):
        '''checks complex formatting'''
        expected = "A Title: Should never be alone"
        self.assertEqual(expected, self.third_record.titles[0])


class TypeOfResourceTests(unittest.TestCase):
    """

    """

    def setUp(self):
        records = MODSReader(os.path.join(test_dir_path, 'resourceType_xml.xml'))
        self.first_record = next(records)
        self.second_record = next(records)

    def test_mods_resourceType_text(self):
        '''checks typeOfResource element'''
        expected = 'still image'
        self.assertEqual(expected, self.first_record.type_of_resource)

    def test_mods_resourceType_none(self):
        '''checks typeOfResource None value'''
        expected = None
        self.assertEqual(expected, self.second_record.type_of_resource)


if __name__ == '__main__':
    unittest.main()
