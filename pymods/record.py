import re
import collections
from lxml import etree
from pymods.constants import NAMESPACES, DATE_FIELDS

Abstract = collections.namedtuple('Abstract', 'text type displayLabel')
Collection = collections.namedtuple('Collection', 'location title url')
Genre = collections.namedtuple('Genre', 'term authority authorityURI valueURI')
Identifier = collections.namedtuple('Identifier', 'text type')
Language = collections.namedtuple('Language', 'language type')
Name = collections.namedtuple('Name', 'name_parts roles type')
NamePart = collections.namedtuple('NamePart', 'name type')
Role = collections.namedtuple('Role', 'role type')
Note = collections.namedtuple('Note', 'text type dispayLabel')
PublicationPlace = collections.namedtuple('PublicationPlace', 'place type')
mods = NAMESPACES['mods']


class Record(etree.ElementBase):

    def _init(self):
        super(Record, self)._init()


class MODSRecord(Record):

    def _init(self):
        super(MODSRecord, self)._init()

    @property
    def abstract(self):
        """
        Pull information from mods:abstract element(s).
        :return: list of Abstract elements with text, type, and displayLabel attributes
        """
        return [Abstract(getattr(abstract, 'text', ''),
                         abstract.attrib.get('type'),
                         abstract.attrib.get('displayLabel'))
                for abstract in self.iterfind('./{0}abstract'.format(mods))]

    @property
    def classification(self):
        """
        Pull information from mods:classification element(s)
        :return: list of text from classification element(s)
        """
        return [classification.text
                for classification in self.iterfind('./{0}classification'.format(mods))]

    # @property
    # def collection(self):
    #     """
    #     Retrieve archival collection metadata from mods:relatedItem[type="host"]:
    #             :return: A Collection element with location, title, and url attributes
    #     """
    #     related_item = self.findall('./{0}relatedItem[@type="host"]'.format(mods))[0]
    #     return Collection(self.physical_location(related_item)[0],
    #                       self._title_constructor(related_item)[0],
    #                       self._url(related_item)[0])

    # def date_constructor(self, elem=None):
    #     """
    #     Accesses mods:dateIssued, mods:dateCreated, mods:copyrightDate, and mods:dateOther underneath mods:originInfo. Other date-type elements are ignored:
    #     return: A date containing string or None.
    #     """
    #     pass

    @property
    def digital_origin(self):
        """
        Get text from mods:edition element.
        :return: String containing digital origin information
        """
        try:
            return self.find('.//{0}digitalOrigin'.format(mods)).text
        except AttributeError:
            return None

    @property
    def doi(self):
        """
        :return: item's DOI.
        """
        return self._identifier(id_type='DOI')

    @property
    def edition(self):
        """
        Accesses mods:edition element:
        return: element text or None.
        """
        try:
            return self.find('.//{0}edition'.format(mods)).text
        except AttributeError:
            return None

    @property
    def extent(self):
        """
        Accesses mods:extent element:
        return: list of mods:extent texts
        """
        return [extent.text for extent in self.iterfind('.//{0}extent'.format(mods))]

    @property
    def form(self):
        """
        Accesses mods:physicalDescription/mods:form element:
        return: list of mods:form texts
        """
        return [form.text for form in self.iterfind('./{0}physicalDescription/{0}form'.format(mods))]

    @property
    def genre(self):
        """
        Accesses mods:genre element:
        :return: A list containing Genre elements with term, authority,
            authorityURI, and valueURI attributes
        """
        return [Genre(genre.text,
                      genre.attrib.get('authority'),
                      genre.attrib.get('authorityURI'),
                      genre.attrib.get('valueURI'))
                for genre in self.iterfind('./{0}genre'.format(mods))]

    @property
    def geographic_code(self):
        """
        Accesses mods:geographicCode element:
        return: list of mods:geographicCode texts.
        """
        return [geocode.text for geocode in self.iterfind('./{0}subject/{0}geographicCode'.format(mods))]

    @property
    def identifier(self):
        """

        :return:
        """
        return self._identifier()

    @property
    def iid(self):
        """
        
        :return: 
        """
        return self._identifier(id_type='IID')

    @property
    def issuance(self):
        """
        Accesses mods:issuance element:
        return: list of mods:issuance texts.
        """
        return [issuance.text for issuance in self.iterfind('.//{0}issuance'.format(mods))]

    # def language(self, elem=None):
    #     """
    #     Accesses mods:languageterm elements:
    #     :return: list of of dicts [{term-type: term}] or None.
    #     """
    #     pass

    # def _nameGen_(names, full_name):
    #     """
    #
    #     :param full_name:
    #     :return:
    #     """
    #     pass

    # def name_constructor(self, elem=None):
    #     """
    #     Accesses mods:name/mods:namePart elements and reconstructs names into LOC order:
    #     return: a list of strings.
    #     """
    #     pass

    @property
    def note(self):
        """
        Access mods:note elements and return a list of dicts:
        :return: A list containing Note elements with text, type, and displayLabel attributes
        """
        return [Note(note.text, note.attrib.get('type'), note.attrib.get('displayLabel'))
                for note in self.iterfind('./{0}note'.format(mods))]

    @property
    def physical_description_note(self):
        """
        Access mods:physicalDescription/mods:note elements and return a list of text values:
        :return: list of note text values.
        """
        return [note.text for note in self.findall('./{0}physicalDescription/{0}note'.format(mods))]

    # def physical_location(self, elem=None):
    #     """
    #     Access mods:mods/mods:location/mods:physicalLocation and return text values.
    #     return: list of element text values.
    #     """
    #     pass

    @property
    def pid(self):
        """
        Get fedora PID from MODS record:
        return: item's fedora PID.
        """
        return self._identifier(id_type='fedora')

    # def publication_place(self, elem=None):
    #     """
    #     Access mods:place and return a list of dicts:
    #     return: [{termType: termText}, {'untyped': termText}, ...]
    #     """
    #     pass

    @property
    def publisher(self):
        """
        Access mods:publisher and return a list of text values:
        return: [publisher, ...]
        """
        return [publisher.text for publisher in
                self.findall('./{0}originInfo/{0}publisher'.format(mods))]

    @property
    def purl(self):
        """
        Accesses record's Persistent URL from mods:mods/mods:location/mods:url:
        return: item PURL as string.
        """
        purl = re.compile('((http://purl)[\w\d:#@%/;$()~_?\+-=\\\.&]+)')
        return [url.text for url in self.iterfind('./{0}location/{0}url'.format(mods)) if purl.search(url.text)]

    # def rights(self, elem=None):
    #     """
    #     Access mods:rights[type="use and reproduction|useAndReproduction" and return a dict:
    #     return: {'text': elementText, 'URI': rightsURI}
    #     """
    #     pass
    #
    # def _subject_parser_(subject):
    #     pass
    #
    # def subject(self, elem=None):
    #     """
    #     Access mods:subject elements and returns a list of dicts:
    #     return: [{'authority': , 'authorityURI': , 'valueURI': , children: {'type': child element name, 'term': text value}}, ... ]
    #     """
    #     pass

    # def _subject_text_(subject):
    #     pass
    #
    # def subject_constructor(self, elem=None):
    #     """
    #     Access mods:subject elements and parses text values into LOC double hyphenated complex headings
    #     return: A list of strings
    #     """
    #     pass

    @property
    def type_of_resource(self):
        """
        Access mods:typeOfResource and return text value:
        :return: text value or None
        """
        try:
            return self.find('./{0}typeOfResource'.format(mods)).text
        except AttributeError:
            return None

    def _format_titles(self, non_sort, title, subtitle):
        """Construct valid title regardless if any constituent part missing."""
        return '{non_sort}{title}{subtitle}'.format(
            non_sort=non_sort+' ' if non_sort else '',
            title=title if title else '',
            subtitle=': '+subtitle if subtitle else '')

    def _get_dates(self, elem):
        return [date for date in elem.find('./{0}originInfo'.format(mods)).iterchildren()
                if date.tag in DATE_FIELDS]

    def _get_text(self, elem):
        """Wrapping common use of getattr for safe attribute access."""
        return getattr(elem, 'text', None)

    def _identifier(self, id_type=None):
        """

        :return:
        """
        if id_type:
            return [Identifier(identifier.text, id_type)
                    for identifier in self.iterfind('.//{0}identifier'.format(mods)) if
                    identifier.attrib.get('type') == id_type]
        else:
            return [Identifier(identifier.text, identifier.attrib.get('type'))
                    for identifier in self.iterfind('.//{0}identifier'.format(mods))]

    def _title_constructor(self, elem):
        """
        :param elem: The element containing title information
        :return: A list of correctly formatted titles
        """
        return [self._format_titles(
            self._get_text(title.find('./{0}nonSort'.format(mods))),
            self._get_text(title.find('./{0}title'.format(mods))),
            self._get_text(title.find('./{0}subTitle'.format(mods))))
                for title in elem.iterfind('./{0}titleInfo'.format(mods))]

    def _url(self, elem):
        return [url.text for url in elem.iterfind('./{0}location/{0}url'.format(mods))]


class OAIRecord(Record):

    def _init(self):
        super(OAIRecord, self)._init()

    @property
    def oai_urn(self):
        """
        :return: The OAI ID as a string
        """
        if '{http://repox.ist.utl.pt}' in self.tag:
            try:
                return self.attrib['id']
            except AttributeError:
                pass
        elif '{http://www.openarchives.org/OAI/2.0/oai_dc/}' in self.tag:
            try:
                return self.find('{0}header/{0}identifier'.format(NAMESPACES['oai_dc'])).text
            except AttributeError:
                pass
        else:
            try:
                return self.find('{}header/{}identifier').text
            except AttributeError:
                pass
