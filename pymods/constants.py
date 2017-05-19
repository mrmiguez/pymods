NAMESPACES = {'oai_dc': '{http://www.openarchives.org/OAI/2.0/oai_dc/}',
              'dc': '{http://purl.org/dc/elements/1.1/}',
              'mods': '{http://www.loc.gov/mods/v3}',
              'dcterms': '{http://purl.org/dc/terms}',
              'xlink': '{http://www.w3.org/1999/xlink}',
              'repox': '{http://repox.ist.utl.pt}'}

DATE_FIELDS = ['{0}dateIssued'.format(NAMESPACES['mods']),
               '{0}dateCreated'.format(NAMESPACES['mods']),
               '{0}copyrightDate'.format(NAMESPACES['mods']),
               '{0}dateOther'.format(NAMESPACES['mods'])]
