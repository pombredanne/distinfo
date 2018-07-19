from distinfo.collectors import distinfo

from .cases import TestCase

SETUP = """
from setuptools import setup
setup(
    # this needs to be present or distutils barfs
    setup_requires=["setuptools"],
    install_requires=["bbb"],
    # badly specified requirements, seen in unittest2
    tests_require=(["ccc"],),
    extras_require=dict(test="ddd"),
)
"""


class TestDistInfo(TestCase):

    collector = distinfo.DistInfo

    def test_collect(self, tmpdir):
        tmpdir.join("setup.py").write(SETUP)
        tmpdir.join("xxx").mkdir().join("__init__.py").write("")
        collector = self._collect(tmpdir)
        assert {"setuptools"} == collector.requires.build
        assert {"bbb"} == collector.requires.run
        assert {"ccc", "ddd"} == collector.requires.test
        assert ["xxx"] == collector.ext.packages

    def test_process_output(self, tmpdir):
        collector = self._collect(tmpdir)
        collector._process_output("Searching for xxx")
        assert collector.requires.build == {"xxx"}

    def test_collect_nosetup(self, tmpdir, caplog):
        self._collect(tmpdir)
        assert "has no setup.py" in caplog.text

    def test_run_dist_info_fail(self, caplog, monkeypatch, tmpdir):
        def _raiser(action):
            if action == "dist_info":
                raise Exception()
            return run_setup(action)
        run_setup = distinfo.run_setup
        monkeypatch.setattr(distinfo, "run_setup", _raiser)
        tmpdir.join("setup.py").write(SETUP)
        collector = self._collect(tmpdir)
        assert "dist_info raised" in caplog.text
        assert collector.name == "UNKNOWN"

    def test_run_egg_info_fail(self, caplog, monkeypatch, tmpdir):
        monkeypatch.setattr(distinfo, "run_setup", self._raiser())
        tmpdir.join("setup.py").write(SETUP)
        collector = self._collect(tmpdir)
        assert "egg_info raised" in caplog.text
        assert collector.name == "UNKNOWN"
