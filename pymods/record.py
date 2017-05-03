from lxml import etree
from pymods.constants import NAMESPACES


class Record(etree.ElementBase):

    def _init(self):
        super(Record, self)._init()


class MODSRecord(Record):

    def _init(self):
        super(MODSRecord, self)._init()

    def abstract(self, elem=None):
        """
        Access mods:abstract elements and return a list of dicts:
        return: [{abstract displayLabel: abstract text}] or None.
        """
        pass

    def classification(self, elem=None):
        """
        Access mods:classification element:
        return: [classification text, ... ] or None
        """
        pass

    def collection(self, elem=None):
        """
        Retrieve archival collection metadata from mods:relatedItem[type="host"]:
        return: {'location': collection location, 'title': collection title, 'url': link to collection (if found)}
        """
        pass

    def date_constructor(self, elem=None):
        """
        Accesses mods:dateIssued, mods:dateCreated, mods:copyrightDate, and mods:dateOther underneath mods:originInfo. Other date-type elements are ignored:
        return: A date containing string or None.
        """
        pass

    def digital_origin(self, elem=None):
        """
        Accesses mods:digitalOrigin element:
        return: element text or None.
        """
        pass

    def doi_search(self, elem=None):
        """
        Retrieve DOI:
        return: item's DOI.
        """
        pass

    def edition(self, elem=None):
        """
        Accesses mods:edition element:
        return: element text or None.
        """
        pass

    def extent(self, elem=None):
        """
        Accesses mods:extent element:
        return: list of mods:extent texts or None.
        """
        pass

    def form(self, elem=None):
        """
        Accesses mods:physicalDescription/mods:form element:
        return: list of mods:form texts or None.
        """
        pass

    def genre(self, elem=None):
        """
        Accesses mods:genre element:
        return: [ { 'term': , 'authority': , 'authorityURI': , 'valueURI': }, ] or None.
        """
        pass

    def geographic_code(self, elem=None):
        """
        Accesses mods:geographicCode element:
        return: list of mods:geographicCode texts or None.
        """
        pass

    def issuance(self, elem=None):
        """
        Accesses mods:issuance element:
        return: list of mods:issuance texts or None.
        """
        pass

    def language(self, elem=None):
        """
        Accesses mods:languageterm elements:
        :return: list of of dicts [{term-type: term}] or None.
        """
        pass

    def local_identifier(self, elem=None, type='IID'):
        """
        Get DigiNole IID from MODS record:
        return: item's IID.
        """
        pass

    def _nameGen_(names, full_name):
        """
        
        :param full_name: 
        :return: 
        """
        pass

    def name_constructor(self, elem=None):
        """
        Accesses mods:name/mods:namePart elements and reconstructs names into LOC order:
        return: a list of strings.
        """
        pass

    def note(self, elem=None):
        """
        Access mods:note elements and return a list of dicts:
        return: [{note-type: note-text}, untyped-note-text]
        """
        pass

    def physical_description_note(self, elem=None):
        """
        Access mods:physicalDescription/mods:note elements and return a list of text values:
        return: list of note text values.
        """
        pass

    def physical_location(self, elem=None):
        """
        Access mods:mods/mods:location/mods:physicalLocation and return text values.
        return: list of element text values.
        """
        pass

    def pid_search(self, elem=None, prefix='fsu:'):
        """
        Get fedora PID from MODS record:
        return: item's fedora PID.
        """
        pass

    def publication_place(self, elem=None):
        """
        Access mods:place and return a list of dicts:
        return: [{termType: termText}, {'untyped': termText}, ...]
        """
        pass

    def publisher(self, elem=None):
        """
        Access mods:publisher and return a list of text values:
        return: [publisher, ...]
        """
        pass

    def purl_search(self, elem=None):
        """
        Accesses record's Persistent URL from mods:mods/mods:location/mods:url:
        return: item PURL as string.
        """
        purl = re.compile('((http://purl)[\w\d:#@%/;$()~_?\+-=\\\.&]+)')
        pass

    def rights(self, elem=None):
        """
        Access mods:rights[type="use and reproduction|useAndReproduction" and return a dict:
        return: {'text': elementText, 'URI': rightsURI}
        """
        pass

    def _subject_parser_(subject):
        pass

    def subject(self, elem=None):
        """
        Access mods:subject elements and returns a list of dicts:
        return: [{'authority': , 'authorityURI': , 'valueURI': , children: {'type': child element name, 'term': text value}}, ... ]
        """
        pass


    def _subject_text_(subject):
        pass

    def subject_constructor(self, elem=None):
        """
        Access mods:subject elements and parses text values into LOC double hyphenated complex headings
        return: A list of strings
        """
        pass

    def title_constructor(self, elem=None):
        """
        Accesses children of mods:titleInfo and return a list of titles in natural order:
        return: list of titles.
        """
        pass

    def type_of_resource(self, elem=None):
        """
        Access mods:typeOfResource and return text value:
        return: text value or None
        """
        pass


class OAIRecord(Record):

    def _init(self):
        super(OAIRecord, self)._init()

    @property
    def oai_urn(self):
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
