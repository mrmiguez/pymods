import collections
import re

from lxml import etree

from pymods.constants import NAMESPACES, DATE_FIELDS

__pdoc__ = {}  # for pdoc documentation - http://pdoc.burntsushi.net/pdoc

Abstract = collections.namedtuple('Abstract', 'text type displayLabel elem')
# helper statements for pdoc documentation - http://pdoc.burntsushi.net/pdoc
__pdoc__['Abstract.text'] = 'Abstract elem text value.'
__pdoc__['Abstract.type'] = 'Value of elem@type attribute.'
__pdoc__['Abstract.displayLabel'] = 'Value of elem@displayLabel attribute.'
__pdoc__['Abstract.elem'] = 'lxml.etree.Element.'

Collection = collections.namedtuple('Collection', 'location title url elem')
__pdoc__['Collection'] = 'Tuple container for archival collection information.'
__pdoc__['Collection.location'] = 'Collection location (relatedItem[@type="host"]/location/physicalLocation).'
__pdoc__['Collection.title'] = 'Collection title (relatedItem[@type="host"]/titleInfo).'
__pdoc__[
    'Collection.url'] = 'Value of relatedItem[@type="host"]/location/url, which for local practice is a link to the finding aid.'
__pdoc__['Collection.elem'] = 'lxml.etree.Element.'

Date = collections.namedtuple('Date', 'text type elem')
__pdoc__['Date.text'] = 'Date elem text value. Potentially reformatted if a date range.'
__pdoc__['Date.type'] = 'Date elem type.'
__pdoc__['Date.elem'] = 'lxml.etree.Elements.'

Genre = collections.namedtuple('Genre', 'text uri authority authorityURI elem')
__pdoc__['Genre.text'] = 'Genre elem text value.'
__pdoc__['Genre.uri'] = 'Value of elem@valueURI attribute.'
__pdoc__['Genre.authority'] = 'Value of elem@authority attribute.'
__pdoc__['Genre.authorityURI'] = 'Value of elem@authorityURI attribute.'
__pdoc__['Genre.elem'] = 'lxml.etree.Element.'

Identifier = collections.namedtuple('Identifier', 'text type elem')
__pdoc__['Identifier.text'] = 'Identifier elem text value.'
__pdoc__['Identifier.type'] = 'Value of elem@type attribute.'
__pdoc__['Identifier.elem'] = 'lxml.etree.Element.'

Language = collections.namedtuple('Language', 'text code authority elem')
__pdoc__['Language.text'] = 'Language elem[@type="text"] value.'
__pdoc__['Language.code'] = 'Language elem[@type="code"] value.'
__pdoc__['Language.authority'] = 'Value of elem@authority attribute.'
__pdoc__['Language.elem'] = 'lxml.etree.Element.'

Name = collections.namedtuple('Name', 'text type uri authority authorityURI role elem')
__pdoc__['Name.text'] = 'Name elem text value.'
__pdoc__['Name.type'] = 'Value of elem@type attribute.'
__pdoc__['Name.uri'] = 'Value of elem@valueURI attribute.'
__pdoc__['Name.authority'] = 'Value of elem@authority attribute.'
__pdoc__['Name.authorityURI'] = 'Value of elem@authorityURI attribute.'
__pdoc__['Name.role'] = 'Role tuple generated from the values in elem/role/roleTerm'
__pdoc__['Name.elem'] = 'lxml.etree.Element.'

NamePart = collections.namedtuple('NamePart', 'text type elem')
__pdoc__['NamePart'] = 'Used internally to reformat name texts.'

Note = collections.namedtuple('Note', 'text type displayLabel elem')
__pdoc__['Note.text'] = 'Note elem text value.'
__pdoc__['Note.type'] = 'Value of elem@type attribute.'
__pdoc__['Note.displayLabel'] = 'Value of elem@displayLabel attribute.'
__pdoc__['Note.elem'] = 'lxml.etree.Element.'

PublicationPlace = collections.namedtuple('PublicationPlace', 'text type elem')
__pdoc__['PublicationPlace.text'] = 'Publication place elem text value.'
__pdoc__['PublicationPlace.type'] = 'Value of elem@type attribute.'
__pdoc__['PublicationPlace.elem'] = 'lxml.etree.Element.'

Rights = collections.namedtuple('Rights', 'text type uri elem')
__pdoc__['Rights.text'] = 'Rights elem text value.'
__pdoc__['Rights.type'] = 'Value of elem@type attribute.'
__pdoc__[
    'Rights.uri'] = "Value of elem@xlink:href attribute. Local practice is to store rightsstaments.org URI's in this attribute."
__pdoc__['Rights.elem'] = 'lxml.etree.Element.'

Role = collections.namedtuple('Role', 'text code authority elem')
__pdoc__['Role.text'] = 'Role elem[@type="text"] value.'
__pdoc__['Role.code'] = 'Role elem[@type="code"] value.'
__pdoc__['Role.authority'] = 'Value of elem@authority attribute.'
__pdoc__['Role.elem'] = 'lxml.etree.Element.'

Subject = collections.namedtuple('Subject', 'text uri authority authorityURI elem')
__pdoc__['Subject.text'] = 'Text values of children of Subject elem. Potentially reformatted into LCSH order.'
__pdoc__['Subject.uri'] = 'Value of elem@valueURI attribute.'
__pdoc__['Subject.authority'] = 'Value of elem@authority attribute.'
__pdoc__['Subject.authorityURI'] = 'Value of elem@authorityURI attribute.'
__pdoc__['Subject.elem'] = 'lxml.etree.Element.'

SubjectPart = collections.namedtuple('SubjectPart', 'text type elem')
__pdoc__['SubjectPart'] = 'Used internally to reformat subject texts.'

# Making life easier
mods = NAMESPACES['mods']


class Record(etree.ElementBase):
    """
    Base record class. Subclass of etree.ElementBase.
    """

    def _init(self):
        super(Record, self)._init()


class MODSRecord(Record):
    """
    Class for retrieving information from documents using the
    MODSXML standard (http://www.loc.gov/standards/mods).

    Most element structures are supported. Data is returned mostly
    as lists of strings or lists of named tuples. When possible
    data is parsed from element parts and returned in typical
    LOC ordered strings:

    * {family name}, {given name}, {dates} for names.
    * {non-sort character} {title}: {subtitle} for titles.
    """

    def _init(self):
        super(MODSRecord, self)._init()

    @property
    def abstract(self):
        """
        Pull information from mods:abstract element(s).

        :return: A list of Abstract elements with text, type, and displayLabel attributes.
        """
        return [Abstract(getattr(abstract, 'text', ''),
                         abstract.attrib.get('type'),
                         abstract.attrib.get('displayLabel'),
                         abstract)
                for abstract in self.iterfind('./{0}abstract'.format(mods))]

    @property
    def classification(self):
        """
        Pull information from mods:classification element(s).

        :return: A list of text from classification element(s).
        """
        return [classification.text
                for classification in self.iterfind('./{0}classification'.format(mods))]

    @property
    def collection(self):
        """
        Retrieve archival collection metadata from mods:relatedItem[type="host"].

        :return: A Collection element with location, title, and url attributes.
        """
        try:
            related_item = self.findall('./{0}relatedItem[@type="host"]'.format(mods))[0]
            coll_location, coll_title, coll_url = None, None, None

            try:
                coll_location = self._physical_location(related_item)[0]
            except IndexError:
                pass

            try:
                coll_title = self._title_part(related_item)[0]
            except IndexError:
                pass

            try:
                coll_url = self._url(related_item)[0]
            except IndexError:
                pass

            return Collection(coll_location, coll_title, coll_url, related_item)

        except IndexError:
            return None

    @property
    def dates(self):
        """
        Constructs dates from dateIssued, dateCreated, copyrightDate, and dateOther elements.

        :return: List of Date elements with text and type attributes.
        """
        try:
            return [Date(self._date_text(date_pair)[0], self._date_text(date_pair)[1], date_pair)
                    for date_pair in self._date_collector(self.find('./{0}originInfo'.format(mods)))]
        except TypeError:
            return None

    @property
    def digital_origin(self):
        """
        Get text from mods:edition element.

        :return: String containing digital origin information.
        """
        try:
            return self.find('.//{0}digitalOrigin'.format(mods)).text
        except AttributeError:
            return None

    @property
    def doi(self):
        """
        :return: Item's DOI or None.
        """
        try:
            return self._identifier(id_type='DOI')[0].text
        except IndexError:
            return None

    @property
    def edition(self):
        """
        Accesses mods:edition element.

        :return: Edition element text or None.
        """
        try:
            return self.find('.//{0}edition'.format(mods)).text
        except AttributeError:
            return None

    @property
    def extent(self):
        """
        Accesses mods:extent element.

        :return: A list of mods:extent texts.
        """
        return [extent.text for extent in self.iterfind('.//{0}extent'.format(mods))]

    @property
    def form(self):
        """
        Accesses mods:physicalDescription/mods:form element.

        :return: A list of mods:form texts.
        """
        return [form.text for form in self.iterfind('./{0}physicalDescription/{0}form'.format(mods))]

    @property
    def genre(self):
        """
        Accesses mods:genre element.

        :return: A list containing Genre elements with term, uri, authority,
            and authorityURI attributes.
        """
        return [Genre(genre.text,
                      genre.attrib.get('valueURI'),
                      genre.attrib.get('authority'),
                      genre.attrib.get('authorityURI'),
                      genre)
                for genre in self.iterfind('./{0}genre'.format(mods))]

    @property
    def geographic_code(self):
        """
        Accesses mods:geographicCode element.

        :return: A list of mods:geographicCode texts.
        """
        return [geocode.text for geocode in self.iterfind('./{0}subject/{0}geographicCode'.format(mods))]

    @property
    def get_corp_names(self):
        """
        Separates corporate names from other name types.

        :return: A list of corporate names.
        """
        return sorted([name for name in self.get_names(type='corporate')])

    @property
    def get_creators(self):
        """
        Separates creator names from other name roles.

        :return: A list of creator names.
        """
        return sorted([name for name in self.get_names(role='Creator')])  # TODO: this needs to flexible to code='cre'

    def get_names(self, **kwargs):
        """
        A customizable name query service. Subsets of all record names can be identified by 
        type ('personal', 'corporate', etc.), name authority, or role. 

        :param kwargs: A key, value pair of type="*", authority="*", or role="*".
        :return: A list of names matching query.
        """
        if 'type' in kwargs.keys():
            return [name for name in self.names if name.type == kwargs['type']]
        elif 'authority' in kwargs.keys():
            return [name for name in self.names if name.authority == kwargs['authority']]
        elif 'role' in kwargs.keys():
            return [name for name in self.names if name.role.text == kwargs['role']]
        else:
            raise KeyError

    def get_notes(self, **kwargs):
        """
        A customizable name query service. Subsets of all record notes can be identified by 
        type or displayLabel.

        :param kwargs: A key, value pair of type="*" or displayLabel="*".
        :return: A list of notes matching query.
        """
        if 'type' in kwargs.keys():
            return [note for note in self.note if note.type == kwargs['type']]
        elif 'displayLabel' in kwargs.keys():
            return [note for note in self.note if note.displayLabel == kwargs['displayLabel']]
        else:
            raise KeyError

    @property
    def get_pers_names(self):
        """
        Separates personal names from other name types.

        :return: A list of personal names.
        """
        return sorted([name for name in self.get_names(type='personal')])

    @property
    def identifiers(self):
        """
        Accesses mods:identifier elements.

        :return: A list of identifiers.
        """
        return self._identifier()

    @property
    def iid(self):
        """
        A custom FSU identifier service.

        :return: Item's IID or None.
        """
        try:
            return self._identifier(id_type='IID')[0].text
        except IndexError:
            return None

    @property
    def internet_media_type(self):
        """
        Accesses mods:physicalDescription/mods:internetMediaType element.

        :return: A list of mods:internetMediaType texts.
        """
        return [mime_type.text for mime_type in
                self.iterfind('./{0}physicalDescription/{0}internetMediaType'.format(mods))]

    @property
    def issuance(self):
        """
        Accesses mods:issuance element.

        :return: List of mods:issuance texts.
        """
        return [issuance.text for issuance in self.iterfind('.//{0}issuance'.format(mods))]

    @property
    def language(self):
        """
        Accesses mods:languageTerm elements.

        :return: A list of Language elements with text, code, and authority attributes.
        """
        return [Language(language.find('./{0}languageTerm[@type="text"]'.format(mods)).text,
                         language.find('./{0}languageTerm[@type="code"]'.format(mods)).text,
                         language.find('./{0}languageTerm[@type="text"]'.format(mods)).attrib.get('authority'),
                         language)
                if len(language) > 1
                else Language(None,
                              language.find('./{0}languageTerm'.format(mods)).text,
                              language.find('./{0}languageTerm'.format(mods)).attrib.get('authority'),
                              language)
        if language.find('./{0}languageTerm'.format(mods)).text.islower()
        else Language(language.find('./{0}languageTerm'.format(mods)).text,
                      None,
                      language.find('./{0}languageTerm'.format(mods)).attrib.get('authority'),
                      language)
                for language in self.iterfind('{0}language'.format(mods))]

    @property
    def names(self):
        """
        General mods:name service.

        :return: A list of Name elements with text, uri, authority, and authorityURI attributes.
        """
        return [Name(name._name_text(),
                     name.attrib.get('type'),
                     name.attrib.get('valueURI'),
                     name.attrib.get('authority'),
                     name.attrib.get('authorityURI'),
                     name._name_role(),
                     name)
                for name in self.iterfind('./{0}name'.format(mods))]

    @property
    def name_parts(self):
        """
        Not currently implemented.

        :return:
        """
        return NotImplemented
        # TODO: return unformatted name parts for transformation scenarios

    @property
    def note(self):
        """
        Access mods:note elements.

        :return: A list containing Note elements with text, type, and displayLabel attributes.
        """
        return [Note(note.text, note.attrib.get('type'), note.attrib.get('displayLabel'), note)
                for note in self.iterfind('./{0}note'.format(mods))]

    @property
    def physical_description_note(self):
        """
        Access mods:physicalDescription/mods:note elements and return a list of text values.

        :return: A list of note text values.
        """
        return [note.text for note in self.findall('./{0}physicalDescription/{0}note'.format(mods))]

    @property
    def physical_location(self):
        """
        Access mods:mods/mods:location/mods:physicalLocation and return text values.

        :return: A list of element text values.
        """
        return self._physical_location()

    @property
    def pid(self):
        """
        Get fedora PID from MODS record.

        :return: Item's fedora PID or None.
        """
        try:
            return self._identifier(id_type='fedora')[0].text
        except IndexError:
            return None

    @property
    def publication_place(self):
        """
        Accesses mods:originInfo/mods:place elements.

        :return: A list of PublicationPlace elements with text and type attributes.
        """
        return [PublicationPlace(place.text, place.attrib.get('type'), place)
                for place in self.iterfind('./{0}originInfo/{0}place/{0}placeTerm'.format(mods))]

    @property
    def publisher(self):
        """
        Accesses mods:publisher elements.

        :return: A list of element text values.
        """
        return [publisher.text for publisher in
                self.findall('./{0}originInfo/{0}publisher'.format(mods))]

    @property
    def purl(self):
        """
        Retrieves record's Persistent URL from mods:mods/mods:location/mods:url.

        :return: List of strings.
        """
        purl = re.compile('((http://purl)[\w\d:#@%/;$()~_?\+-=\\\.&]+)')
        return [url.text for url in self.iterfind('./{0}location/{0}url'.format(mods)) if purl.search(url.text)]

    @property
    def rights(self):
        """
        Access mods:accessCondition and return values.

        :return: A list containing Rights elements with text, type, and uri.
        """
        return [Rights(rights.text,
                       rights.attrib.get('type'),
                       rights.attrib.get('{http://www.w3.org/1999/xlink}href'),
                       rights)
                for rights in self.iterfind('{0}accessCondition'.format(mods))]

    @property
    def subjects(self):
        """
        General subject retrieval service.

        :return: list of Subject elements with text, uri, authority and authorityURI values.
        """
        return [Subject(subject._subject_text(),
                        subject[0].attrib.get('valueURI'),
                        subject.attrib.get('authority'),
                        subject.attrib.get('authorityURI'),
                        subject)
                if subject.attrib.get('valueURI') is None
                else Subject(subject._subject_text(),
                             subject.attrib.get('valueURI'),
                             subject.attrib.get('authority'),
                             subject.attrib.get('authorityURI'),
                             subject)
                for subject in self.iterfind('{0}subject'.format(mods))
                if 'geographicCode' not in subject[0].tag]

    @property
    def subject_parts(self):
        """
        Not currently implemented.

        :return:
        """
        return NotImplemented
        # TODO: return unformatted subject parts for transformation scenarios

    @property
    def table_of_contents(self):
        try:        
            return [toc.text for toc in self.iterfind('{0}tableOfContents'.format(mods))]
        except AttributeError:
            return None

    @property
    def titles(self):
        """
        General title retrieval service.

        :return: A list of title texts.
        """
        return [title for title in self._title_part()]

    @property
    def title_parts(self):
        """
        Not currently implemented.

        :return:
        """
        return NotImplemented
        # TODO: return unformatted title parts for transformation scenarios

    @property
    def type_of_resource(self):
        """
        Access mods:typeOfResource and return text value.

        :return: Text value or None.
        """
        try:
            return self.find('./{0}typeOfResource'.format(mods)).text
        except AttributeError:
            return None

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

    def _get_dates(self, elem):
        return [date for date in elem.find('./{0}originInfo'.format(mods)).iterchildren()
                if date.tag in DATE_FIELDS]

    def _get_text(self, elem):
        """Wrapping common use of getattr for safe attribute access."""
        return getattr(elem, 'text', None)

    def _identifier(self, id_type=None):
        """
        :param id_type: A MODSXML @type='id_type' attribute value.
        :return: A list of Identifier elements with text and type attributes.
        """
        if id_type:
            return [Identifier(identifier.text, id_type, identifier)
                    for identifier in self.iterfind('.//{0}identifier'.format(mods)) if
                    identifier.attrib.get('type') == id_type]
        else:
            return [Identifier(identifier.text, identifier.attrib.get('type'), identifier)
                    for identifier in self.iterfind('.//{0}identifier'.format(mods))]

    def _name_part(self, elem=None):
        if elem is None:
            elem = self
        return [NamePart(name.text, name.attrib.get('type'), name) for name in
                elem.iterfind('./{0}namePart'.format(mods))]

    def _name_role(self, elem=None):
        if elem is None:
            elem = self
        return Role(elem._name_role_text(), elem._name_role_code(), elem._name_role_authority(), elem)

    def _name_role_authority(self):
        try:
            return self.find('.//{0}roleTerm'.format(mods)).attrib.get('authority')
        except AttributeError:
            return None

    def _name_role_code(self):
        try:
            return self.find('.//{0}roleTerm[@type="code"]'.format(mods)).text
        except AttributeError:
            return None

    def _name_role_text(self):
        try:
            return self.find('.//{0}roleTerm[@type="text"]'.format(mods)).text
        except AttributeError:
            return None

    def _name_text(self, elem=None):
        if elem is None:
            elem = self
        if elem.attrib.get('type') == 'personal':
            family = ', '.join(x.text for x in elem._name_part() if x.type == 'family')
            given = ', '.join(x.text for x in elem._name_part() if x.type == 'given')
            terms_of_address = ', '.join(x.text for x in elem._name_part() if x.type == 'termsOfAddress')
            date = ', '.join(x.text for x in elem._name_part() if x.type == 'date')
            untyped_name = ', '.join(x.text for x in elem._name_part() if x.type is None)
            return '{family}{given}{termsOfAddress}{untyped_name}{date}'.format(
                family=family + ', ' if family else '',
                given=given if given else '',
                termsOfAddress=', ' + terms_of_address if terms_of_address else '',
                untyped_name=untyped_name if untyped_name else '',
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

        :return: A list of text values.
        """
        if elem is None:
            elem = self
        return [location.text for location in elem.iterfind('./{0}location/{0}physicalLocation'.format(mods))]

    def _subject_part(self, elem=None):
        if elem is None:
            elem = self
        return [SubjectPart(term._name_text(), term.tag, term)
                if 'name' in term.tag
                else SubjectPart(term.text, term.tag, term)
                for term in elem.iterchildren()]

    def _subject_text(self):
        subject_text = ''
        for subject_part in self._subject_part():
            subject_text = subject_text + '{0}--'.format(subject_part.text)
        return subject_text.strip('--')

    def _title_part(self, elem=None):  # TODO - name title stuff to match name&subject methods
        """
        :param elem: The element containing a mods:titleInfo elements (i.e. mods:mods or mods:relatedItem).
        :return: A list of correctly formatted titles.
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
            non_sort=non_sort + ' ' if non_sort else '',
            title=title if title else '',
            subtitle=': ' + subtitle if subtitle else '')

    def _url(self, elem):
        return [url.text for url in elem.iterfind('./{0}location/{0}url'.format(mods))]


class OAIRecord(Record):
    """
    Record class for records stored in the OAI-PMH format.
    OAI documents in either the OAI-PMH standard or
    repox export standard are supported.

    This class allows access to OAI wrapper data,
    such as the OAI record URN. The OAIRecord.metadata property
    allows access to the metadata content of the record.
    Standard methods from the MODSRecord and DCRecord classes
    can be performed on OAIRecord objects through the metadata
    property. Internal tests will automatically select the correct
    parser and class to return.
    """

    def _init(self):
        super(OAIRecord, self)._init()

    @property
    def oai_urn(self):
        """
        :return: The OAI ID as a string.
        """
        if '{http://repox.ist.utl.pt}' in self.tag:
            try:
                return self.attrib['id']
            except AttributeError:
                pass
        elif '{http://www.openarchives.org/OAI/2.0/}' in self.tag:
            try:
                return self.find('{0}header/{0}identifier'.format(NAMESPACES['oai_dc'])).text
            except AttributeError:
                pass
        else:
            try:
                return self.find('{}header/{}identifier').text
            except AttributeError:
                pass

    @property
    def metadata(self):
        """
        Exposes the metadata content of an OAIRecord.

        :return: A reparsed root element either in the MODSRecord or DCRecord class, as appropriate.
        """
        record_data = self.find('./{*}metadata')
        if record_data is not None:
            try:
                if 'mods' in record_data[0].tag:
                    mods_parser_registration = etree.ElementDefaultClassLookup(element=MODSRecord)
                    mods_parser = etree.XMLParser()
                    mods_parser.set_element_class_lookup(mods_parser_registration)
                    return etree.XML(etree.tostring(record_data[0], encoding='UTF-8').decode('utf-8'),
                                     parser=mods_parser)
                elif 'qualified' in record_data[0].tag:
                    qdc_parser_registration = etree.ElementDefaultClassLookup(element=DCRecord)
                    qdc_parser = etree.XMLParser()
                    qdc_parser.set_element_class_lookup(qdc_parser_registration)
                    return etree.XML(etree.tostring(record_data[0], encoding='UTF-8').decode('utf-8'),
                                     parser=qdc_parser)
                elif 'dc' in record_data[0].tag:
                    dc_parser_registration = etree.ElementDefaultClassLookup(element=DCRecord)
                    dc_parser = etree.XMLParser()
                    dc_parser.set_element_class_lookup(dc_parser_registration)
                    return etree.XML(etree.tostring(record_data[0], encoding='UTF-8').decode('utf-8'),
                                     parser=dc_parser)
            except IndexError:
                pass


class DCRecord(Record):
    """
    Record class for Dublin Core and Qualified Dublin Core elements.
    """

    def _init(self):
        super(DCRecord, self)._init()

    def get_element(self, elem, delimiter=None):
        """
        :param elem: An element. It can be named explicitly by namespace using Clark Notation,
            or using the form '{*}elem' will match elem in any namespace.
        :param delimiter: A character used to separate values within a single element.
        :return: A list of element values.
        """
        if self.find('{0}'.format(elem)) is not None:
            if delimiter is None:
                return [item.text for item in self.findall('{0}'.format(elem)) if item.text]
            else:
                return [split_text.strip()
                        for item in self.findall('{0}'.format(elem)) if item.text
                        for split_text in item.text.split(delimiter)]
