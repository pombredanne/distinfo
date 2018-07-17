from pipreqs import pipreqs

from distinfo.collectors import PipReqs

from .cases import TestCase


class TestPipReqs(TestCase):

    collector = PipReqs

    def test_collect(self, tmpdir):
        tmpdir.join("xxx").mkdir().join("__init__.py") .write("import aaa")
        tmpdir.join("tests").mkdir().join("__init__.py") .write("import bbb")
        dist = self._collect(tmpdir)
        assert dist.ext.imports.xxx == {"aaa"}
        assert dist.ext.imports.tests == {"bbb"}

    def test_collect_empty(self, tmpdir):
        dist = self._collect(tmpdir)
        assert not hasattr(dist.ext, "imports")

    def test_collect_fail(self, monkeypatch, tmpdir):
        tmpdir.join("xxx").mkdir().join("__init__.py") .write("import aaa")
        def _raiser(_p):
            raise Exception()
        monkeypatch.setattr(pipreqs, "get_pkg_names", _raiser)
        dist = self._collect(tmpdir)
        assert not dist.ext.imports.xxx
