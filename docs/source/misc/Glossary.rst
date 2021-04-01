Glossary
========

.. glossary::

    compile
        In the context of ``httpsuite``, compiling means converting a :class:`Response` or :class:`Request` object into 
        another more useable type, typically either :class:`str` or :class:`bytes`. 

    message
        The parent object of both an HTTP request and response.

    modify
        In the context of ``httpsuite``, modifying means changing attributes in either the :class:`Request` or 
        :class:`Response` objects. When modifications are applied to these objects usually compilation follows. 

    parse
        In the context of ``httpsuite``, parsing means interpreting an external type and creating a representative
        :class:`Response` or :class:`Request` object.
