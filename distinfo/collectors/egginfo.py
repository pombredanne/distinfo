from email.parser import FeedParser
import logging

import pkg_resources

from .collector import Collector

log = logging.getLogger(__name__)


class EggInfo(Collector):

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

    def _collect(self):

        egg_infos = list(self.path.glob("**/*.egg-info"))
        if not egg_infos:
            log.warning("%r has no egg info", self)
            return
        egg_info = egg_infos[0]

        # parse metadata
        parser = FeedParser()
        parser.feed(open(egg_info / "PKG-INFO").read())
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

        # parse requires
        requires_path = egg_info / "requires.txt"
        if requires_path.exists():
            requires = requires_path.open().read()
            for extra, reqs in sorted(pkg_resources.split_sections(requires),
                                      key=lambda x: x[0] or ""):
                if extra is None:
                    extra = "run"
                for req in reqs:
                    self.add_requirement(req, extra)
