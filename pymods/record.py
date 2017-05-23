import re
import collections
from lxml import etree
from pymods.constants import NAMESPACES, DATE_FIELDS

Abstract = collections.namedtuple('Abstract', 'text type displayLabel')
Collection = collections.namedtuple('Collection', 'location title url')
Date = collections.namedtuple('Date', 'text type')
Genre = collections.namedtuple('Genre', 'text authority authorityURI valueURI')
Identifier = collections.namedtuple('Identifier', 'text type')
Language = collections.namedtuple('Language', 'text type authority')
Name = collections.namedtuple('Name', 'text type uri authority authorityURI role')  # MM
NamePart = collections.namedtuple('NamePart', 'text type')  # MM
# Name = collections.namedtuple('Name', 'name_parts roles type')  # EH
# NamePart = collections.namedtuple('NamePart', 'name type')  # EH
Note = collections.namedtuple('Note', 'text type displayLabel')
PublicationPlace = collections.namedtuple('PublicationPlace', 'text type')
Rights = collections.namedtuple('Rights', 'text type uri')
Role = collections.namedtuple('Role', 'text type')
Subject = collections.namedtuple('Subject', 'text uri authority authorityURI')
SubjectPart = collections.namedtuple('SubjectPart', 'text type')
mods = NAMESPACES['mods']

# TODO - pub. place


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

    @property
    def collection(self):
        """
        Retrieve archival collection metadata from mods:relatedItem[type="host"]:
        :return: A Collection element with location, title, and url attributes
        """
        try:
            related_item = self.findall('./{0}relatedItem[@type="host"]'.format(mods))[0]
            coll_location, coll_title, coll_url = None, None, None

            try:
                coll_location = self._physical_location(related_item)[0]
            except IndexError:
                pass

            try:
                coll_title = self._title_constructor(related_item)[0]
            except IndexError:
                pass

            try:
                coll_url = self._url(related_item)[0]
            except IndexError:
                pass

            return Collection(coll_location, coll_title, coll_url)

        except IndexError:
            return None

    # def date_constructor(self, elem=None):
    #     """
    #     Accesses mods:dateIssued, mods:dateCreated, mods:copyrightDate, and mods:dateOther underneath mods:originInfo. Other date-type elements are ignored:
    #     return: A date containing string or None.
    #     """
    #     pass

    @property
    def dates(self):
        """
        
        :return: List of date elements with text and type attributes.
        """
        try:
            return [Date(self._date_text(date_pair)[0], self._date_text(date_pair)[1])
                    for date_pair in self._date_collector(self.find('./{0}originInfo'.format(mods)))]
        except TypeError:
            return None

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
        try:
            return self._identifier(id_type='DOI')[0].text
        except IndexError:
            return None

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
    def get_corp_names(self):  # EH
        return sorted([name for name in self.get_names(type='corporate')])

    @property
    def get_creators(self):
        return sorted([name for name in self.get_names(role='Creator')])  # TODO: this needs to flexible to code='cre'

    def get_names(self, **kwargs):
        """

        :param kwargs: 
        :return: 
        """
        if 'type' in kwargs.keys():
            return [name for name in self.names if name.type == kwargs['type']]
        elif 'authority' in kwargs.keys():
            return [name for name in self.names if name.authority == kwargs['authority']]
        elif 'role' in kwargs.keys():  # TODO
            return [name for name in self.names for role in name.role if role.text == kwargs['role']]
        else:
            raise TypeError  # TODO: find proper error to raise

        # return [name for name in self.names if name.type == kwargs['type']]

    def get_notes(self, **kwargs):
        """
        
        :param kwargs: 
        :return: 
        """
        if 'type' in kwargs.keys():
            return [note for note in self.note if note.type == kwargs['type']]
        elif 'displayLabel' in kwargs.keys():
            return [note for note in self.note if note.displayLabel == kwargs['displayLabel']]
        else:
            return self.note

    @property
    def get_pers_names(self):  # EH
        return sorted([name for name in self.get_names(type='personal')])

    @property
    def identifiers(self):
        """

        :return:
        """
        return self._identifier()

    @property
    def iid(self):
        """
        
        :return: 
        """
        try:
            return self._identifier(id_type='IID')[0].text
        except IndexError:
            return None

    @property
    def issuance(self):
        """
        Accesses mods:issuance element:
        return: list of mods:issuance texts.
        """
        return [issuance.text for issuance in self.iterfind('.//{0}issuance'.format(mods))]

    @property
    def language(self):
        """
        Accesses mods:languageterm elements:
        :return: A list of Language elements with text, type, and authority attributes
        """
        return [Language(term.text,
                         term.attrib.get('type'),
                         term.attrib.get('authority'))
                for language in self.iterfind('{0}language'.format(mods))
                for term in language.iterfind('{0}languageTerm'.format(mods))]

    @property
    def names(self):
        """

        :return: A list of Name elements with text, uri, authority, and authorityURI attributes
        """
        return [Name(name._name_text(),
                     name.attrib.get('type'),
                     name.attrib.get('valueURI'),
                     name.attrib.get('authority'),
                     name.attrib.get('authorityURI'),
                     name._name_role())
                for name in self.iterfind('./{0}name'.format(mods))]

    @property
    def name_parts(self):
        """
        
        :return: 
        """
        return NotImplemented
        # TODO: return unformatted name parts for transformation scenarios

    @property
    def note(self):
        """
        Access mods:note elements and return a list of dicts:
        :return: A list containing Note elements with text, type, and displayLabel attributes
        """
        return [Note(note.text, note.attrib.get('type'), note.attrib.get('displayLabel'))
                for note in self.iterfind('./{0}note'.format(mods))]

    # @property  # EH
    # def personal_names(self):
    #     return sorted([self._name_text(name) for name in self.get_names()
    #                    if name.type == 'personal'])

    @property
    def physical_description_note(self):
        """
        Access mods:physicalDescription/mods:note elements and return a list of text values:
        :return: list of note text values.
        """
        return [note.text for note in self.findall('./{0}physicalDescription/{0}note'.format(mods))]

    @property
    def physical_location(self):
        """
        Access mods:mods/mods:location/mods:physicalLocation and return text values.
        :return: list of element text values.
        """
        return self._physical_location()

    @property
    def pid(self):
        """
        Get fedora PID from MODS record:
        return: item's fedora PID.
        """
        try:
            return self._identifier(id_type='fedora')[0].text
        except IndexError:
            return None

    # def publication_place(self, elem=None):
    #     """
    #     Access mods:place and return a list of dicts:
    #     :return: [{termType: termText}, {'untyped': termText}, ...]
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

    @property
    def rights(self):
        """
        Access mods:rights[type="use and reproduction|useAndReproduction" and return a dict:
        :return: A list containing Rights elements with text, type, and uri
        """
        return [Rights(rights.text,
                       rights.attrib.get('type'),
                       rights.attrib.get('{http://www.w3.org/1999/xlink}href'))
                for rights in self.iterfind('{0}accessCondition'.format(mods))]

    @property
    def subjects(self):
        """
        
        :return: list of Subject elements with text, uri, authority and authorityURI values.
        """
        return [Subject(subject._subject_text(),
                        subject.attrib.get('valueURI'),
                        subject.attrib.get('authority'),
                        subject.attrib.get('authorityURI'))
                for subject in self.iterfind('{0}subject'.format(mods))
                if 'geographicCode' not in subject[0].tag]

    @property
    def subject_parts(self):
        """
        
        :return: 
        """
        return NotImplemented
        # TODO: return unformatted subject parts for transformation scenarios

    @property
    def titles(self):
        """
        
        :return: 
        """
        return [title for title in self._title_constructor()]

    @property
    def title_parts(self):
        """
        
        :return: 
        """
        return NotImplemented

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

    # def _format_name(self, name):  # EH
    #     """
    #
    #
    #     :param name: A Name element
    #     :return: A string formatted according to LOC conventions
    #     """
    #     family = ', '.join(x.name for x in name.name_parts
    #                        if x.type == 'family')
    #     given = ', '.join(x.name for x in name.name_parts
    #                       if x.type == 'given' or x.type is None)
    #     terms_of_address = ', '.join(x.name for x in name.name_parts
    #                                  if x.type == 'termsOfAddress')
    #     date = ', '.join(x.name for x in name.name_parts
    #                      if x.type == 'date')
    #     return '{family}{given}{termsOfAddress}{date}'.format(
    #         family=family + ', ' if family else '',
    #         given=given if given else '',
    #         termsOfAddress=', ' + terms_of_address if terms_of_address else '',
    #         date=', ' + date if date else ''
    #     )

    def _date_collector(self, elem):
        for tag in DATE_FIELDS:
            try:
                if elem.find('./{0}'.format(tag)) is not None:
                    return [elem.findall('./{0}'.format(tag))]
            except AttributeError:
                pass

    def _date_text(self, date_pair):
        if len(date_pair) == 1:
            return date_pair[0].text, date_pair[0].tag
        elif len(date_pair) == 2:
            date_list = sorted([date.text for date in date_pair])
            return '{0} - {1}'.format(date_list[0], date_list[1]), date_pair[0].tag

    def _get_dates(self, elem):  # EH
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

    # def _make_name_parts(self, el):  # EH
    #     return [NamePart(name.text, name.attrib.get('type')) for name in
    #             el.iterfind('./{0}namePart'.format(mods))]

    def _name_part(self, elem=None):  # MM
        """

        :param elem:
        :return: namePart text and type
        """
        if elem is None:
            elem = self
        return [NamePart(name.text, name.attrib.get('type')) for name in
                elem.iterfind('./{0}namePart'.format(mods))]

    def _name_role(self, elem=None):  # EH
        """
        
        :param elem: 
        :return: 
        """
        if elem is None:
            elem = self
        return [Role(name.text, name.attrib.get('type')) for name in
                elem.iterfind('./{0}role/{0}roleTerm'.format(mods))]

    def _name_text(self, elem=None):  # MM
        """

        :param elem:
        :return:
        """
        if elem is None:
            elem = self
        if elem.attrib.get('type') == 'personal':
            family = ', '.join(x.text for x in elem._name_part() if x.type == 'family')
            given = ', '.join(x.text for x in elem._name_part() if x.type == 'given')
            terms_of_address = ', '.join(x.text for x in elem._name_part() if x.type == 'termsOfAddress')
            date = ', '.join(x.text for x in elem._name_part() if x.type == 'date')
            return '{family}{given}{termsOfAddress}{date}'.format(
                family=family + ', ' if family else '',
                given=given if given else '',
                termsOfAddress=', ' + terms_of_address if terms_of_address else '',
                date=', ' + date if date else ''
            )
        else:
            text = ''
            for part in elem.iter(tag='{0}namePart'.format(mods)):
                text = text + '{0}, '.format(part.text)
            return text.strip(', ')

    def _physical_location(self, elem=None):
        """
        Access mods:mods/mods:location/mods:physicalLocation and return text values.
        return: list of element text values.
        """
        if elem is None:
            elem = self
        return [location.text for location in elem.iterfind('./{0}location/{0}physicalLocation'.format(mods))]

    def _subject_part(self, elem=None):
        """
        
        :param elem: 
        :return: list of SubjectPart elements with text and type values.
        """
        if elem is None:
            elem = self
        return [SubjectPart(term.text,
                            term.tag)
                for term in elem.iterchildren()]

    def _subject_text(self):
        subject_text = ''
        if 'name' not in self[0].tag:
            for subject_part in self._subject_part():
                subject_text = subject_text + '{0}--'.format(subject_part.text)
            return subject_text.strip('--')
        else:
            return self.names[0].text

    def _title_constructor(self, elem=None): # TODO - name title stuff to match name&subject methods
        """
        :param elem: The element containing title information
        :return: A list of correctly formatted titles
        """
        if elem is None:
            elem = self
        return [self._title_text(
            self._get_text(title.find('./{0}nonSort'.format(mods))),
            self._get_text(title.find('./{0}title'.format(mods))),
            self._get_text(title.find('./{0}subTitle'.format(mods))))
                for title in elem.iterfind('./{0}titleInfo'.format(mods))]

    def _title_text(self, non_sort, title, subtitle):
        """Construct valid title regardless if any constituent part missing."""
        return '{non_sort}{title}{subtitle}'.format(
            non_sort=non_sort+' ' if non_sort else '',
            title=title if title else '',
            subtitle=': '+subtitle if subtitle else '')

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
