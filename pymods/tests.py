from os.path import abspath, dirname, join
import unittest
import pymods

test_dir_path = abspath(dirname(__file__))


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

    def test_mods_physical_location_exception(self):
        no_location = self.location_xml.record_list[1].physical_location()
        self.assertRaises(pymods.exceptions.ElementNotFound, msg="Record does not contain the specified element")


if __name__ == '__main__':
    unittest.main()
