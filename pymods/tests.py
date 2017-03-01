import unittest
from pymods import MODS, FSUDL, OAI

class NameTests(unittest.TestCase):

    name_xml = MODS('tests/name_xml.xml')

    def test_mods_names_pers_text(self):
        expected_names = ['Olsen, Stanford',
                          'Delp, Roy',
                          'Miguez, Matthew Roland 1984-']
        for name in MODS.name_constructor(self.name_xml.record_list[0]):
            if 'type' in name.keys() and name['type'] == 'personal':
                self.assertTrue(name['text'] in expected_names)

    def test_mods_names_corp_text(self):
        expected_names = ['College of Music',
                          'Florida State University',
                          'Florida, Legislature, House of Representatives, Office of the Clerk']
        for name in MODS.name_constructor(self.name_xml.record_list[0]):
            if 'type' in name.keys() and name['type'] == 'corporate':
                self.assertTrue(name['text'] in expected_names)


if __name__ == '__main__':
    unittest.main()