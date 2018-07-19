from pathlib import Path

from distinfo import const

SETUP = """
from setuptools import setup
setup()
"""


class Case:

    DIST = "test.dist"

    data_path = Path(__file__).parent / "data"

    def _raiser(self, exc=Exception):
        def _raiser(*_args, **_kwargs):
            raise exc()
        return _raiser

    def _write_setup(self, tmpdir, setup=SETUP):
        tmpdir.join(const.SETUP_PY).write(setup)
