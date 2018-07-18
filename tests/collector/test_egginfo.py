from distinfo.collectors import EggInfo
from distinfo.requirement import parse_requirement

from .cases import TestCase


class TestEggInfo(TestCase):

    collector = EggInfo

    def test_collect(self):
        source_dir = self.data_path / "test.dist"
        req = parse_requirement(source_dir)
        dist = self._collect(source_dir, req=req)
        assert dist.name == "test.dist"
