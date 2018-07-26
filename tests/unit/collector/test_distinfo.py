from distinfo import const
from distinfo.collectors import distinfo

from .cases import Case

SETUP = """
from setuptools import setup, find_packages
setup(
    packages=find_packages(),
    py_modules=["yyy"],
    # setup_requires packages must be present or distutils will barf, so we
    # use one that definitely is here
    setup_requires=["zzz"],
    # badly specified requirements, seen in unittest2
    tests_require=(["ccc"],),
)
"""


class TestDistInfo(Case):

    collector = distinfo.DistInfo

    def test_collect(self, tmpdir):
        self._write_setup(tmpdir, SETUP)
        tmpdir.join("xxx").mkdir().join("__init__.py").write("")
        collector = self._collect(tmpdir)
        assert {"zzz"} == collector.requires.build
        assert {"ccc"} == collector.requires.test
        assert ["xxx"] == collector.ext.packages
        assert ["yyy"] == collector.ext.modules

    def test_collect_empty(self, caplog, tmpdir):  # pylint: disable=arguments-differ
        super().test_collect_empty(tmpdir)
        assert "has no %s" % const.SETUP_PY in caplog.text
