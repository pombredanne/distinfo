from distinfo.distribution import Distribution

from ..cases import TestCase as _TestCase


class TestCase(_TestCase):

    collector = None

    def _collect(self, source_dir, name=None, **kwargs):
        dist = Distribution()
        if name is not None:
            dist["name"] = name
        for req in kwargs.pop("reqs", []):
            dist.add_requirement(req)
        dist.ext.update(kwargs)
        collector = self.collector(dist, source_dir)  # pylint: disable=not-callable
        collector.collect()
        return collector
