from distinfo import Requirement
from distinfo.collectors import EggInfo

from .cases import TestCase


class TestEggInfo(TestCase):

    collector = EggInfo

    def test_collect(self):
        source_dir = self.data_path / "test.dist"
        req = Requirement.from_source(source_dir)
        dist = self._collect(source_dir, req=req)
        assert dist.name == "test.dist"
