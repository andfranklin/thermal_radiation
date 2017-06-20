|Travis|_ |PyPi|_ |ReadDocs|_ |Pyup|_

.. |PyPi| image:: https://img.shields.io/pypi/v/thermal_radiation.svg
        :target: https://pypi.python.org/pypi/thermal_radiation

.. |Travis| image:: https://img.shields.io/travis/andfranklin/thermal_radiation.svg
        :target: https://travis-ci.org/andfranklin/thermal_radiation

.. |ReadDocs| image:: https://readthedocs.org/projects/thermal-radiation/badge/?version=latest
        :target: https://thermal-radiation.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. |Pyup| image:: https://pyup.io/repos/github/andfranklin/thermal_radiation/shield.svg
     :target: https://pyup.io/repos/github/andfranklin/thermal_radiation/
     :alt: Updates

=================
Thermal Radiation
=================

A framework to aid in the analysis of thermal networks involving thermal radiation.


* Free software: MIT license
* Documentation: https://thermal-radiation.readthedocs.io.


Features
--------

* Analytic functions to calculate view factors for various geometries and configurations [1]_.
* Framework to calculate grey body factors and Radk's in a thermal network using Gebhart's method [2]_ [3]_.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

References
----------

.. [1] `Form Factor Catalog`_ffc

.. _ffc: http://www.thermalradiation.net/tablecon.html

.. [2] `Form Factors, Grey Bodies and Radiation Conductances (Radks) by Steven L. Rickman`_rickman

.. _rickman https://tfaws.nasa.gov/TFAWS12/Proceedings/Form%20Factors%20Grey%20Bodies%20and%20Radks%20Course.pdf

.. [3] `Gebhart Factor's`_gebhart

.. _gebhart https://en.wikipedia.org/wiki/Gebhart_factor
