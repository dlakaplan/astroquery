.. doctest-skip-all

.. _astroquery.pulsarsurveys:

Pulsar Survey Scraper Queries (`astroquery.pulsarsurveys`)
======================================

Getting started
---------------

This example shows how to perform an search of the pulsar survey scraper:

.. code-block:: python

    >>> from astroquery.pulsarsurveys import PulsarSurveys
    >>> from astropy import coordinates as coords
    >>> pos = coords.SkyCoord('0h8m05.63s +14d50m23.3s')
    >>> pulsars = PulsarSurveys.query_region(pos, radius=5)

This retrieves the pulsars within 5 degrees of the given position as
an `astropy.Table`.

You can further specify a central DM and tolerance to search:

.. code-block:: python

    >>> pulsars = PulsarSurveys.query_region(pos, radius=5, dm=30, dmtolerance=10)



Reference/API
-------------

.. automodapi:: astroquery.pulsarsurveys
    :no-inheritance-diagram:
