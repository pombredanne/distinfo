import distutils
import logging
import sys
import warnings

import setuptools

from .. import const
from .collector import Collector

warnings.filterwarnings("ignore", "Unknown distribution option", module="dist")

log = logging.getLogger(__name__)


class DistInfo(Collector):

    STD_EXTRAS = dict(
        setup_requires="build",
        install_requires="run",
        tests_require="test",
    )

    def _filter_reqs(self, reqs):
        # fix incorrectly specified requirements (unittest2 does this)
        if isinstance(reqs, tuple) and isinstance(reqs[0], list):
            reqs = reqs[0]
        return filter(lambda r: r.strip(), reqs)

    def _collect(self):

        setup_py = self.path / const.SETUP_PY
        if not setup_py.exists():
            log.warning("%r has no %s", self, const.SETUP_PY)
            return

        distutils.core._setup_distribution = None
        distutils.core._setup_stop_after = "config"

        # replace setuptools.setup with distutils.setup because the setuptools
        # version attempts to install `setup_requires` which is not necessary
        # for our purposes
        _setup = setuptools.setup
        setuptools.setup = distutils.core.setup

        try:
            # FIXME: don't work
            # setuptools.sandbox.run_setup(const.SETUP_PY, ["-h"])
            sandbox = setuptools.sandbox
            with sandbox.save_argv((const.SETUP_PY, "-h")), sandbox.save_path():
                sys.path.insert(0, ".")
                sandbox._execfile(
                    const.SETUP_PY,
                    dict(__file__=const.SETUP_PY, __name__="__main__"),
                )
        finally:
            setuptools.setup = _setup

        dist = distutils.core._setup_distribution
        assert dist is not None, "distutils.core.setup not called"

        # get requirements from distutils dist
        for attr, extra in self.STD_EXTRAS.items():
            reqs = getattr(dist, attr, None) or []
            for req in self._filter_reqs(reqs):
                self.add_requirement(req, extra)
        for extra, reqs in getattr(dist, "extras_require", {}).items():
            for req in self._filter_reqs(reqs):
                self.add_requirement(req, extra)

        # get packages
        self.ext.packages = getattr(dist, "packages", [])
        self.ext.modules = getattr(dist, "py_modules", [])
        self.ext.hasext = bool(getattr(dist, "ext_modules", []))
