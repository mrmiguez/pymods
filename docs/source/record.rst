pymods.record Module
====================

Custom pymods lxml parsers.

:pymods.MODSReader: Instantiates the pymods.MODSRecord class. Iterates over mods.mods elements.
Many properties of the MODSRecord class return namedtuples. Named aliases correspond to attributes and features
of the parent XML element.

:pymods.OAIReader: Instantiates the pymods.OAIRecord class. Iterates record elements in any namespace.

:pymods.DCRecord: Basic functions for accessing elements in the Dublin Core and Qualified Dublin Core namespaces.

.. toctree::
    :maxdepth: 2
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
