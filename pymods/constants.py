"""
Various lists and dicts needed for parsers and record classes. Stored here for convenience.
"""

NAMESPACES = {'oai_dc': '{http://www.openarchives.org/OAI/2.0/}',
              'dc': '{http://purl.org/dc/elements/1.1/}',
              'mods': '{http://www.loc.gov/mods/v3}',
              'dcterms': '{http://purl.org/dc/terms}',
              'xlink': '{http://www.w3.org/1999/xlink}',
              'repox': '{http://repox.ist.utl.pt}'}

DATE_FIELDS = ['{0}dateIssued'.format(NAMESPACES['mods']),
               '{0}dateCreated'.format(NAMESPACES['mods']),
               '{0}copyrightDate'.format(NAMESPACES['mods']),
               '{0}dateOther'.format(NAMESPACES['mods'])]

NS_MAP = {'mods': 'http://www.loc.gov/mods/v3',
          'xlink': 'http://www.w3.org/1999/xlink',
          'flvc': 'info:flvc/manifest/v1'}
