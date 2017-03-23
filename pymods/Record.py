import collections

from lxml import etree

from pymods.constants import NAMESPACES, DATE_FIELDS


Abstract = collections.namedtuple('Abstract', 'text type displayLabel')
Collection = collections.namedtuple('Collection', 'location title url')
Genre = collections.namedtuple('Genre', 'term authority authorityURI valueURI')
Language = collections.namedtuple('Language', 'language type')
mods = NAMESPACES['mods']


class Record:

    def __init__(self, mods_xml):
        self.mods_xml = parse_xml(mods_xml)

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
        return Collection(self._physical_location(related_item)[0],
                          self._title_constructor(related_item)[0],
                          self._url(related_item)[0])

    def _title_constructor(self, el):
        """
        Just for reference, if a method is internal, i.e. only used to make
        other methods in your class easier and not for the outside world to
        bugger with, Python coders tend to prefix those with an underscore
        to let other coders know this is a helper. Python doesn't have a
        concept of private like a lot of languages do, so this convention is
        just a gentle reminder to others reading the code.

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
            non_sort=non_sort+' ' if non_sort else '',
            title=title if title else '',
            subtitle=': '+subtitle if subtitle else ''
        )

    def _get_text(self, el):
        """Wrapping common use of getattr for safe attribute access."""
        return getattr(el, 'text', None)

    def _physical_location(self, el):
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


def parse_xml(xml):
    try:
        return etree.parse(xml).getroot()
    except OSError:
        return etree.fromstring(xml)
