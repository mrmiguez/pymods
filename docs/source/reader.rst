pymods.reader Module
====================

Custom pymods lxml parsers.

:pymods.MODSReader: Instantiates the pymods.MODSRecord class. Iterates over mods.mods elements.
Many properties of the MODSRecord class return namedtuples. Named aliases correspond to attributes and features
of the parent XML element.

:pymods.OAIReader: Instantiates the pymods.OAIRecord class. Iterates record elements in any namespace.

.. toctree::
    :maxdepth: 2
    :caption: pymods.reader:

.. autoclass:: pymods.Reader
    :members:
    :show-inheritance:
    :undoc-members:

.. autoclass:: pymods.MODSReader
    :members:
    :show-inheritance:
    :undoc-members:

.. autoclass:: pymods.OAIReader
    :members:
    :show-inheritance:
    :undoc-members:
