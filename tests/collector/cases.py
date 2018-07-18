from distinfo.distribution import Distribution

from ..cases import TestCase as _TestCase


class TestCase(_TestCase):

    collector = None

    def _collect(self, source_dir, req=None, **kwargs):
        dist = Distribution(name="xxx")
        dist.ext.update(kwargs)
        collector = self.collector(dist, source_dir, req=req)  # pylint: disable=not-callable
        collector.collect()
        return dist
