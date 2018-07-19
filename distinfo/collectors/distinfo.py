from distutils.core import run_setup
from email.parser import FeedParser
import logging
import re

import capturer

from munch import Munch

from .collector import Collector

log = logging.getLogger(__name__)

SEARCH_PATTERN = re.compile("Searching for (.*)")


class DistInfo(Collector):

    MULTI_KEYS = (
        "classifier",
        "obsoletes",
        "obsoletes_dist",
        "platform",
        "project_url",
        "provides",
        "provides_dist",
        "provides_extra",
        "requires",
        "requires_dist",
        "requires_external",
        "supported_platform",
    )

    SETUP = "setup.py"

    def _process_output(self, output):
        for req in SEARCH_PATTERN.findall(output):
            self.add_requirement(req, "build")

    def _collect(self):

        if not (self.path / self.SETUP).exists():
            log.warning("%r has no setup.py")
            return

        with capturer.CaptureOutput(relay=False) as capture:
            try:
                dist = run_setup(self.SETUP, ["dist_info"])
            except BaseException as exc:
                log.warning("%r dist_info raised %r", self, exc)
                try:
                    dist = run_setup(self.SETUP, ["egg_info"])
                except BaseException as exc:
                    log.warning("%r egg_info raised %r", self, exc)
                    return
            finally:
                self._process_output(capture.get_text())

        # get metadata
        provides_dist = True
        infos = list(self.path.glob("**/*.dist-info/METADATA"))
        if not infos:
            provides_dist = False
            infos = list(self.path.glob("**/*.egg-info/PKG-INFO"))
        assert infos
        parser = FeedParser()
        parser.feed(open(infos[0]).read())
        message = parser.close()
        for key, value in message.items():
            value = value.strip()
            if not value or value == "UNKNOWN":
                continue
            key = key.lower().replace("-", "_")
            if key in self.MULTI_KEYS:
                self.dist.setdefault(key, set()).add(value)
            else:
                self.dist[key] = value

        # get requirements from distutils dist
        extras = Munch(setup_requires="build", tests_require="test")
        if not provides_dist:
            extras.install_requires = "run"
            for extra, reqs in getattr(dist, "extras_require", {}).items():
                for req in reqs:
                    self.add_requirement(req, extra)
        for attr, extra in extras.items():
            reqs = getattr(dist, attr, None) or []
            # fix incorrectly specified requirements (unittest2 does this)
            if isinstance(reqs, tuple) and isinstance(reqs[0], list):
                reqs = reqs[0]
            for req in reqs:
                self.add_requirement(req, extra)

        # get packages
        self.ext.packages = list(map(
            lambda p: str(p.parent.relative_to(".")),
            sorted(self.path.glob("*/__init__.py")),
        ))
