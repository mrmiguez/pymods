import unittest
from pymods import MODS, FSUDL, OAI

class AbstractTests(unittest.TestCase):

    abstract_xml = MODS('tests/abstract_xml.xml')

    def test_mods_abstract_text(self):
        '''checks element value'''
        test_string = 'Remain calm! This is only a test!'
        result = MODS.abstract(self.abstract_xml.record_list[0])
        self.assertEqual(result, test_string)

class NameTests(unittest.TestCase):

    name_xml = MODS('tests/name_xml.xml')

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


if __name__ == '__main__':
    unittest.main()