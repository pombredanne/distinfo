from distinfo.collectors.findtests import FindTests

from .cases import TestCase


class TestFindTests(TestCase):

    collector = FindTests

    def test_collect(self, tmpdir):
        tmpdir.join("test.py").write("True")
        collector = self._collect(tmpdir)
        assert collector.ext.tests

    def test_collect_false(self, tmpdir):
        collector = self._collect(tmpdir)
        assert not hasattr(collector.ext, "tests")
