from urllib.parse import parse_qs, urlparse

from .trackers import TrackerMixin


class MagnetQuery:
    def __init__(self, query):
        if isinstance(query, str):
            self._query = parse_qs(query)
        else:
            self._query = query
        self.display_name = self._query.get('dn')
        self.exact_length = self._query.get('xl')
        self.exact_topic = self._query.get('xt')
        self.web_seed = self._query.get('ws')
        self.acceptable_source = self._query.get('as')
        self.exact_source = self._query.get('xs')
        self.keyword_topic = self._query.get('kt')
        self.manifest_topic = self._query.get('mt')
        self.address_tracker = self._query.get('tr')

    def build(self):
        data = {
            'dn': self.display_name,
            'xl': self.exact_length,
            'xt': self.exact_topic,
            'ws': self.web_seed,
            'as': self.acceptable_source,
            'xs': self.exact_source,
            'kt': self.keyword_topic,
            'mt': self.manifest_topic,
            'tr': self.address_tracker,
        }
        return {key: value for key, value in data.items() if value is not None}

    @property
    def trackers(self):
        return [TrackerMixin(tracker) for tracker in self.address_tracker]


def parse_magnet(magnet_url):
    parsed = urlparse(magnet_url)
    query = parse_qs(parsed.query)
    return {
        'scheme': parsed.scheme,
        'query': query,
    }