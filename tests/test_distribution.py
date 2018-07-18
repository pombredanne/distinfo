from pip._vendor.packaging.requirements import InvalidRequirement

import pytest

from setuptools import sandbox

from distinfo.distribution import Distribution
from distinfo.exc import DistInfoException

from .cases import TestCase


class TestDistribution(TestCase):

    def dist(self, name):
        return Distribution.from_source(self.data_path / name)

    def test_repr(self):
        dist = Distribution()
        assert "Distribution" in repr(dist)

    def test_add_requirement(self):
        dist = Distribution()
        dist.add_requirement("xxx")
        assert {"xxx"} == dist.requires_dist
        assert {"xxx"} == dist.requires.run
        dist.add_requirement("yyy", extra=":python_version > '1'")
        assert len(dist.requires.run) == 2

    def test_bad_requirement(self, caplog):
        dist = Distribution()
        dist.add_requirement("-cxxx")
        assert len(caplog.records) == 1
        assert "InvalidRequirement" in caplog.text

    def test_bad_setup(self, monkeypatch):
        # pylint: disable=protected-access
        name = "test.dist"
        original = sandbox._execfile
        monkeypatch.setattr(sandbox, "_execfile", self._make_raiser(BaseException))
        pytest.raises(DistInfoException, self.dist, name)
        monkeypatch.setattr(sandbox,
                            "_execfile",
                            self._make_raiser(BaseException, function=original))
        self.dist(name)

    def test_requires(self, caplog):
        dist = Distribution(requires_dist=["xxx", "asdasd; d"])
        assert {"xxx"} == dist.requires.run
        assert len(caplog.records) == 1
        assert "InvalidRequirement" in caplog.text
