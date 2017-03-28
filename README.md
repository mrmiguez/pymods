# pymods [![Build Status](https://travis-ci.org/mrmiguez/pymods.svg?branch=master)](https://travis-ci.org/mrmiguez/pymods)

pymods is utility module for working with the Library of Congress's MODS XML standard: Metadata Description Schema (MODS). It is a utility wrapper for the lxml module specific to deserializing data out of MODSXML into python data types.

If you need a module to serialize data into MODSXML, see the other [pymods by Matt Cordial](https://github.com/cordmata/pymods).

## Installing

Recommended:

`pip install pymods`

## Using

### Basics

XML is parsed using the MODSReader class:

`mods_records = pymods.MODSReader('some_file.xml')`

Individual records are stored as an iterator of the MODSRecord object:

```python
In [3]: len(mods_records)
Out[3]: 3
```
```python
In [5]: for record in mods_records:
  ....:    print(record)
  ....:
<Element Record at 0x6fffe5d50e8>
<Element Record at 0x6fffe5d5188>
<Element Record at 0x6fffe5d5228>

```

Or they can be accessed invidually through the the MODSReader.record_list attribute:

```python
In [8]: print(mods_records.record_list[0].title_constructor())
['Fire Line System']
```

MODSReader will work with `mods:modsCollection` documents, outputs from OAI-PMH feeds, or individual MODSXML documents with `mods:mods` as the root element. When parsing only a single record, the MODSReader class will still store the record in the record_list attribute. Accessing the record will still require calling the object as an iterator or by list index.
    
#### pymods.Record

The MODSReader class parses each `mods:mods` element into a pymods.Record object. pymods.Record is a custom wrapper class for the lxml.ElementBase class. All children of pymods.Record inherit the lxml._Element and lxml.ElementBase methods. 

### Methods

All functions return data either as a string, list, or dict. See the appropriate docstrings for details.

## Examples

Importing
```python
from pymods import MODSReader, Record
```

Parsing a file
```python
>>> mods = MODSReader('example.xml')

>>> len(mods)
3
```

### Simple tasks

Generating a title list
```python
In [14]: for record in mods:
   ....:     print(record.title_constructor())
   ....:
['Fire Line System']
['$93,668.90. One Mill Tax Apportioned by Various Ways Proposed']
['Broward NOW News: National Organization for Women, February 1987']
```

Creating a subject list
```python
In [17]: for record in mods:
   ....:     for subject in record.subject_constructor():
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
In [18]: for record in mods:
   ....:     for subject in record.subject():
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
In [23]: for record in mods:
   ....:     if record.rights()['URI'] == 'http://rightsstatements.org/vocab/NoC-US/1.0/':
   ....:         print(record.purl_search())
   ....:
http://purl.flvc.org/fsu/fd/FSU_MSS0204_B01_F10_09
http://purl.flvc.org/fsu/fd/FSU_MSS2008003_B18_F01_004
```