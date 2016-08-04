#!/usr/bin/env python3
from lxml import etree
from modstools import mods_typeOfResource

NS = {'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/', 'dc': 'http://purl.org/dc/elements/1.1/', 'mods': 'http://www.loc.gov/mods/v3', 'dcterms': 'http://purl.org/dc/terms'}
tree = etree.parse('fsu_cookbooksandherbals.xml')
root = tree.getroot()
for record in root.iterfind('.//{%s}mods' % NS['mods']):
	print(mods_typeOfResource(record, NS))
