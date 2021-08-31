########
Versions
########

******
``v1``
******

``1.2.0``
=========
  * Organized project.

``1.1.0``
=========
  * Revamped and cleaned the codebase.
  * Update documentation.

``1.0.6``
=========
  * Updated core ``Message`` to include ``protocol`` by default. 
  * Removed ``info.py`` and place content inside ``__init__.py``.
  * Formatted some tests with Black.

``1.0.5``
=========
  * Fixed documentation bug relating to ``sphinx_rtd_theme``.

``1.0.4``
=========
  * Fixed documentation bug relating to ``m2r``.

``1.0.3``
=========
  * Fixed PyLint errors.
  * Added ``__bool__`` to ``Item`` for accurate comparissons (i.e. ``if request.body`` will return ``False`` when no body exists).
  * Modified ``Message._compile`` input param ``format`` to ``frmt``.

``1.0.2``
=========
  * Cleaned up imports and codebase.

``1.0.1``
=========
  * Cleaned up imports and codebase.

``1.0.0``
=========
  * Initial commit.
