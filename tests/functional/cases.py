from pathlib import Path
import shutil

from ..cases import Case as _Case


class Case(_Case):

    def _sdist(self, tmpdir):
        sdist = Path(tmpdir) / "src"
        shutil.copytree(self.data_path / self.DIST, sdist)
        return sdist
