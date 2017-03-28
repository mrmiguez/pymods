from .record import *
from .exceptions import *
from .reader import *
from .constants import *

'''
# 
# Retaining for future OAI-PMH Reader/Record classes
#

class FSUDL(MODSReader):
    """
    Helper functions specific to Florida State
    University's DigiNole: http://diginole.lib.fsu.edu
    """

    def __init__(self, input_file=None):
        """
        MODS constructor class.
        input_file: file or directory of files to be accessed.
        """
        super(FSUDL, self).__init__(input_file)
        record_list = []
        for mods_record in self.root.iterfind('.//{0}mods'.format(nameSpace_default['mods'])):
            record_list.append(mods_record)
        self.record_list = record_list

    def purl_search(record):
        """
        Accesses record's Persistent URL from mods:mods/mods:location/mods:url:
        return: item PURL as string.
        """
        purl = re.compile('((http://purl)[\w\d:#@%/;$()~_?\+-=\\\.&]+)')
        for url in record.iterfind('./{0}location/{1}url'.format(nameSpace_default['mods'], nameSpace_default['mods'])):
            match = purl.search(url.text)
            if match:
                return match.group()

    def pid_search(record):
        """
        Get fedora PID from MODS record:
        return: item's fedora PID.
        """
        pid = re.compile('fsu:[0-9]+')
        for identifier in record.iterfind('.//{0}identifier'.format(nameSpace_default['mods'])):
            match = pid.search(identifier.text)
            if match:
                return match.group()

    def local_identifier(record):
        """
        Get DigiNole IID from MODS record:
        return: item's IID.
        """
        for identifier in record.iterfind('.//{0}identifier'.format(nameSpace_default['mods'])):
            if 'type' in identifier.attrib is not None:
                if 'IID' == identifier.attrib['type']:
                    return identifier.text

    def doi_search(record):
        """
        Get DigiNole IID from MODS record:
        return: item's IID.
        """
        for identifier in record.iterfind('.//{0}identifier'.format(nameSpace_default['mods'])):
            if 'type' in identifier.attrib is not None:
                if 'DOI' == identifier.attrib['type']:
                    return identifier.text


class OAI(MODSReader):
    """
    oai_dc elements are output wrappers from OAI-PMH feeds. This
    class provides access to those elements.

    Some implementations of the OAI-PMH standard do not include the
    default namespace for oai_dc. A future release will include a test
    for inclusion of the default namespace,and add it to the file when
    not present.
    """

    def __init__(self, input_file=None):
        """
        Constructor class for oai_dc namespace elements.
        input_file: file or directory of files to be accessed.
        """
        super(OAI, self).__init__(input_file)
        record_list = []

        if self.root.nsmap is not None:
            self.nsmap = self.root.nsmap

        if 'oai_dc' in self.nsmap:
            for oai_record in self.root.iterfind('.//{0}record'.format(nameSpace_default['oai_dc'])):
                record_list.append(oai_record)
            self.nsroot = 'oai_dc'
            self.set_spec = self.root.find('.//{0}setSpec'.format(nameSpace_default['oai_dc'])).text
            oai_id = self.root.find('.//{0}header/{0}identifier'.format(nameSpace_default['oai_dc'])).text
            oai_urn = ""
            for part in oai_id.split(':')[:-1]:
                oai_urn = oai_urn + ':' + part
            self.oai_urn = oai_urn.strip(':')

        elif 'repox' in self.nsmap:
            for oai_record in self.root.iterfind('.//{0}record'.format(nameSpace_default['repox'])):
                record_list.append(oai_record)
            self.nsroot = 'repox'
            self.set_spec = self.root.attrib['set']
            oai_id = self.root.find('./{0}record'.format(nameSpace_default['repox'])).attrib['id']
            oai_urn = ""
            for part in oai_id.split(':')[:-1]:
                oai_urn = oai_urn + ':' + part
            self.oai_urn = oai_urn.strip(':')

        elif nameSpace_default['mods'] in self.nsmap:
            return MODS(self)

        self.record_list = record_list

    def pid_search(self, record=None):
        """
        Get fedora PID from oai_dc wrapper:
        return: item's fedora PID.
        """
        pid = re.compile('fsu_[0-9]+')

        if record == None:
            for record in self.record_list:
                return self.pid_search(record)

        if self.nsroot == 'oai_dc':
            for identifier in record.iterfind('.//{0}identifier'.format(nameSpace_default['oai_dc'])):
                match = pid.search(identifier.text)
                if match:
                    return match.group().replace('_', ':')

        if self.nsroot == 'repox':
            return FSUDL.pid_search(record)

'''

