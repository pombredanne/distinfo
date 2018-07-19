from pathlib import Path
import shutil


class TestCase:

    DIST = "test.dist"

    data_path = Path(__file__).parent / "data"

    def _raiser(self, exc=Exception):
        def _raiser(*_args, **_kwargs):
            raise exc()
        return _raiser

    def _sdist(self, tmpdir):
        sdist = Path(tmpdir) / "src"
        shutil.copytree(self.data_path / self.DIST, sdist)
        return sdist
