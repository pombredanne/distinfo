from distinfo.distribution import Distribution

from ..cases import Case as _Case


class Case(_Case):

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

    def test_collect_empty(self, tmpdir):
        collector = self._collect(tmpdir)
        assert not collector.requires
        return collector
