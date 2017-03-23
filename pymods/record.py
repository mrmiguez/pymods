from lxml import etree

from pymods.constants import NAMESPACES
from pymods.exceptions import ElementNotFound


class Record(etree.ElementBase):

    def _init(self):
        super(etree.ElementBase, self).__init__()
        return self

    def abstract(self, record):
        """
        Access mods:abstract elements and return a list of dicts:
        return: [{abstract displayLabel: abstract text}] or None.
        """
        self.record = record
        if self.record.find('./{0}abstract'.format(NAMESPACES['mods'])) is not None:
            self.all_abstracts = []
            for abstract in self.record.iterfind('./{0}abstract'.format(NAMESPACES['mods'])):
                if len(abstract.attrib) >= 1:
                    if 'type' in abstract.attrib.keys():
                        typed_abstract = {abstract.attrib['type']: abstract.text}
                        self.all_abstracts.append(typed_abstract)
                    elif 'displayLabel' in abstract.attrib.keys():
                        labeled_abstract = {abstract.attrib['displayLabel']: abstract.text}
                        self.all_abstracts.append(labeled_abstract)
                    else:
                        self.all_abstracts.append(abstract.text)
                else:
                    self.all_abstracts.append(abstract.text)
            return self.all_abstracts
        else:
            raise ElementNotFound

    def classification(self, record):
        """
        Access mods:classification element:
        return: [classification text, ... ] or None
        """
        self.record = record
        if self.record.find('./{0}classification'.format(NAMESPACES['mods'])) is not None:
            self.all_classifications = []
            for classification in self.record.iterfind('./{0}classification'.format(NAMESPACES['mods'])):
                self.all_classifications.append(classification.text)
            return self.all_classifications
        else:
            raise ElementNotFound

    def collection(self, record):
        """
        Retrieve archival collection metadata from mods:relatedItem[type="host"]:
        return: {'location': collection location, 'title': collection title, 'url': link to collection (if found)}
        """
        self.record = record
        if self.record.find('./{0}relatedItem'.format(NAMESPACES['mods'])) is not None:
            for related_item in self.record.iterfind('./{0}relatedItem'.format(NAMESPACES['mods'])):
                if 'type' in related_item.attrib.keys():
                    if 'host' == related_item.attrib['type']:
                        self.host_info = {}
                        if Record.title_constructor(related_item) is not None:
                            host_title = Record.title_constructor(related_item)[0]
                            self.host_info['title'] = host_title
                        if Record.physical_location(related_item) is not None:
                            host_location = Record.physical_location(related_item)[0]
                            self.host_info['location'] = host_location
                        if related_item.find('./{0}location/{0}url'.format(NAMESPACES['mods'])) is not None:
                            self.host_info['url'] = related_item.find(
                                './{0}location/{0}url'.format(NAMESPACES['mods'])).text
                        return self.host_info
                    else:
                        raise ElementNotFound

    def date_constructor(self, record):
        """
        Accesses mods:dateIssued, mods:dateCreated, mods:copyrightDate, and mods:dateOther underneath mods:originInfo. Other date-type elements are ignored:
        return: A date containing string or None.
        """
        self.record = record
        date_list = ['{0}dateIssued'.format(NAMESPACES['mods']),
                     '{0}dateCreated'.format(NAMESPACES['mods']),
                     '{0}copyrightDate'.format(NAMESPACES['mods']),
                     '{0}dateOther'.format(NAMESPACES['mods'])]
        ignore_list = ['{0}place'.format(NAMESPACES['mods']),
                       '{0}publisher'.format(NAMESPACES['mods']),
                       '{0}dateCaptured'.format(NAMESPACES['mods']),
                       '{0}dateValid'.format(NAMESPACES['mods']),
                       '{0}dateModified'.format(NAMESPACES['mods']),
                       '{0}edition'.format(NAMESPACES['mods']),
                       '{0}issuance'.format(NAMESPACES['mods']),
                       '{0}frequency'.format(NAMESPACES['mods'])]
        if self.record.find('./{0}originInfo'.format(NAMESPACES['mods'])) is not None:
            self.origin_info = self.record.find('./{0}originInfo'.format(NAMESPACES['mods']))
            self.date = None
            for child in self.origin_info.iterchildren():
                if child.tag in date_list:
                    # date range
                    if 'point' in child.attrib.keys():
                        if child.attrib['point'] == 'start':
                            if self.date is None:
                                self.date = child.text
                            else:
                                self.date = child.text + ' - ' + self.date
                        elif child.attrib['point'] == 'end':
                            if self.date is None:
                                self.date = child.text
                            else:
                                self.date = self.date + ' - ' + child.text
                    # single date
                    else:
                        self.date = child.text
                elif child.tag in ignore_list:
                    pass
            return self.date

    def digital_origin(self, record):
        """
        Accesses mods:digitalOrigin element:
        return: element text or None.
        """
        self.record = record
        if self.record.find('.//{0}digitalOrigin'.format(NAMESPACES['mods'])) is not None:
            return self.record.find('.//{0}digitalOrigin'.format(NAMESPACES['mods'])).text
        else:
            raise ElementNotFound

    def edition(self, record):
        """
        Accesses mods:edition element:
        return: element text or None.
        """
        self.record = record
        if self.record.find('.//{0}edition'.format(NAMESPACES['mods'])) is not None:
            return self.record.find('.//{0}edition'.format(NAMESPACES['mods'])).text
        else:
            raise ElementNotFound

    def extent(self, record):
        """
        Accesses mods:extent element:
        return: list of mods:extent texts or None.
        """
        self.record = record
        if self.record.find('.//{0}extent'.format(NAMESPACES['mods'])) is not None:
            self.all_extents = []
            for extent in self.record.iterfind('.//{0}extent'.format(NAMESPACES['mods'])):
                self.all_extents.append(extent.text)
            return self.all_extents
        else:
            raise ElementNotFound

    def form(self, record):
        """
        Accesses mods:physicalDescription/mods:form element:
        return: list of mods:form texts or None.
        """
        self.record = record
        if self.record.find('./{0}physicalDescription/{0}form'.format(NAMESPACES['mods'])) is not None:
            self.all_forms = []
            for form in self.record.iterfind('./{0}physicalDescription/{0}form'.format(NAMESPACES['mods'])):
                self.all_forms.append(form.text)
            return self.all_forms
        else:
            raise ElementNotFound

    def genre(self, record):
        """
        Accesses mods:genre element:
        return: [ { 'term': , 'authority': , 'authorityURI': , 'valueURI': }, ] or None.
        """
        self.record = record
        if self.record.find('./{0}genre'.format(NAMESPACES['mods'])) is not None:
            self.all_genres = []
            for genre in self.record.iterfind('./{0}genre'.format(NAMESPACES['mods'])):
                genre_elems = {}
                genre_elems['term'] = genre.text
                if 'authority' in genre.attrib.keys():
                    genre_elems['authority'] = genre.attrib['authority']
                if 'authorityURI' in genre.attrib.keys():
                    genre_elems['authorityURI'] = genre.attrib['authorityURI']
                if 'valueURI' in genre.attrib.keys():
                    genre_elems['valueURI'] = genre.attrib['valueURI']
                self.all_genres.append(genre_elems)
            return self.all_genres
        else:
            raise ElementNotFound

    def geographic_code(self, record):
        """
        Accesses mods:geographicCode element:
        return: list of mods:geographicCode texts or None.
        """
        self.record = record
        if self.record.find('./{0}subject/{0}geographicCode'.format(NAMESPACES['mods'])) is not None:
            self.all_geocodes = []
            for geocode in self.record.iterfind('./{0}subject/{0}geographicCode'.format(NAMESPACES['mods'])):
                self.all_geocodes.append(geocode.text)
            return self.all_geocodes
        else:
            raise ElementNotFound

    def issuance(self, record):
        """
        Accesses mods:issuance element:
        return: list of mods:issuance texts or None.
        """
        self.record = record
        if self.record.find('.//{0}issuance'.format(NAMESPACES['mods'])) is not None:
            self.all_issuances = []
            for issuance in self.record.iterfind('.//{0}issuance'.format(NAMESPACES['mods'])):
                self.all_issuances.append(issuance.text)
            return self.all_issuances
        else:
            raise ElementNotFound

    def language(self, record):
        """
        Accesses mods:languageterm elements:
        :return: list of of dicts [{term-type: term}] or None.
        """
        self.record = record
        if self.record.find('.//{0}language'.format(NAMESPACES['mods'])) is not None:
            self.all_languages = []
            for language in self.record.iterfind('.//{0}language'.format(NAMESPACES['mods'])):
                languages = {}
                for term in language.iterchildren():
                    if 'type' in term.keys():
                        languages[term.attrib['type']] = term.text
                    else:
                        languages['untyped'] = term.text
                self.all_languages.append(languages)
            return self.all_languages
        else:
            raise ElementNotFound

    def _nameGen_(names, fullName):
        keys = []
        for key in names.keys():
            keys.append(key)
        if all(x in keys for x in ['family', 'given',
                                   'termsOfAddress', 'date']):
            fullName = fullName + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress'] + ', ' + \
                       names['date']
        elif all(x in keys for x in ['family', 'given', 'date']):
            fullName = fullName + names['family'] + ', ' + names['given'] + ', ' + names['date']
        elif all(x in keys for x in ['family', 'given', 'termsOfAddress']):
            fullName = fullName + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress']
        elif all(x in keys for x in ['family', 'termsOfAddress', 'date']):
            fullName = fullName + names['family'] + ', ' + names['termsOfAddress'] + ', ' + names['date']
        elif all(x in keys for x in ['given', 'termsOfAddress', 'date']):
            fullName = fullName + names['given'] + ', ' + names['termsOfAddress'] + ', ' + names['date']
        elif all(x in keys for x in ['family', 'given']):
            fullName = fullName + names['family'] + ', ' + names['given']
        elif all(x in keys for x in ['family', 'date']):
            fullName = fullName + names['family'] + ', ' + names['date']
        elif all(x in keys for x in ['family', 'termsOfAddress']):
            fullName = fullName + names['family'] + ', ' + names['termsOfAddress']
        elif all(x in keys for x in ['given', 'date']):
            fullName = fullName + names['given'] + ', ' + names['date']
        elif all(x in keys for x in ['given', 'termsOfAddress']):
            fullName = fullName + names['given'] + ', ' + names['termsOfAddress']
        elif all(x in keys for x in ['termsOfAddress', 'date']):
            fullName = fullName + ', ' + names['termsOfAddress'] + ', ' + names['date']
        elif 'date' in keys:
            fullName = fullName + ', ' + names['date']
        elif 'termsOfAddress' in keys:
            fullName = fullName + ', ' + names['termsOfAddress']
        return fullName

    def name_constructor(self, record):
        """
        Accesses mods:name/mods:namePart elements and reconstructs names into LOC order:
        return: a list of strings.
        """
        self.record = record
        if self.record.find('./{0}name'.format(NAMESPACES['mods'])) is not None:
            self.all_names = []
            for name in self.record.iterfind('./{0}name'.format(NAMESPACES['mods'])):
                full_name = name.attrib
                name_text = ""

                if name.find('./{0}namePart'.format(NAMESPACES['mods'])) is not None:

                    # Multipart name
                    if len(name.findall('./{0}namePart'.format(NAMESPACES['mods']))) > 1:
                        names = {}
                        for name_part in name.iterfind('./{0}namePart'.format(NAMESPACES['mods'])):

                            # Untyped nameParts
                            if 'type' not in name_part.attrib.keys():
                                name_text = name_text + ', ' + name_part.text
                                full_name['text'] = name_text.strip(', ')
                            # Typed nameParts
                            elif 'type' in name_part.attrib.keys():
                                names[name_part.attrib['type']] = name_part.text

                        if len(names) > 0:
                            full_name['text'] = Record._nameGen_(names, name_text.strip(', '))

                    # Single part name
                    else:
                        full_name['text'] = name_text + name.find(
                            './{0}namePart'.format(NAMESPACES['mods'])).text

                    # Roles
                    if name.find('./{0}role'.format(NAMESPACES['mods'])) is not None:
                        for role_term in name.iterfind('./{0}role/{0}roleTerm'.format(NAMESPACES['mods'])):
                            if role_term.attrib['type'] == 'code':
                                full_name['roleCode'] = role_term.text
                            elif role_term.attrib['type'] == 'text':
                                full_name['roleText'] = role_term.text

                else:
                    pass

                    self.all_names.append(full_name)

            if len(self.all_names) == 0:
                return None
            else:
                return self.all_names

        else:
            raise ElementNotFound

    def note(self, record):
        """
        Access mods:note elements and return a list of dicts:
        return: [{note-type: note-text}, untyped-note-text]
        """
        self.record = record
        if self.record.find('./{0}note'.format(NAMESPACES['mods'])) is not None:
            self.all_notes = []
            for note in self.record.iterfind('./{0}note'.format(NAMESPACES['mods'])):
                if len(note.attrib) >= 1:
                    if 'type' in note.attrib.keys():
                        typed_note = {note.attrib['type']: note.text}
                        self.all_notes.append(typed_note)
                    elif 'displayLabel' in note.attrib.keys():
                        labeled_note = {note.attrib['displayLabel']: note.text}
                        self.all_notes.append(labeled_note)
                    else:
                        self.all_notes.append({'untyped': note.text})
                else:
                    self.all_notes.append({'untyped': note.text})
            return self.all_notes
        else:
            raise ElementNotFound

    def physical_description_note(self, record):
        """
        Access mods:physicalDescription/mods:note elements and return a list of text values:
        return: list of note text values.
        """
        self.record = record
        if self.record.find('./{0}physicalDescription'.format(NAMESPACES['mods'])) is not None:
            for physical_description in self.record.iterfind('./{0}physicalDescription'.format(NAMESPACES['mods'])):
                self.all_notes = []
                for note in physical_description.iterfind('./{0}note'.format(NAMESPACES['mods'])):
                    self.all_notes.append(note.text)
            return self.all_notes
        else:
            raise ElementNotFound

    def physical_location(self, record):
        """
        Access mods:mods/mods:location/mods:physicalLocation and return text values.
        return: list of element text values.
        """
        self.record = record
        if self.record.find('./{0}location/{0}physicalLocation'.format(NAMESPACES['mods'])) is not None:
            self.all_locations = []
            for location in self.record.iterfind('./{0}location/{0}physicalLocation'.format(NAMESPACES['mods'])):
                self.all_locations.append(location.text)
            return self.all_locations
        else:
            raise ElementNotFound

    def publication_place(self, record):
        """
        Access mods:place and return a list of dicts:
        return: [{termType: termText}, {'untyped': termText}, ...]
        """
        self.record = record
        if self.record.find('.//{0}place'.format(NAMESPACES['mods'])) is not None:
            self.all_places = []
            for place in self.record.iterfind('.//{0}place'.format(NAMESPACES['mods'])):
                places = {}
                for term in place.iterchildren():
                    if 'type' in term.attrib.keys():
                        places[term.attrib['type']] = term.text
                    else:
                        places['untyped'] = term.text
                self.all_places.append(places)
            return self.all_places
        else:
            raise ElementNotFound

    def publisher(self, record):
        """
        Access mods:publisher and return a list of text values:
        return: [publisher, ...]
        """
        self.record = record
        if self.record.find('.//{0}publisher'.format(NAMESPACES['mods'])) is not None:
            self.all_publishers = []
            for publisher in self.record.iterfind('.//{0}publisher'.format(NAMESPACES['mods'])):
                self.all_publishers.append(publisher.text)
            return self.all_publishers
        else:
            raise ElementNotFound

    def rights(self, record):
        """
        Access mods:rights[type="use and reproduction|useAndReproduction" and return a dict:
        return: {'text': elementText, 'URI': rightsURI}
        """
        self.record = record
        if self.record.find('.//{0}accessCondition'.format(NAMESPACES['mods'])) is not None:
            for access_condition in self.record.iterfind('.//{0}accessCondition'.format(NAMESPACES['mods'])):
                self.rights = {}
                if 'use and reproduction' or 'useAndReproduction' in access_condition.attrib['type']:
                    self.rights['text'] = access_condition.text
                    if '{http://www.w3.org/1999/xlink}href' in access_condition.attrib.keys():
                        self.rights['URI'] = access_condition.attrib['{http://www.w3.org/1999/xlink}href']
            return self.rights

    def _subject_parser_(subject):
        parts = ['authority', 'authorityURI', 'valueURI']
        if subject.tag == '{0}subject'.format(NAMESPACES['mods']):
            subject_parts = {'text': Record._subject_text_(subject)}
        else:
            subject_parts = {'type': subject.tag, 'term': subject.text}
        children = []
        for part in parts:
            if part in subject.attrib.keys():
                subject_parts.update({part: subject.attrib[part]})
            else:
                pass
        for child in subject.iterchildren():
            children.append(Record._subject_parser_(child))
        if len(children) > 0:
            subject_parts.update({'children': children})
        return subject_parts

    def subject(self, record):
        """
        Access mods:subject elements and returns a list of dicts:
        return: [{'authority': , 'authorityURI': , 'valueURI': , children: {'type': child element name, 'term': text value}}, ... ]
        """
        self.record = record
        if self.record.find('./{0}subject'.format(NAMESPACES['mods'])) is not None:
            self.all_subjects = []
            for subject in self.record.iterfind('./{0}subject'.format(NAMESPACES['mods'])):
                if 'authority' in subject.attrib.keys():
                    if 'lcsh' or 'lctgm' or 'fast' == subject.attrib['authority'].lower():
                        self.all_subjects.append(Record._subject_parser_(subject))
                    elif 'naf' or 'lcnaf' == subject.attrib['authority'].lower():
                        if Record.name_constructor(subject) is not None:
                            self.all_subjects.append(Record.name_constructor(subject)[0])
                else:
                    self.all_subjects.append(Record._subject_parser_(subject))
            return self.all_subjects
        else:
            raise ElementNotFound

    def _subject_text_(subject):
        subject_text = ""
        for child in subject:
            if child.tag == '{0}name'.format(NAMESPACES['mods']):
                subject_text = subject_text + '--' + Record.name_constructor(child.getparent())[0]['text']
            else:
                subject_text = subject_text + '--' + child.text
        return subject_text.strip(' -,.')

    def subject_constructor(self, record):
        """
        Access mods:subject elements and parses text values into LOC double hyphenated complex headings
        return: A list of strings
        """
        self.record = record
        if Record.subject(self.record) is not None:
            self.subject_text_list = []
            for subject in Record.subject(self):
                self.subject_text_list.append(subject['text'])
            return self.subject_text_list
        else:
            raise ElementNotFound

    def title_constructor(self, record):
        """
        Accesses children of mods:titleInfo and return a list of titles in natural order:
        return: list of titles.
        """
        self.record = record
        if self.record.find('./{0}titleInfo'.format(NAMESPACES['mods'])) is not None:
            self.all_titles = []
            for title in self.record.iterfind('./{0}titleInfo'.format(NAMESPACES['mods'])):
                if title.find('./{0}nonSort'.format(NAMESPACES['mods'])) is not None and title.find(
                        './{0}title'.format(NAMESPACES['mods'])) is not None and title.find(
                    './{0}subTitle'.format(NAMESPACES['mods'])) is not None:
                    title_full = title.find('./{0}nonSort'.format(NAMESPACES['mods'])).text + ' ' + title.find(
                        './{0}title'.format(NAMESPACES['mods'])).text + ': ' + title.find(
                        './{0}subTitle'.format(NAMESPACES['mods'])).text
                elif title.find('./{0}nonSort'.format(NAMESPACES['mods'])) is not None and title.find(
                        './{0}title'.format(NAMESPACES['mods'])) is not None:
                    title_full = title.find('./{0}nonSort'.format(NAMESPACES['mods'])).text + ' ' + title.find(
                        './{0}title'.format(NAMESPACES['mods'])).text
                elif title.find('./{0}title'.format(NAMESPACES['mods'])) is not None and title.find(
                        './{0}subTitle'.format(NAMESPACES['mods'])) is not None:
                    title_full = title.find('./{0}title'.format(NAMESPACES['mods'])).text + ': ' + title.find(
                        './{0}subTitle'.format(NAMESPACES['mods'])).text
                else:
                    title_full = title.find('./{0}title'.format(NAMESPACES['mods'])).text
                self.all_titles.append(title_full)
            return self.all_titles
        else:
            raise ElementNotFound

    def type_of_resource(self, record):
        """
        Access mods:typeOfResource and return text value:
        return: text value or None
        """
        self.record = record
        if self.record.find('.//{0}typeOfResource'.format(NAMESPACES['mods'])) is not None:
            self.type_of_resource = self.record.find('.//{0}typeOfResource'.format(NAMESPACES['mods']))
            return self.type_of_resource.text
        else:
            raise ElementNotFound
