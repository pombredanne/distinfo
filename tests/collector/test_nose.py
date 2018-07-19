from distinfo.collectors.nose import Nose

from .cases import TestCase


class TestNose(TestCase):

    collector = Nose

    def test_collect(self, tmpdir):
        tmpdir.join(".noserc").write("x")
        collector = self._collect(tmpdir)
        assert {"nose"} == collector.requires.test
