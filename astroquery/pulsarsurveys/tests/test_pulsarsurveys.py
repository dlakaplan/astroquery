# Licensed under a 3-clause BSD style license - see LICENSE.rst
from contextlib import contextmanager
import os
import requests
import json
from astropy import coordinates
import pytest
from ...utils import commons
from ...utils.testing_tools import MockResponse
from ... import pulsarsurveys

DATA_FILES = {'query': 'pulsarsurveys.json',
              'dmquery': 'pulsarsurveys_dm.json'}

class MockResponsePulsarSurveys(MockResponse):

    def __init__(self, content, **kwargs):
        super(MockResponsePulsarSurveys, self).__init__(content, **kwargs)

    def iter_lines(self):
        for line in self.text.split("\n"):
            yield line

    def close(self):
        pass


@pytest.fixture
def patch_get(request):
    mp = request.getfixturevalue("monkeypatch")

    mp.setattr(requests, 'get', get_mockreturn)
    return mp

@pytest.fixture
def patch_get_readable_fileobj(request):
    @contextmanager
    def get_readable_fileobj_mockreturn(filename, **kwargs):
        file_obj = data_path(DATA_FILES['query'])  
        yield open(file_obj, 'r')  

    mp = request.getfixturevalue("monkeypatch")

    mp.setattr(commons, 'get_readable_fileobj',
               get_readable_fileobj_mockreturn)
    return mp


def get_mockreturn(url, params=None, timeout=10):
    filename = data_path(DATA_FILES['catalog'])
    content = open(filename, 'rb').read()
    return MockResponseAlfalfa(content)


def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    return os.path.join(data_dir, filename)


coords = coordinates.SkyCoord('0h8m05.63s +14d50m23.3s')

PulsarSurveys = pulsarsurveys.core.PulsarSurveys()

def test_pulsarsurveys_query(patch_get, patch_get_readable_fileobj, coords=coords):
    out = PulsarQueries.query_region(coords, 55)
    print(len(out))
    assert True
    
