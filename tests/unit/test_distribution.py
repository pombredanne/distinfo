import importlib

from distinfo import config
from distinfo.distribution import Distribution
from distinfo.requirement import Requirement

from .cases import Case


class DummyCollector:

    def __init__(self, dist, _source_dir):
        self.dist = dist

    def collect(self):
        self.dist.name = "xxx"


class DummyModule:

    DummyCollector = DummyCollector


class TestDistribution(Case):

    def test_repr(self):
        dist = Distribution()
        assert "Distribution" in repr(dist)

    def test_add_requirement(self):
        dist = Distribution()
        dist.add_requirement("xxx")
        dist.add_requirement(Requirement("xxx"))
        assert {"xxx"} == dist.requires.run
        dist.add_requirement("xxx", extra="test")
        assert {"xxx"} == dist.requires.run
        assert not hasattr(dist.requires, "test")
        dist.add_requirement("yyy", extra="test")
        assert {"yyy"} == dist.requires.test

    def test_add_requirement_merge_specifiers(self):
        dist = Distribution()
        dist.add_requirement("xxx>=1")
        assert {"xxx"} == dist.requires.run
        req = dist.add_requirement("xxx<=2")
        assert req.specifier == "<=2,>=1"

    def test_add_requirement_merge_markers(self):
        dist = Distribution()
        req = dist.add_requirement("xxx; python_version > '1'")
        assert req.marker is not None
        req = dist.add_requirement("xxx")
        assert req.marker is not None
        req = dist.add_requirement("xxx; python_version < '2'")
        assert str(req.marker) == 'python_version > "1" and python_version < "2"'

    def test_add_requirement_merge_extra_marker(self):
        req = Requirement("xxx; python_version > '1'")
        dist = Distribution()
        req = dist.add_requirement(req, extra=":python_version < '2'")
        assert str(req.marker) == 'python_version > "1" and python_version < "2"'

    def test_add_requirement_invalid(self, caplog):
        dist = Distribution()
        dist.add_requirement("-cxxx")
        assert "InvalidRequirement" in caplog.text

    def test_add_requirement_invalid_marker(self, caplog):
        dist = Distribution()
        dist.add_requirement("xxx", extra=":xxx == '1'")
        assert "InvalidMarker" in caplog.text

    def test_requires(self, caplog):
        dist = Distribution(
            requires_dist=[
                "xxx",
                "asdasd; d",
                "yyy; extra == 'aaa' and python_version < '1'",
            ],
            provides_extra=["yyy"],
        )
        assert {"xxx"} == dist.requires.run
        assert not hasattr(dist.requires, "yyy")
        assert "InvalidRequirement" in caplog.text

    def test_from_source_dummy_collect(self, monkeypatch, tmpdir):
        monkeypatch.setitem(config.cfg, "collectors", ["DummyCollector"])
        monkeypatch.setattr(importlib, "import_module", lambda _x: DummyModule())
        self._write_setup(tmpdir)
        dist = Distribution.from_source(tmpdir)
        assert dist.name == "xxx"

    def test_from_source_no_collect(self, caplog, monkeypatch, tmpdir):
        monkeypatch.setitem(config.cfg, "collectors", [])
        self._write_setup(tmpdir)
        dist = Distribution.from_source(tmpdir)
        assert dist.name == "UNKNOWN"
        assert "metadata unavailable" in caplog.text
