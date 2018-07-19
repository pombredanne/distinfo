from distinfo.collectors.requirementsfile import RequirementsFile

from .cases import TestCase


class TestRequirementsFile(TestCase):

    collector = RequirementsFile

    def test_collect(self, tmpdir):
        tmpdir.join("requirements-test.txt").write("aaa")
        collector = self._collect(tmpdir)
        assert {"aaa"} == collector.requires.test
