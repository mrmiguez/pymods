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


