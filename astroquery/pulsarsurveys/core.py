# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Author: David Kaplan
Affiliation: University of Wisconsin-Milwaukee
Email: kaplan@uwm.edu
"""

# put all imports organized as shown below
# 1. standard library imports
import json
import numpy as np

# 2. third party imports
import astropy.units as u
import astropy.coordinates as coord
from astropy.table import Table, Column, MaskedColumn

# 3. local imports - use relative imports
# commonly required local imports shown below as example
# all Query classes should inherit from BaseQuery.
from ..query import BaseQuery
# has common functions required by most modules
from ..utils import commons
# prepend_docstr is a way to copy docstrings between methods
from ..utils import prepend_docstr_nosections
# async_to_sync generates the relevant query tools from _async methods
from ..utils import async_to_sync
# import configurable items declared in __init__.py
from . import conf


# export all the public classes and methods
__all__ = ['PulsarSurveys', 'PulsarSurveysClass']

# declare global variables and constants if any


# Now begin your main class
# should be decorated with the async_to_sync imported previously
@async_to_sync
class PulsarSurveysClass(BaseQuery):

    """
    Not all the methods below are necessary but these cover most of the common
    cases, new methods may be added if necessary, follow the guidelines at
    <http://astroquery.readthedocs.io/en/latest/api.html>
    """
    # use the Configuration Items imported from __init__.py to set the URL,
    # TIMEOUT, etc.
    URL = conf.server
    TIMEOUT = conf.timeout

    # all query methods are implemented with an "async" method that handles
    # making the actual HTTP request and returns the raw HTTP response, which
    # should be parsed by a separate _parse_result method.   The query_object
    # method is created by async_to_sync automatically.  It would look like
    # this:
    """
    def query_object(object_name, get_query_payload=False)
        response = self.query_object_async(object_name,
                                           get_query_payload=get_query_payload)
        if get_query_payload:
            return response
        result = self._parse_result(response, verbose=verbose)
        return result
    """

    # For services that can query coordinates, use the query_region method.
    # The pattern is similar to the query_object method. The query_region
    # method also has a 'radius' keyword for specifying the radius around
    # the coordinates in which to search. If the region is a box, then
    # the keywords 'width' and 'height' should be used instead. The coordinates
    # may be accepted as an `astropy.coordinates` object or as a string, which
    # may be further parsed.

    # similarly we write a query_region_async method that makes the
    # actual HTTP request and returns the HTTP response

    def query_region_async(self, coordinates, radius, dm=None,
                           dmtolerance=10,
                           get_query_payload=False, cache=True):
        """
        Queries a region around the specified coordinates.

        Parameters
        ----------
        coordinates : str or `astropy.coordinates`.
            coordinates around which to query
        radius : str or `astropy.units.Quantity`.
            the radius of the cone search
        dm : float or  `astropy.units.Quantity`, optional
            DM to restrict searches
        dmtolerance : float or  `astropy.units.Quantity`, optional
            Range of DM to restrict searches
        get_query_payload : bool, optional
            Just return the dict of HTTP request parameters.
        verbose : bool, optional
            Display VOTable warnings or not.

        Returns
        -------
        response : `requests.Response`
            The HTTP response returned from the service.
            All async methods should return the raw HTTP response.
        """
        request_payload = self._args_to_payload(coordinates=coordinates, radius=radius, dm=dm, dmtolerance=dmtolerance)
        if get_query_payload:
            return request_payload
        response = self._request('GET', self.URL, params=request_payload,
                                 timeout=self.TIMEOUT, cache=cache)
        return response

    # as we mentioned earlier use various python regular expressions, etc
    # to create the dict of HTTP request parameters by parsing the user
    # entered values. For cleaner code keep this as a separate private method:

    def _args_to_payload(self, *args, **kwargs):
        request_payload = dict()
        request_payload['type']='search'
        coordinates = commons.parse_coordinates(kwargs['coordinates'])

        ra = coordinates.ra.degree
        dec = coordinates.dec.degree
        dr = coord.Angle(kwargs['radius']).deg

        request_payload['ra'] = ra
        request_payload['dec'] = dec
        request_payload['radius'] = dr

        if kwargs['dm'] is not None:
            request_payload['dm'] = float(kwargs['dm'])
            request_payload['dmtol'] = float(kwargs['dmtolerance'])

        return request_payload

    # the methods above call the private _parse_result method.
    # This should parse the raw HTTP response and return it as
    # an `astropy.table.Table`. Below is the skeleton:

    def _parse_result(self, response, verbose=False):
        # if verbose is False then suppress any VOTable related warnings
        if not verbose:
            commons.suppress_vo_warnings()
        # try to parse the result into an astropy.Table, else
        # return the raw result with an informative error message.
        output = response.json()
        try:
            columns=['PSR',
                     'RA',
                     'Dec',
                     'P',
                     'DM',
                     'survey',
                     'retrieval date',
                     'Distance']
            units = [None,
                     u.deg,
                     u.deg,
                     u.ms,
                     u.pc/u.cm**3,
                     None,
                     None,
                     u.deg]
            
            data = {}
            for col in columns:
                data[col] = []                
                
            for key in output.keys():
                if key in ['searchra','searchdec','searchrad','searchcoord','searchdm','searchdmtolerance','nmatches']:
                    continue
                data['PSR'].append(key)
                data['RA'].append(output[key]['ra']['value'])
                data['Dec'].append(output[key]['dec']['value'])
                data['P'].append(output[key]['period']['value'])
                data['DM'].append(output[key]['dm']['value'])
                data['survey'].append(output[key]['survey']['value'])
                data['retrieval date'].append(output[key]['date']['value'])
                data['Distance'].append(output[key]['distance']['value'])
            
            columndata = {}
            for col, unit in zip(columns, units):
                if col in ['P', 'DM']:
                    columndata[col] = MaskedColumn(data[col], name=col, unit=unit, mask=np.array(data[col])<0)
                else:
                    columndata[col] = Column(data[col], name=col, unit=unit)
    
            responsetable = Table(columndata)
            for key in output.keys():
                if key in ['searchra','searchdec','searchrad','searchcoord','searchdm','searchdmtolerance']:
                    responsetable.meta[key] = output[key]['value']
            responsetable.sort('Distance')
            return responsetable

        except ValueError:
            # catch common errors here, but never use bare excepts
            # return raw result/ handle in some way
            pass

        return Table()



# the default tool for users to interact with is an instance of the Class
PulsarSurveys = PulsarSurveysClass()

# once your class is done, tests should be written
# See ./tests for examples on this

# Next you should write the docs in astroquery/docs/module_name
# using Sphinx.
