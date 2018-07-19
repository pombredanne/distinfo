from pipreqs import pipreqs

from distinfo.collectors.pipreqs import PipReqs

from .cases import TestCase

PACKAGE = """
import aaa
"""

TESTS = """
import xxx
import bbb
"""


class TestPipReqs(TestCase):

    collector = PipReqs

    def test_collect(self, caplog, tmpdir):
        tmpdir.join("xxx").mkdir().join("__init__.py") .write(PACKAGE)
        tmpdir.join("tests").mkdir().join("__init__.py") .write(TESTS)
        collector = self._collect(
            tmpdir,
            name="xxx",
            packages=["xxx", "tests"],
            tests=["tests"],
        )
        assert collector.ext.imports.xxx == {"aaa"}
        assert collector.ext.imports.tests == {"bbb"}
        assert "missing run dependencies" in caplog.text
        assert "missing test dependencies" in caplog.text

    def test_collect_empty(self, tmpdir):
        collector = self._collect(tmpdir)
        assert not hasattr(collector.ext, "imports")

    def test_collect_fail(self, monkeypatch, tmpdir):
        tmpdir.join("xxx").mkdir().join("__init__.py") .write("import aaa")
        monkeypatch.setattr(pipreqs, "get_pkg_names", self._raiser())
        collector = self._collect(tmpdir, packages=["xxx"])
        assert not collector.ext.imports
