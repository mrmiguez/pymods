import collections

from lxml import etree

from pymods.constants import NAMESPACES


Abstract = collections.namedtuple('Abstract', 'text type displayLabel')


class Record:

    def __init__(self, mods_xml):
        self.mods_xml = parse_xml(mods_xml)

    @property
    def abstract(self):
        """
        Access mods:abstract elements and return a list of dicts:
        return: [{abstract displayLabel: abstract text}] or None.
        """
        return [Abstract(getattr(abstract, 'text', ''),
                         abstract.attrib.get('type'),
                         abstract.attrib.get('displayLabel'))
                for abstract in self.mods_xml.iterfind(
                    './{0}abstract'.format(NAMESPACES['mods']))]

    @property
    def classification(self):
        """
        Access mods:classification element:
        return: [classification text, ... ] or None
        """
        return [classification.text for classification in
                self.mods_xml.iterfind(
                    './{0}classification'.format(NAMESPACES['mods']))]


def parse_xml(xml):
    try:
        return etree.parse(xml).getroot()
    except OSError:
        return etree.fromstring(xml)
