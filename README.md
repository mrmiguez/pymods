# pymods [![Build Status](https://travis-ci.org/mrmiguez/pymods.svg?branch=master)](https://travis-ci.org/mrmiguez/pymods)

pymods is utility module for working with the Library of Congress's MODS XML standard: Metadata Description Schema (MODS). It is a utility wrapper for the lxml module specific to deserializing data out of MODSXML into python data types.

If you need a module to serialize data into MODSXML, see the other [pymods by Matt Cordial](https://github.com/cordmata/pymods).

## Installing

## Using

### Basics

XML is parsed using either the MODS or OAI class:

`mods_records = MODS('some_file.xml')`

`oai_records = OAI('some_file.xml')`

Individual records are stored at the MODS or OAI object in the record_list attribute. These records can be called individually by index number or used as an iterator.

```python
for record in mods_records.record_list:
   print(MODS.rights(record))
```
```python
print(MODS.rights(oai_records.record_list[3]))
```
    
#### MODS

The MODS class parses records at each `mods:mods` element. It will work with `mods:modsCollection` documents, outputs from OAI-PMH feeds, or individual MODSXML documents with `mods:mods` as the root element.

When parsing only a single record, the MODS and OAI classes will still store the record in the record_list attribute. Accessing the record will still require calling the object as an iterator or by list index.

#### OAI

The OAI class can be used with the output from OAI-PMH feeds or repox exports. `oai_dc:record` elements are parsed as the record root elements in documents in the oai_dc namespace. Documents in the repox namespace are parsed using `repox:record` as the record root element.
    
### Methods

All functions return data either as a string, list, or dict. See the appropriate docstrings for details.

### FSUDL

Methods in the FSUDL class are helper functions specific to Florida State University's [DigiNole](http://diginole.lib.fsu.edu) and might not apply to records from other sources.

## Examples

Importing
```python
from pymods import MODS, FSUDL, OAI
```

Parsing a file
```python
>>> mods = MODS('example.xml')

>>> len(mods.record_list)
3
```

### Simple tasks

Generating a title list
```python
In [14]: for record in mods.record_list:
   ....:     print(MODS.title_constructor(record))
   ....:
['Fire Line System']
['$93,668.90. One Mill Tax Apportioned by Various Ways Proposed']
['Broward NOW News: National Organization for Women, February 1987']
```

Creating a subject list
```python
In [17]: for record in mods.record_list:
   ....:     for subject in MODS.subject_constructor(record):
   ....:         print(subject)
   ....:
Concert halls
Architecture
Architectural drawings
Structural systems
Structural systems drawings
Structural drawings
Safety equipment
Construction
Mechanics
Structural optimization
Architectural design
Fire prevention--Safety measures
7013143
Taxes
Tax payers
Tax collection
Organizations
Feminism
Sex discrimination against women
Women's rights
Equal rights amendments
2020598
Women--Societies and clubs
National Organization for Women
```

### More complex tasks

Creating a list of subject URI's only for LCSH subjects
```python
In [18]: for record in mods.record_list:
   ....:     for subject in MODS.subject(record):
   ....:         if 'authority' in subject.keys() and 'lcsh' == subject['authority']:
   ....:             print(subject['valueURI'])
   ....:
http://id.loc.gov/authorities/subjects/sh85082767
http://id.loc.gov/authorities/subjects/sh88004614
http://id.loc.gov/authorities/subjects/sh85132810
http://id.loc.gov/authorities/subjects/sh85147343
```

Get URLs for objects using a No Copyright US rightsstatement.org URI
```python
In [23]: for record in mods.record_list:
   ....:     if MODS.rights(record)['URI'] == 'http://rightsstatements.org/vocab/NoC-US/1.0/':
   ....:         print(FSUDL.purl_search(record))
   ....:
http://purl.flvc.org/fsu/fd/FSU_MSS0204_B01_F10_09
http://purl.flvc.org/fsu/fd/FSU_MSS2008003_B18_F01_004
```