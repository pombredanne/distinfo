from distinfo import Distribution

from ..cases import TestCase as _TestCase


class TestCase(_TestCase):

    collector = None

    def _collect(self, source_dir, req=None):
        dist = Distribution(name="xxx")
        collector = self.collector(dist, source_dir, req=req)  # pylint: disable=not-callable
        collector.collect()
        return dist
