import collections

from lxml import etree

from pymods.constants import NAMESPACES, DATE_FIELDS

Abstract = collections.namedtuple('Abstract', 'text type displayLabel')
Collection = collections.namedtuple('Collection', 'location title url')
Genre = collections.namedtuple('Genre', 'term authority authorityURI valueURI')
Language = collections.namedtuple('Language', 'language type')
Name = collections.namedtuple('Name', 'name_parts roles type')
NamePart = collections.namedtuple('NamePart', 'name type')
Role = collections.namedtuple('Role', 'role type')
Note = collections.namedtuple('Note', 'text type dispayLabel')
PublicationPlace = collections.namedtuple('PublicationPlace', 'place type')
mods = NAMESPACES['mods']


class Record(etree.ElementBase):

    def _init(self):
        """
        Just hold on to the individual record up here, you don't need to pass
        it in to every method.

        :param mods_xml: XML representation of a MODS item
        """
        super(Record, self)._init()
        #self.mods_xml = parse_xml(mods_xml)

    # @property
    # def tag(self):
    #     return super().tag

    @property
    def abstract(self):
        """
        Pull information from mods:abstract element(s).

        List comprehensions allows building up a list by doing something
        with an iterator. In this case, the code as it would look in a
        C-style for loop would be:
        --
        accumulator = []
        for abstract in self.mods_xml.iterfind('./{0}abstract'.format(mods)):
            accumulator.append(Abstract(getattr(abstract, 'text', ''),
                                        abstract.attrib.get('type'),
                                        abstract.attrib.get('displayLabel'))
        return accumulator

        --
        Comprehension says more directly that 1) I'm just building up a list
        2) I'm just returning that list (what you want, a list with these
        elements, rather than how you want it built, by accumulating elements
        in such and such a way). It also keeps away from maintaining the state
        with an accumulator variable. Any time you find yourself doing
        something like above, consider a list comprehension.

        @property decorator means it will be called as .abstract rather than
        .abstract(); to me, this reads as 'this record has a thing called abstract'
        whereas .abstract() reads as 'this record does a thing called abstract'

        Also, Python has the concept of 'truthy', which means that in a
        boolean context, 0, the empty string, the empty list, the empty dict, etc.
        evaluate to false. So rather than returning None, we can just return the
        empty list which simplifies things by having only 1 return type. (Rule
        of thumb: if you say "Or" in describing what your function does or
        returns, think if "Or" is necessary. Try to keep methods, functions, etc.
        to doing or returning 1 type of thing, even though this isn't required
        by the language).

        So we can just iterate over what we find in iterfind, if nothing is there
        we end up with just an empty list. You don't really need to test if
        an iterator is going to have anything before iterating over it, if it's
        empty you just move on (this is not true in every language).

        :return: list of Abstract elements with text, type, and displayLabel
            attributes
        """
        return [Abstract(getattr(abstract, 'text', ''),
                         abstract.attrib.get('type'),
                         abstract.attrib.get('displayLabel'))
                for abstract in self.mods_xml.iterfind(
                './{0}abstract'.format(mods))]

    @property
    def classification(self):
        """
        Pull information from mods:classification element(s)

        :return: list of text from classification element(s)
        """
        return [classification.text for classification in
                self.mods_xml.iterfind(
                    './{0}classification'.format(mods))]

    @property
    def collection(self):
        """
        Retrieve data related to the item in a collection.

        I don't know MODS or your use case very well, so I assumed based on
        prior code that collection is 1) non-repeated, so return the collection
        rather than a list of collections, and 2) the elements are non-repeating,
        so return the first element of their lists. Alter as needed when these
        assumptions are false.

        :return: A Collection element with location, title, and url attributes
        """
        related_item = self.mods_xml.findall(
            './{0}relatedItem[@type="host"]'.format(mods))[0]
        return Collection(self.physical_location(related_item)[0],
                          self._title_constructor(related_item)[0],
                          self._url(related_item)[0])

    def _title_constructor(self, el):
        """
        Just for reference, if a method is internal, i.e. only used to make
        other methods in your class easier and not for the outside world to
        bugger with, Python coders tend to prefix those with an underscore
        to let other coders know this is a helper. Python doesn't have a
        concept of private like a lot of languages do, so this convention is
        just a gentle reminder to others reading the code. Some of your methods
        have a single underscore before and after, which is fine as far as the
        language is concerned, but will be confusing to other coders. It also
        treads dangerously close to dunder methods like __init__, which could
        be a problem.

        :param el: The element containing title information
        :return: A list of correctly formatted titles
        """
        return [self._format_titles(
            self._get_text(title.find('./{0}nonSort'.format(mods))),
            self._get_text(title.find('./{0}title'.format(mods))),
            self._get_text(title.find('./{0}subTitle'.format(mods))))
            for title in el.iterfind('./{0}titleInfo'.format(mods))]

    def _format_titles(self, non_sort, title, subtitle):
        """Construct valid title regardless if any constituent part missing."""
        return '{non_sort}{title}{subtitle}'.format(
            non_sort=non_sort + ' ' if non_sort else '',
            title=title if title else '',
            subtitle=': ' + subtitle if subtitle else ''
        )

    def _get_text(self, el):
        """Wrapping common use of getattr for safe attribute access."""
        return getattr(el, 'text', None)

    def physical_location(self, el):
        return [loc.text for loc in el.iterfind(
            './{0}location/{0}physicalLocation'.format(mods))]

    def _url(self, el):
        return [url.text for url in el.iterfind('./{0}location/{0}url'.format(mods))]

    def date_constructor(self):
        """
        Build a date string from information in originInfo

        This is another area where I am not familiar with your use case or
        MODS, so I have left the functionality as it was and just factored out
        a couple of layers. Questions about functionality:

        If a MODS record has the 'end' point before the 'start' point for any
        reason (or no reason), your string will output 'end - start'. You can
        collect a start and possibly end to avoid this. MODS or your use may
        outlaw this, but we all know data in the wild is weird.

        What if there are repeated or multiple bits of date information, i.e.
        a copyright date different from a dateIssued. This will only return the
        last of these rather than all (or, if it starts with a copyright, then
        something with a start and end, it will append them all, i.e.
        copyright - start - end, or if every element has a 'start', it will just
        continually appending dates onto each other). Depending, might consider
        making this a list of date elements with attributes, and do the string formatting
        separately for any given date, i.e. have a Date type that has a start
        and end attribute and format any given string based on whether or not
        it has an end. Can also store if it's an issued date, copyright date,
        etc.

        Also, you don't need the ignore list in this case. Those will be ignored
        by virtue of not being in the acceptable list. In most cases, if all
        you do is 'pass' on something, it may not be necessary.

        :return: A date containing string or None.
        """
        date = None
        for child in self._get_dates(self.mods_xml):
            # date range
            if 'point' in child.attrib.keys():
                if child.attrib['point'] == 'start':
                    if date is None:
                        date = child.text
                    else:
                        date = child.text + ' - ' + date
                elif child.attrib['point'] == 'end':
                    if date is None:
                        date = child.text
                    else:
                        date = date + ' - ' + child.text
            # single date
            else:
                date = child.text
        return date

    def _get_dates(self, el):
        return [date for date in el.find('./{0}originInfo'.format(mods)).iterchildren()
                if date.tag in DATE_FIELDS]

    @property
    def digital_origin(self):
        """
        Get text from mods:edition element.

        Python axiom: Better to ask forgiveness than permission.
        In Python code you will see a lot of try/except blocks rather than
        testing if something exists and then accessing it. This is also the
        reason for functions/methods like getattr and .get.

        In lots of languages, the axiom is look before you leap, so you get:
        if this_thing == exists:
            return this_thing

        This is the only way to avoid trying to access something that doesn't
        exist. But Python says "Just do the thing, and handle it if you get
        an error", and it's optimized for that style.

        So here, I try to just return the text from finding the edition field.
        If it's not there, self.mods_xml.find... will return None. I then try
        to access the text attribute, and if it's None, None does not have
        a text attribute, so it throws an AttributeError, which I catch and
        return an appropriate value. It's often trial and error to see what
        errors will be thrown by reasonable inputs.

        :return: String containing digital origin information
        """
        try:
            return self.mods_xml.find('.//{0}digitalOrigin'.format(mods)).text
        except AttributeError:
            return None

    @property
    def edition(self):
        """
        Accesses mods:edition element:
        return: element text or None.
        """
        try:
            return self.mods_xml.find('.//{0}edition'.format(mods)).text
        except AttributeError:
            return None

    @property
    def extent(self):
        """
        Accesses mods:extent element:
        return: list of mods:extent texts
        """
        return [extent.text for extent in self.mods_xml.iterfind('.//{0}extent'.format(mods))]

    @property
    def form(self):
        """
        Accesses mods:physicalDescription/mods:form element:
        return: list of mods:form texts
        """
        return [form.text for form in
                self.mods_xml.iterfind('./{0}physicalDescription/{0}form'.format(mods))]

    @property
    def genre(self):
        """
        Accesses mods:genre element:

        With this and the others like it, you could just as easily make this a
        dict with:
        {'term': genre.text, 'authority': genre.attrib.get('authority'),
         'authorityURI': genre.attrib.get('authorityURI'),
         'valueURI': genre.attrib.get('valueURI')}

        I just think namedtuples are a little more explicit about my intent.
        They also take up less space in memory. Just know that namedtuples
        (and all tuples) are immutable, so if you want to be able to change
        the values, you'll definitely want the dict.

        :return: A list containing Genre elements with term, authority,
            authorityURI, and valueURI attributes
        """
        return [Genre(genre.text,
                      genre.attrib.get('authority'),
                      genre.attrib.get('authorityURI'),
                      genre.attrib.get('valueURI'))
                for genre in self.mods_xml.iterfind('./{0}genre'.format(mods))]

    @property
    def geographic_code(self):
        """
        Accesses mods:geographicCode element:
        return: list of mods:geographicCode texts.
        """
        return [geocode.text for geocode in self.mods_xml.iterfind(
            './{0}subject/{0}geographicCode'.format(mods))]

    @property
    def issuance(self):
        """
        Accesses mods:issuance element:
        return: list of mods:issuance texts.
        """
        return [issuance.text for issuance in self.mods_xml.iterfind(
            './/{0}issuance'.format(mods))]

    @property
    def language(self):
        """
        language.type will just be None if we don't have a type, which is fine
        and easier to reason about than trying to figure out if it has such
        and such key in a dict. language.type will have the type if it exists.

        The nested list comprehension can be read the same as a nested for loop.
        The below would be:
        ---

        for lang in self.mods.iterfin(...):
            for term in lang.iterchildren():
                Language(term.text, term.attrib.get('type')

        ---

        :return: list of of Language elements with language and type attributes
        """
        return [Language(term.text, term.attrib.get('type'))
                for lang in self.mods_xml.iterfind('.//{0}language'.format(mods))
                for term in lang.iterchildren()]

    @property
    def personal_names(self):
        return sorted([self._format_name(name) for name in self.get_names()
                       if name.type == 'personal'])

    @property
    def corporate_names(self):
        return sorted([self._format_name(name) for name in self.get_names()
                       if name.type == 'corporate'])

    def _format_name(self, name):
        """
        Take in a Name object and make a formatted string representation.

        The big picture thing here is that you should separate out the logic
        that finds and puts names together and the logic that formats them
        for output. That way if you want to do anything with them other than
        output them that way, you already have them ready.

        This is kind of ugly, and if our lists were large it would be pretty
        inefficient (we go over the whole list of names 4 times), but allows
        using the same format method for corporate and personal names.
        A dict implementation is below that is not complete.

        Note that in a library like this it is not even strictly necessary
        to give formatted strings; if somebody else wants the role and doesn't
        care so much about whether it's corporate or personal, they might want
        the strings formatted differently (I get it that this is LC style, but
        what if someone is running transformations?). The get_names method might
        prove to be more useful. That said, giving a common string representation
        is certainly nice.

        :param name: A Name element
        :return: A string formatted according to LOC conventions
        """
        family = ', '.join(x.name for x in name.name_parts
                           if x.type == 'family')
        given = ', '.join(x.name for x in name.name_parts
                          if x.type == 'given' or x.type is None)
        terms_of_address = ', '.join(x.name for x in name.name_parts
                                     if x.type == 'termsOfAddress')
        date = ', '.join(x.name for x in name.name_parts
                         if x.type == 'date')
        return '{family}{given}{termsOfAddress}{date}'.format(
            family=family + ', ' if family else '',
            given=given if given else '',
            termsOfAddress=', ' + terms_of_address if terms_of_address else '',
            date=', ' + date if date else ''
        )

    def get_names(self):
        return [Name(self._make_name_parts(name),
                     self._make_roles(name),
                     name.attrib.get('type'))
                for name in self.mods_xml.iterfind('./{0}name'.format(mods))]

    def _make_name_parts(self, el):
        return [NamePart(name.text, name.attrib.get('type')) for name in
                el.iterfind('./{0}namePart'.format(mods))]

    def _make_roles(self, el):
        return [Role(name.text, name.attrib.get('type')) for name in
                el.iterfind('./{0}role/{0}roleTerm'.format(mods))]

    @property
    def personal_names_dict(self):
        return sorted([self._format_names_dict(name) for name in
                       self.get_names_dict() if name['type'] == 'personal'])

    def get_names_dict(self):
        """
        This would look cleaner if I'd broken getting name parts into their
        own functions like I did with the namedtuple version. This method does
        have the nice quality of keeping the type of part tightly coupled
        with its value so you can get the familyName by dict['family']
        rather than name.name if name.type == 'family'. A defaultdict is really
        handy, it acts like a dict, but you assign it a default value. So in
        this case, we can just start appending to a list at the location
        name_parts[type] because if that address is not initialized, it will
        automatically become a list. Removes the:
            if not name_parts[type]:
                name_parts[type] = ['our namePart text']

        This code is essentially doing the same thing as the code above, and
        could be put into a compact list comprehension if we wanted.
        :return: a list of dicts containing a type string, a nameParts list
        of dicts, and a roles list of dicts.
        """
        names = []
        for name in self.mods_xml.iterfind('./{0}name'.format(mods)):
            name_parts = collections.defaultdict(list)
            for name_part in name.iterfind('./{0}namePart'.format(mods)):
                name_parts[name_part.attrib.get('type')].append(name_part.text)
            names.append({'type': name.attrib.get('type'),
                          'nameParts': name_parts,
                          'roles': [{'type': role.attrib.get('type'),
                                     'role': role.text} for role in
                                    name.iterfind('./{0}role/{0}roleTerm'.format(mods))]})
        return names

    def _format_names_dict(self, name):
        """
        The reason for keeping everything in lists even when we can assume there
        will only be 1 of them (i.e. only 1 given name, only 1 family name)
        is basically to deal with None. A name with no type can show up an
        unlimited number of times, and it's easier to reason if everything of
        a type has the same representation, not some being strings and some
        beings lists of strings and some being None. If all we have to know is
        a name is in a list, that reduces our cognitive load, even though
        sometimes it leads to kind of wonky looking code (honestly, trying
        to make string formatting generic I feel always leads to wonky looking
        stuff). It's also a memory consideration, because a single-item list
        with a string will take more memory than just the string itself.
        Also, I prefer data structures to have a set representation, so, as in
        several places above, I will have structures with fields whether or not
        they are used because some members of that type have those fields.
        The extra memory for these is rarely an issue, especially in most
        general library contexts where we're not dealing with mission-critical
        memory issues.
        .get() for dicts makes this less of an issue in Python, because we can
        try to get something from a dict and then just default if it's not
        there.

        Also, this is probably doing too much in one line; the joining and
        all should happen somewhere else then the conditional formatting
        can happen.
        :param name:
        :return:
        """
        return '{family}{given}{termsOfAddress}{date}'.format(
            family=''.join(name['nameParts'].get('family')) + ', ' if name['nameParts'].get('family') else '',
            given=''.join(name['nameParts'].get('given')) if name['nameParts'].get('given') else ', '.join(
                name['nameParts'][None]),
            termsOfAddress=', ' + ''.join(name['nameParts'].get('termsOfAddress')) if name['nameParts'].get(
                'termsOfAddress') else '',
            date=', ' + ''.join(name['nameParts'].get('date')) if name['nameParts'].get('date') else ''
        )

    @property
    def note(self):
        return [Note(note.text, note.attrib.get('type'), note.attrib.get('displayLabel'))
                for note in self.mods_xml.iterfind('./{0}note'.format(mods))]

    @property
    def physical_description_note(self):
        return [note.text for note in self.mods_xml.findall(
            './{0}physicalDescription/{0}note'.format(mods))]

    @property
    def publication_place(self):
        """Probably not exactly what you want, treats each pub place as disctinct,
        even if just a code."""
        return [PublicationPlace(term.text, term.attrib.get('type'))
                for place in self.mods_xml.findall('./{0}originInfo/{0}place'.format(mods))
                for term in place.iterchildren()]

    @property
    def publication_place_dict(self):
        """
        Sorry, couldn't help it.

        I'm sorry if this just got a little bendy, but it should hopefully
        read in a way that makes sense. In Python, we can do comprehensions
        over dicts, sets, and lists (and generators, but that's a bit different)
        So really, this code does exactly what your previous code did, it goes
        over every child of every originInfo/place, and places them into a dict
        by their 'type' attribute, and places that dict into a list.
        Comprehensions are oh so nice.

        Code still has questions, namely the arch-nemesis 'what if we have more
        than 1?' If we have multiple codes for something or multiple 'untyped'
        we will end up just overwriting, only retaining the last one seen. Is
        this not a problem in real-world MODS?
        :return: A list of dicts containing element texts indexed by name
            attribute
        """
        return [{term.attrib.get('type'): term.text for term in place.iterchildren()}
                for place in self.mods_xml.findall(
                './{0}originInfo/{0}place'.format(mods))]

    @property
    def publisher(self):
        return [publisher.text for publisher in
                self.mods_xml.findall('./{0}originInfo/{0}publisher'.format(mods))]

        # @property
        # def rights(self):
        #     """
        #     If we're potentially iterating over accessConditions, should we be
        #     building up a list of them?
        #
        #     Also, this implementation has a subtle bug in your first conditional.
        #     ---
        #     if 'use and reproduction' or 'useAndReproduction' in access_condition.attrib['type']:
        #     ---
        #     that is always going to return True and as such enter that branch. The
        #     reason is one of those areas where Python being so readable runs us into
        #     a common trouble. The condition is parsed as follows:
        #     if ('use and reproduction') or ('useAndReproduction' in access_condition.attrib['type']):
        #     'use and reproduction' is parsed as its own statement, and since it's a
        #     non-empty string, it returns True every time. It has to do with
        #     operator precedence and such, but for now just know that this statement
        #     needs to be written a little more verbosely:
        #     if 'use and reproduction' in access_condition.attrib['type'] or 'useAndReproduction' in access_condition.attrib['type']:
        #
        #     Also, is it true that we only want URIs if accessCondition is for
        #     use and reproduction? Should we just build up the rights as they are
        #     in the document and then pull out the ones we care about for software
        #     later? We may want a separation of parsing the MODS document and what
        #     we want to do with that information into pymods, the library for getting
        #     the data and the software we build with the pymods library to do interesting
        #     things.
        #
        #     :return:
        #     """
        #     if record.find('.//{0}accessCondition'.format(
        #             nameSpace_default['mods'])) is not None:
        #         for access_condition in record.iterfind(
        #                 './/{0}accessCondition'.format(nameSpace_default['mods'])):
        #             rights = {}
        #             if 'use and reproduction' or 'useAndReproduction' in \
        #                     access_condition.attrib['type']:
        #                 rights['text'] = access_condition.text
        #                 if '{http://www.w3.org/1999/xlink}href' in access_condition.attrib.keys():
        #                     rights['URI'] = access_condition.attrib[
        #                         '{http://www.w3.org/1999/xlink}href']
        #
        #     return rights
        #
        # def subject(record):
        #     """
        #     Your inner if/elif clauses here have the same bug as above:
        #     'lcsh' or 'lctgm' == subject.attrib['authority'].lower(): will always
        #     go true, so your naf or lcnaf branches are never being executed.
        #     """
        #     if record.find('./{0}subject'.format(nameSpace_default['mods'])) is not None:
        #         all_subjects = []
        #         for subject in record.iterfind('./{0}subject'.format(nameSpace_default['mods'])):
        #             if 'authority' in subject.attrib.keys():
        #                 if 'lcsh' or 'lctgm' or 'fast' == subject.attrib['authority'].lower():
        #                     all_subjects.append(MODS._subject_parser_(subject))
        #                 elif 'naf' or 'lcnaf' == subject.attrib['authority'].lower():
        #                     if MODS.name_constructor(subject) is not None:
        #                         all_subjects.append(MODS.name_constructor(subject)[0])
        #             else:
        #                 all_subjects.append(MODS._subject_parser_(subject))
        #         return all_subjects
        #     else:
        #         return None


class OAIRecord(Record):

    def __init__(self):
        super(OAIRecord, self).__init__()

    @property
    def oai_id(self):
        pass


def parse_xml(xml):
    """
    Take the argument to a new instance of Record, and try to parse it as a file.
    If it's not a file (i.e. it's coming from a MODSReader class) then an OSError
    will be thrown, in which case we build it from a string. Should probably
    also handle the case where some bad XML or something gets passed and
    etree.fromstring(xml) throws an Exception to provide a good error message
    to users rather than whatever lxml uses.
    :param xml: 
    :return: 
    """
    try:
        return etree.parse(xml).getroot()
    except OSError:
        return etree.fromstring(xml)

# import re
# from lxml import etree
#
# from pymods.constants import NAMESPACES
# from pymods.exceptions import ElementNotFound
#
#
# class Record(etree.ElementBase):
#
#     def _init(self):
#         super(etree.ElementBase, self).__init__()
#
#     def abstract(self, elem=None):
#         """
#         Access mods:abstract elements and return a list of dicts:
#         return: [{abstract displayLabel: abstract text}] or None.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}abstract'.format(NAMESPACES['mods'])) is not None:
#             all_abstracts = []
#             for abstract in record.iterfind('./{0}abstract'.format(NAMESPACES['mods'])):
#                 if len(abstract.attrib) >= 1:
#                     if 'type' in abstract.attrib.keys():
#                         typed_abstract = {abstract.attrib['type']: abstract.text}
#                         all_abstracts.append(typed_abstract)
#                     elif 'displayLabel' in abstract.attrib.keys():
#                         labeled_abstract = {abstract.attrib['displayLabel']: abstract.text}
#                         all_abstracts.append(labeled_abstract)
#                     else:
#                         all_abstracts.append(abstract.text)
#                 else:
#                     all_abstracts.append(abstract.text)
#             return all_abstracts
#         else:
#             return None
#
#     def classification(self, elem=None):
#         """
#         Access mods:classification element:
#         return: [classification text, ... ] or None
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}classification'.format(NAMESPACES['mods'])) is not None:
#             all_classifications = []
#             for classification in record.iterfind('./{0}classification'.format(NAMESPACES['mods'])):
#                 all_classifications.append(classification.text)
#             return all_classifications
#         else:
#             return None
#
#     def collection(self, elem=None):
#         """
#         Retrieve archival collection metadata from mods:relatedItem[type="host"]:
#         return: {'location': collection location, 'title': collection title, 'url': link to collection (if found)}
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}relatedItem'.format(NAMESPACES['mods'])) is not None:
#             for related_item in record.iterfind('./{0}relatedItem'.format(NAMESPACES['mods'])):
#                 if 'type' in related_item.attrib.keys():
#                     if 'host' == related_item.attrib['type']:
#                         host_info = {}
#                         if self.title_constructor(related_item) is not None:
#                             host_title = self.title_constructor(related_item)[0]
#                             host_info['title'] = host_title
#
#                         if self.physical_location(related_item) is not None:
#                             host_location = self.physical_location(related_item)[0]
#                             host_info['location'] = host_location
#
#                         if related_item.find('./{0}location/{0}url'.format(NAMESPACES['mods'])) is not None:
#                             host_info['url'] = related_item.find('./{0}location/{0}url'.format(NAMESPACES['mods'])).text
#
#                         return host_info
#         else:
#             return None
#
#     def date_constructor(self, elem=None):
#         """
#         Accesses mods:dateIssued, mods:dateCreated, mods:copyrightDate, and mods:dateOther underneath mods:originInfo. Other date-type elements are ignored:
#         return: A date containing string or None.
#         """
#         date_list = ['{0}dateIssued'.format(NAMESPACES['mods']),
#                      '{0}dateCreated'.format(NAMESPACES['mods']),
#                      '{0}copyrightDate'.format(NAMESPACES['mods']),
#                      '{0}dateOther'.format(NAMESPACES['mods'])]
#         ignore_list = ['{0}place'.format(NAMESPACES['mods']),
#                        '{0}publisher'.format(NAMESPACES['mods']),
#                        '{0}dateCaptured'.format(NAMESPACES['mods']),
#                        '{0}dateValid'.format(NAMESPACES['mods']),
#                        '{0}dateModified'.format(NAMESPACES['mods']),
#                        '{0}edition'.format(NAMESPACES['mods']),
#                        '{0}issuance'.format(NAMESPACES['mods']),
#                        '{0}frequency'.format(NAMESPACES['mods'])]
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}originInfo'.format(NAMESPACES['mods'])) is not None:
#             origin_info = record.find('./{0}originInfo'.format(NAMESPACES['mods']))
#             date = None
#             for child in origin_info.iterchildren():
#                 if child.tag in date_list:
#                     # date range
#                     if 'point' in child.attrib.keys():
#                         if child.attrib['point'] == 'start':
#                             if date is None:
#                                 date = child.text
#                             else:
#                                 date = child.text + ' - ' + date
#                         elif child.attrib['point'] == 'end':
#                             if date is None:
#                                 date = child.text
#                             else:
#                                 date = date + ' - ' + child.text
#                     # single date
#                     else:
#                         date = child.text
#                 elif child.tag in ignore_list:
#                     pass
#             return date
#         else:
#             return None
#
#     def digital_origin(self, elem=None):
#         """
#         Accesses mods:digitalOrigin element:
#         return: element text or None.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}digitalOrigin'.format(NAMESPACES['mods'])) is not None:
#             return record.find('.//{0}digitalOrigin'.format(NAMESPACES['mods'])).text
#         else:
#             return None
#
#     def doi_search(self, elem=None):
#         """
#         Get DigiNole IID from MODS record:
#         return: item's IID.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}identifier'.format(NAMESPACES['mods'])) is not None:
#             for identifier in record.iterfind('.//{0}identifier'.format(NAMESPACES['mods'])):
#                 if 'type' in identifier.attrib is not None:
#                     if 'DOI' == identifier.attrib['type']:
#                         return identifier.text
#         else:
#             return None
#
#     def edition(self, elem=None):
#         """
#         Accesses mods:edition element:
#         return: element text or None.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}edition'.format(NAMESPACES['mods'])) is not None:
#             return record.find('.//{0}edition'.format(NAMESPACES['mods'])).text
#         else:
#             return None
#
#     def extent(self, elem=None):
#         """
#         Accesses mods:extent element:
#         return: list of mods:extent texts or None.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}extent'.format(NAMESPACES['mods'])) is not None:
#             all_extents = []
#             for extent in record.iterfind('.//{0}extent'.format(NAMESPACES['mods'])):
#                 all_extents.append(extent.text)
#             return all_extents
#         else:
#             return None
#
#     def form(self, elem=None):
#         """
#         Accesses mods:physicalDescription/mods:form element:
#         return: list of mods:form texts or None.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}physicalDescription/{0}form'.format(NAMESPACES['mods'])) is not None:
#             all_forms = []
#             for form in record.iterfind('./{0}physicalDescription/{0}form'.format(NAMESPACES['mods'])):
#                 all_forms.append(form.text)
#             return all_forms
#         else:
#             return None
#
#     def genre(self, elem=None):
#         """
#         Accesses mods:genre element:
#         return: [ { 'term': , 'authority': , 'authorityURI': , 'valueURI': }, ] or None.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}genre'.format(NAMESPACES['mods'])) is not None:
#             all_genres = []
#             for genre in record.iterfind('./{0}genre'.format(NAMESPACES['mods'])):
#                 genre_elems = {}
#                 genre_elems['term'] = genre.text
#                 if 'authority' in genre.attrib.keys():
#                     genre_elems['authority'] = genre.attrib['authority']
#                 if 'authorityURI' in genre.attrib.keys():
#                     genre_elems['authorityURI'] = genre.attrib['authorityURI']
#                 if 'valueURI' in genre.attrib.keys():
#                     genre_elems['valueURI'] = genre.attrib['valueURI']
#                 all_genres.append(genre_elems)
#             return all_genres
#         else:
#             return None
#
#     def geographic_code(self, elem=None):
#         """
#         Accesses mods:geographicCode element:
#         return: list of mods:geographicCode texts or None.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}subject/{0}geographicCode'.format(NAMESPACES['mods'])) is not None:
#             all_geocodes = []
#             for geocode in record.iterfind('./{0}subject/{0}geographicCode'.format(NAMESPACES['mods'])):
#                 all_geocodes.append(geocode.text)
#             return all_geocodes
#         else:
#             return None
#
#     def issuance(self, elem=None):
#         """
#         Accesses mods:issuance element:
#         return: list of mods:issuance texts or None.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}issuance'.format(NAMESPACES['mods'])) is not None:
#             all_issuances = []
#             for issuance in record.iterfind('.//{0}issuance'.format(NAMESPACES['mods'])):
#                 all_issuances.append(issuance.text)
#             return all_issuances
#         else:
#             return None
#
#     def language(self, elem=None):
#         """
#         Accesses mods:languageterm elements:
#         :return: list of of dicts [{term-type: term}] or None.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}language'.format(NAMESPACES['mods'])) is not None:
#             all_languages = []
#             for language in record.iterfind('.//{0}language'.format(NAMESPACES['mods'])):
#                 languages = {}
#                 for term in language.iterchildren():
#                     if 'type' in term.keys():
#                         languages[term.attrib['type']] = term.text
#                     else:
#                         languages['untyped'] = term.text
#                 all_languages.append(languages)
#             return all_languages
#         else:
#             return None
#
#     def local_identifier(self, elem=None, type='IID'):
#         """
#         Get DigiNole IID from MODS record:
#         return: item's IID.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}identifier'.format(NAMESPACES['mods'])) is not None:
#             for identifier in record.iterfind('.//{0}identifier'.format(NAMESPACES['mods'])):
#                 if 'type' in identifier.attrib is not None:
#                     if type == identifier.attrib['type']:
#                         return identifier.text
#
#     def _nameGen_(names, full_name):
#         keys = []
#         for key in names.keys():
#             keys.append(key)
#         if all(x in keys for x in ['family', 'given',
#                                    'termsOfAddress', 'date']):
#             full_name = full_name + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress'] + ', ' + \
#                        names['date']
#         elif all(x in keys for x in ['family', 'given', 'date']):
#             full_name = full_name + names['family'] + ', ' + names['given'] + ', ' + names['date']
#         elif all(x in keys for x in ['family', 'given', 'termsOfAddress']):
#             full_name = full_name + names['family'] + ', ' + names['given'] + ', ' + names['termsOfAddress']
#         elif all(x in keys for x in ['family', 'termsOfAddress', 'date']):
#             full_name = full_name + names['family'] + ', ' + names['termsOfAddress'] + ', ' + names['date']
#         elif all(x in keys for x in ['given', 'termsOfAddress', 'date']):
#             full_name = full_name + names['given'] + ', ' + names['termsOfAddress'] + ', ' + names['date']
#         elif all(x in keys for x in ['family', 'given']):
#             full_name = full_name + names['family'] + ', ' + names['given']
#         elif all(x in keys for x in ['family', 'date']):
#             full_name = full_name + names['family'] + ', ' + names['date']
#         elif all(x in keys for x in ['family', 'termsOfAddress']):
#             full_name = full_name + names['family'] + ', ' + names['termsOfAddress']
#         elif all(x in keys for x in ['given', 'date']):
#             full_name = full_name + names['given'] + ', ' + names['date']
#         elif all(x in keys for x in ['given', 'termsOfAddress']):
#             full_name = full_name + names['given'] + ', ' + names['termsOfAddress']
#         elif all(x in keys for x in ['termsOfAddress', 'date']):
#             full_name = full_name + ', ' + names['termsOfAddress'] + ', ' + names['date']
#         elif 'date' in keys:
#             full_name = full_name + ', ' + names['date']
#         elif 'termsOfAddress' in keys:
#             full_name = full_name + ', ' + names['termsOfAddress']
#         return full_name
#
#     def name_constructor(self, elem=None):
#         """
#         Accesses mods:name/mods:namePart elements and reconstructs names into LOC order:
#         return: a list of strings.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}name'.format(NAMESPACES['mods'])) is not None:
#             all_names = []
#             for name in record.iterfind('./{0}name'.format(NAMESPACES['mods'])):
#                 full_name = name.attrib
#                 name_text = ""
#
#                 if name.find('./{0}namePart'.format(NAMESPACES['mods'])) is not None:
#
#                     # Multipart name
#                     if len(name.findall('./{0}namePart'.format(NAMESPACES['mods']))) > 1:
#                         names = {}
#                         for name_part in name.iterfind('./{0}namePart'.format(NAMESPACES['mods'])):
#
#                             # Untyped nameParts
#                             if 'type' not in name_part.attrib.keys():
#                                 name_text = name_text + ', ' + name_part.text
#                                 full_name['text'] = name_text.strip(', ')
#                             # Typed nameParts
#                             elif 'type' in name_part.attrib.keys():
#                                 names[name_part.attrib['type']] = name_part.text
#
#                         if len(names) > 0:
#                             full_name['text'] = Record._nameGen_(names, name_text.strip(', '))
#
#                     # Single part name
#                     else:
#                         full_name['text'] = name_text + name.find(
#                             './{0}namePart'.format(NAMESPACES['mods'])).text
#
#                     # Roles
#                     if name.find('./{0}role'.format(NAMESPACES['mods'])) is not None:
#                         for role_term in name.iterfind('./{0}role/{0}roleTerm'.format(NAMESPACES['mods'])):
#                             if role_term.attrib['type'] == 'code':
#                                 full_name['roleCode'] = role_term.text
#                             elif role_term.attrib['type'] == 'text':
#                                 full_name['roleText'] = role_term.text
#
#                     all_names.append(full_name)
#
#             if len(all_names) == 0:
#                 return None
#             else:
#                 return all_names
#         else:
#             return None
#
#     def note(self, elem=None):
#         """
#         Access mods:note elements and return a list of dicts:
#         return: [{note-type: note-text}, untyped-note-text]
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}note'.format(NAMESPACES['mods'])) is not None:
#             all_notes = []
#             for note in record.iterfind('./{0}note'.format(NAMESPACES['mods'])):
#                 if len(note.attrib) >= 1:
#                     if 'type' in note.attrib.keys():
#                         typed_note = {note.attrib['type']: note.text}
#                         all_notes.append(typed_note)
#                     elif 'displayLabel' in note.attrib.keys():
#                         labeled_note = {note.attrib['displayLabel']: note.text}
#                         all_notes.append(labeled_note)
#                     else:
#                         all_notes.append({'untyped': note.text})
#                 else:
#                     all_notes.append({'untyped': note.text})
#             return all_notes
#         else:
#             return None
#
#     def physical_description_note(self, elem=None):
#         """
#         Access mods:physicalDescription/mods:note elements and return a list of text values:
#         return: list of note text values.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}physicalDescription'.format(NAMESPACES['mods'])) is not None:
#             for physical_description in record.iterfind('./{0}physicalDescription'.format(NAMESPACES['mods'])):
#                 all_notes = []
#                 for note in physical_description.iterfind('./{0}note'.format(NAMESPACES['mods'])):
#                     all_notes.append(note.text)
#             return all_notes
#         else:
#             return None
#
#     def physical_location(self, elem=None):
#         """
#         Access mods:mods/mods:location/mods:physicalLocation and return text values.
#         return: list of element text values.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}location/{0}physicalLocation'.format(NAMESPACES['mods'])) is not None:
#             all_locations = []
#             for location in record.iterfind('./{0}location/{0}physicalLocation'.format(NAMESPACES['mods'])):
#                 all_locations.append(location.text)
#             return all_locations
#         else:
#             return None
#
#     def pid_search(self, elem=None, prefix='fsu:'):
#         """
#         Get fedora PID from MODS record:
#         return: item's fedora PID.
#         """
#         pid = re.compile(prefix)
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}identifier'.format(NAMESPACES['mods'])) is not None:
#             for identifier in record.iterfind('.//{0}identifier'.format(NAMESPACES['mods'])):
#                 match = pid.search(identifier.text)
#                 if match:
#                     return match.string
#         else:
#             return None
#
#     def publication_place(self, elem=None):
#         """
#         Access mods:place and return a list of dicts:
#         return: [{termType: termText}, {'untyped': termText}, ...]
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}place'.format(NAMESPACES['mods'])) is not None:
#             all_places = []
#             for place in record.iterfind('.//{0}place'.format(NAMESPACES['mods'])):
#                 places = {}
#                 for term in place.iterchildren():
#                     if 'type' in term.attrib.keys():
#                         places[term.attrib['type']] = term.text
#                     else:
#                         places['untyped'] = term.text
#                 all_places.append(places)
#             return all_places
#         else:
#             return None
#
#     def publisher(self, elem=None):
#         """
#         Access mods:publisher and return a list of text values:
#         return: [publisher, ...]
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}publisher'.format(NAMESPACES['mods'])) is not None:
#             all_publishers = []
#             for publisher in record.iterfind('.//{0}publisher'.format(NAMESPACES['mods'])):
#                 all_publishers.append(publisher.text)
#             return all_publishers
#         else:
#             return None
#
#     def purl_search(self, elem=None):
#         """
#         Accesses record's Persistent URL from mods:mods/mods:location/mods:url:
#         return: item PURL as string.
#         """
#         purl = re.compile('((http://purl)[\w\d:#@%/;$()~_?\+-=\\\.&]+)')
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}location/{0}url'.format(NAMESPACES['mods'])) is not None:
#             for url in record.iterfind('./{0}location/{0}url'.format(NAMESPACES['mods'])):
#                 match = purl.search(url.text)
#                 if match:
#                     return match.string
#         else:
#             return None
#
#     def rights(self, elem=None):
#         """
#         Access mods:rights[type="use and reproduction|useAndReproduction" and return a dict:
#         return: {'text': elementText, 'URI': rightsURI}
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}accessCondition'.format(NAMESPACES['mods'])) is not None:
#             for access_condition in record.iterfind('.//{0}accessCondition'.format(NAMESPACES['mods'])):
#                 rights = {}
#                 if 'use and reproduction' or 'useAndReproduction' in access_condition.attrib['type']:
#                     rights['text'] = access_condition.text
#                     if '{http://www.w3.org/1999/xlink}href' in access_condition.attrib.keys():
#                         rights['URI'] = access_condition.attrib['{http://www.w3.org/1999/xlink}href']
#             return rights
#         else:
#             return None
#
#     def _subject_parser_(subject):
#         parts = ['authority', 'authorityURI', 'valueURI']
#         if subject.tag == '{0}subject'.format(NAMESPACES['mods']):
#             subject_parts = {'text': Record._subject_text_(subject)}
#         else:
#             subject_parts = {'type': subject.tag, 'term': subject.text}
#         children = []
#         for part in parts:
#             if part in subject.attrib.keys():
#                 subject_parts.update({part: subject.attrib[part]})
#             else:
#                 pass
#         for child in subject.iterchildren():
#             children.append(Record._subject_parser_(child))
#         if len(children) > 0:
#             subject_parts.update({'children': children})
#         return subject_parts
#
#     def subject(self, elem=None):
#         """
#         Access mods:subject elements and returns a list of dicts:
#         return: [{'authority': , 'authorityURI': , 'valueURI': , children: {'type': child element name, 'term': text value}}, ... ]
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}subject'.format(NAMESPACES['mods'])) is not None:
#             all_subjects = []
#             for subject in record.iterfind('./{0}subject'.format(NAMESPACES['mods'])):
#                 if 'authority' in subject.attrib.keys():
#                     if 'lcsh' or 'lctgm' or 'fast' == subject.attrib['authority'].lower():
#                         all_subjects.append(Record._subject_parser_(subject))
#                     elif 'naf' or 'lcnaf' == subject.attrib['authority'].lower():
#                         if self.name_constructor(subject) is not None:
#                             all_subjects.append(self.name_constructor(subject)[0])
#                 else:
#                     all_subjects.append(Record._subject_parser_(subject))
#             return all_subjects
#         else:
#             return None
#
#     def _subject_text_(subject):
#         subject_text = ""
#         for child in subject:
#             if child.tag == '{0}name'.format(NAMESPACES['mods']):
#                 subject_text = subject_text + '--' + Record.name_constructor(subject, elem=child.getparent())[0]['text']
#             else:
#                 subject_text = subject_text + '--' + child.text
#         return subject_text.strip(' -,.')
#
#     def subject_constructor(self, elem=None):
#         """
#         Access mods:subject elements and parses text values into LOC double hyphenated complex headings
#         return: A list of strings
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if self.subject(record) is not None:
#             subject_text_list = []
#             for subject in self.subject(record):
#                 subject_text_list.append(subject['text'])
#             return subject_text_list
#         else:
#             return None
#
#     def title_constructor(self, elem=None):
#         """
#         Accesses children of mods:titleInfo and return a list of titles in natural order:
#         return: list of titles.
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('./{0}titleInfo'.format(NAMESPACES['mods'])) is not None:
#             all_titles = []
#             for title in record.iterfind('./{0}titleInfo'.format(NAMESPACES['mods'])):
#                 if title.find('./{0}nonSort'.format(NAMESPACES['mods'])) is not None and title.find(
#                         './{0}title'.format(NAMESPACES['mods'])) is not None and title.find(
#                         './{0}subTitle'.format(NAMESPACES['mods'])) is not None:
#                     title_full = title.find('./{0}nonSort'.format(NAMESPACES['mods'])).text + ' ' + title.find(
#                         './{0}title'.format(NAMESPACES['mods'])).text + ': ' + title.find(
#                         './{0}subTitle'.format(NAMESPACES['mods'])).text
#                 elif title.find('./{0}nonSort'.format(NAMESPACES['mods'])) is not None and title.find(
#                         './{0}title'.format(NAMESPACES['mods'])) is not None:
#                     title_full = title.find('./{0}nonSort'.format(NAMESPACES['mods'])).text + ' ' + title.find(
#                         './{0}title'.format(NAMESPACES['mods'])).text
#                 elif title.find('./{0}title'.format(NAMESPACES['mods'])) is not None and title.find(
#                         './{0}subTitle'.format(NAMESPACES['mods'])) is not None:
#                     title_full = title.find('./{0}title'.format(NAMESPACES['mods'])).text + ': ' + title.find(
#                         './{0}subTitle'.format(NAMESPACES['mods'])).text
#                 else:
#                     title_full = title.find('./{0}title'.format(NAMESPACES['mods'])).text
#                 all_titles.append(title_full)
#             return all_titles
#         else:
#             return None
#
#     def type_of_resource(self, elem=None):
#         """
#         Access mods:typeOfResource and return text value:
#         return: text value or None
#         """
#         if elem is not None:
#             record = elem
#         else:
#             record = self[0]
#         if record.find('.//{0}typeOfResource'.format(NAMESPACES['mods'])) is not None:
#             type_of_resource = record.find('.//{0}typeOfResource'.format(NAMESPACES['mods']))
#             return type_of_resource.text
#         else:
#             return None
#
# #    def _exists(self, elem):
# #        if self[0].find(elem) is not None:
# #            return True
# #        else:
# #            return None
# #            #raise ElementNotFound
