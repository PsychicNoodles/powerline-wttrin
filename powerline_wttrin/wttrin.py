# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division,
                        absolute_import, print_function)
from collections import namedtuple

from powerline.lib.url import urllib_read, urllib_urlencode
from powerline.lib.threaded import KwThreadedSegment
from powerline.segments import with_docstring

base_url = 'https://wttr.in/%s?%s'

_WeatherSettings = namedtuple('Key', 'locations format')


class WeatherSegment(KwThreadedSegment):
    interval = 600

    @staticmethod
    def key(locations=None, format='3', **kwargs):
        if isinstance(locations, str):
            locations = [locations]
        return _WeatherSettings(tuple(locations), format)

    def compute_state(self, key):
        if key.locations == None:
            self.warn('No location provided')
        return urllib_read(base_url % (':'.join(key.locations), urllib_urlencode({'format': key.format})))

    @staticmethod
    def render_one(result, **kwargs):
        if not result:
            return None
        else:
            return [{
                'contents': result.rstrip(),
                'highlight_groups': ['weather']
            }]


weather = with_docstring(WeatherSegment(),
             ('''Return weather from wttr.in.

:param str or list[str] locations:
    weather location(s)
:param str format:
    wttr.in format

Highlight groups used: ``weather``
'''))
