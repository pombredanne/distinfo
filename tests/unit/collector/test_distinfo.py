import pytest

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
    setup_requires=["setuptools"],
    install_requires=["bbb"],
    # badly specified requirements, seen in unittest2
    tests_require=(["ccc"],),
    extras_require=dict(test="ddd"),
)
"""


class TestDistInfo(Case):

    collector = distinfo.DistInfo

    def _collect_check(self, tmpdir):
        collector = self._collect(tmpdir)
        assert not collector.requires.build
        assert {"bbb"} == collector.requires.run
        assert {"ccc", "ddd"} == collector.requires.test
        assert ["xxx"] == collector.ext.packages
        assert ["yyy"] == collector.ext.modules

    def test_collect(self, tmpdir):
        self._write_setup(tmpdir, SETUP)
        tmpdir.join("xxx").mkdir().join("__init__.py").write("")
        self._collect_check(tmpdir)
        # run a second time to hit the "-h" branch
        self._collect_check(tmpdir)

    def test_collect_empty(self, caplog, tmpdir):  # pylint: disable=arguments-differ
        super().test_collect_empty(tmpdir)
        assert "has no %s" % const.SETUP_PY in caplog.text

    def test_run_egg_info_fail(self, caplog, monkeypatch, tmpdir):
        monkeypatch.setattr(distinfo, "run_setup", self._raiser())
        self._write_setup(tmpdir, SETUP)
        pytest.raises(Exception, self._collect, tmpdir)
        assert "setup failure" in caplog.text
