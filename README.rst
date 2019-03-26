Installing bobtemplates.affinitic
=================================

Développer le buildout et ses dépendances.

.. code-block:: bash
    $ make build

ou

.. code-block:: bash
    $ virtualenv-2.7 .
    $ bin/pip install -I -r requirements.txt
    $ bin/buildout

Lancer l'instance

.. code-block:: bash
    $ bin/instance fg


basic.plone.buildout
====================

``bobtemplates.affinitic`` provides a `mr.bob <http://mrbob.readthedocs.org/en/latest/>`_ template to generate packages for Affinitic Plone projects.


Call it from the ``src``-directory of your Plone project like this.::

    $ bin/mrbob -O your.package bobtemplates.affinitic:basic_plone_buildout


Installation a theme package
----------------------------

You can also install bobtemplates.plone with pip in a virtualenv. If you don't have an active virtualenv, you can create one inside your project directory.

.. code-block:: bash

    bin/mrbob -O plonetheme.name bobtemplates.affinitic:theme_package


Warning
-------

Currently, it is not possible to create a 3 part package name.
The name must be of type: plonetheme.name


Credits
=======

This package was developed by `Affinitic team <https://github.com/affinitic>`_.

.. image:: http://www.affinitic.be/affinitic_logo.png
   :alt: Affinitic website
   :target: http://www.affinitic.be

``bobtemplates.affinitic`` is licensed under GNU General Public License, version 2.
