from distinfo.collectors.pep518 import Pep518

from .cases import TestCase

SETUP = """
from setuptools import setup
setup()
"""

PYPROJECT = """
[build-system]
requires = ["zzz"]

[tool.flit.metadata]
requires=["yyy"]
dev-requires=["xxx"]
"""


class TestPep518(TestCase):

    collector = Pep518

    def test_collect(self, tmpdir):
        tmpdir.join("setup.py").write(SETUP)
        tmpdir.join("pyproject.toml").write(PYPROJECT)
        collector = self._collect(tmpdir)
        assert {"zzz"} == collector.requires.build
        assert {"yyy"} == collector.requires.run
        assert {"xxx"} == collector.requires.dev
