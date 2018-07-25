import distutils.core
from email.parser import FeedParser
import logging

import capturer

from munch import Munch

from setuptools import sandbox

from .. import const
from .collector import Collector

log = logging.getLogger(__name__)


# run_setup from distutils.core doesn't work in every case - this does
def run_setup(action):
    distutils.core._setup_distribution = None
    with sandbox.save_argv((const.SETUP_PY, action)):
        sandbox._execfile(
            const.SETUP_PY,
            dict(__file__=const.SETUP_PY, __name__="__main__"),
        )
    dist = distutils.core._setup_distribution
    assert dist is not None, "distutils.core.setup not called"
    return dist


class DistInfo(Collector):

    MULTI_KEYS = (
        "classifier",
        "obsoletes_dist",
        "platform",
        "project_url",
        "provides_dist",
        "provides_extra",
        "requires_dist",
        "requires_external",
        "supported_platform",
    )

    # these are from PEP 314 Metadata 1.1
    KEY_ALIASES = dict(
        obsoletes="obsoletes_dist",
        provides="provides_dist",
        requires="requires_dist",
    )

    EXTRAS = Munch(
        setup_requires="build",
        install_requires="run",
        tests_require="test",
    )

    def _get_pkginfo(self):
        return list(self.path.glob("**/*.egg-info/PKG-INFO"))

    def _collect(self):

        if not (self.path / const.SETUP_PY).exists():
            log.warning("%r has no %s", self, const.SETUP_PY)
            return

        try:
            with capturer.CaptureOutput(relay=False) as capture:
                if self._get_pkginfo():
                    # run anything to get the dist object
                    dist = run_setup("-h")
                else:
                    # not using wheel's dist_info as it fails for some packages
                    # (cryptography), and it adds nothing since it does not
                    # deal with build and test requirements
                    dist = run_setup("egg_info")
        except BaseException:
            log.warning("setup failure:\n%s", capture.get_text())
            raise

        # get metadata
        infos = self._get_pkginfo()
        assert infos
        parser = FeedParser()
        parser.feed(open(infos[0]).read())
        message = parser.close()
        for key, value in message.items():
            value = value.strip()
            if not value or value == "UNKNOWN":
                continue
            key = key.lower().replace("-", "_")
            key = self.KEY_ALIASES.get(key, key)
            if key in self.MULTI_KEYS:
                self.metadata.setdefault(key, set()).add(value)
            else:
                self.metadata[key] = value

        # get requirements from distutils dist
        for attr, extra in self.EXTRAS.items():
            reqs = getattr(dist, attr, None) or []
            # fix incorrectly specified requirements (unittest2 does this)
            if isinstance(reqs, tuple) and isinstance(reqs[0], list):
                reqs = reqs[0]
            for req in reqs:
                self.add_requirement(req, extra)
        for extra, reqs in getattr(dist, "extras_require", {}).items():
            for req in reqs:
                self.add_requirement(req, extra)

        # get packages
        self.ext.packages = getattr(dist, "packages", [])
        self.ext.modules = getattr(dist, "py_modules", [])
