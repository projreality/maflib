MAFLib
======

.. contents:: Table of Contents
  :local:

MAFLib is a library for reading and manipulating Mozilla Archive Format (MAF) files.

Installation
------------

Package is uploaded on `PyPI <https://pypi.org/project/maflib>`_.

You can install it with pip::

  $ pip install maflib

Usage
-----

Open a .maff file

.. code:: python

  fd = maflib.MAF("test.maff")

Open a file within the .maff file

.. code:: python

  fd2 = fd.open("image.jpg")

Open the index file in the .maff file

.. code:: python

  fd2 = fd.open_index()

Return the content of the index file in the .maff file

.. code:: python

  content = fd.read_index()

Show a .maff file in a browser window

.. code:: python

  fd.show()

License
-------

MAFLib is released under the GNU Lesser General Public License, Version 3.
