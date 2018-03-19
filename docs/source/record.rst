pymods.record Module
====================

Custom pymods record classes.

**pymods.MODSRecord**

Defines functions and properties for deserializing MODSXML data into python data types.
Many properties of the MODSRecord class return namedtuples. Named aliases correspond to attributes and features
of the parent XML element.

**pymods.OAIRecord**

Provides convenience functions for accessing OAI-PMH record metadata in a variety of namespaces.

**pymods.DCRecord**

Basic functions for accessing elements in the Dublin Core and Qualified Dublin Core namespaces.

.. toctree::
    :maxdepth: 4
    :caption: pymods.record:

.. autoclass:: pymods.Record
    :members:
    :show-inheritance:
    :undoc-members:

.. autoclass:: pymods.MODSRecord
    :members:
    :show-inheritance:
    :undoc-members:

.. autoclass:: pymods.OAIRecord
    :members:
    :show-inheritance:
    :undoc-members:

.. autoclass:: pymods.DCRecord
    :members:
    :show-inheritance:
    :undoc-members:
