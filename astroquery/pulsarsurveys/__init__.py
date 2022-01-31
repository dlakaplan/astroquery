from astropy import config as _config

class Conf(_config.ConfigNamespace):
    """
    Configuration parameters for `astroquery.template_module`.
    """
    server = _config.ConfigItem(
        ['http://pulsar.cgca-hub.org/api',
         ],
        'Name of the pulsar survey scraper server to use.'
        )
    timeout = _config.ConfigItem(
        30,
        'Time limit for connecting to pulsar survey scraper server.'
        )

conf = Conf()

from .core import PulsarSurveys

__all__ = ['PulsarSurveys', 'conf']
