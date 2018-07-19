import logging

from munch import Munch

from pipreqs import pipreqs

from ..config import cfg
from .collector import Collector

log = logging.getLogger(__name__)


class PipReqs(Collector):

    IGNORE = (
        "setuptools",
    )

    def _get_packages(self, path):
        try:
            return set(
                filter(
                    lambda p: p != self.dist.name and p not in self.IGNORE,
                    map(
                        lambda p: cfg.package_aliases.get(p, p),
                        map(
                            str.lower,
                            pipreqs.get_pkg_names(pipreqs.get_all_imports(path)),
                        )
                    )
                )
            )
        except Exception as exc:  # pylint: disable=broad-except
            self._warn_exc(exc)
            return set()

    def _warn_missing(self, extra, reqs, imports):
        missing = []
        for pkg in imports:
            if pkg not in reqs and pkg.replace("_", "-") not in reqs:
                missing.append(pkg)
        if missing:
            log.warning(
                "%s missing %s dependencies: %s",
                self,
                extra,
                ", ".join(missing),
            )

    def _collect(self):

        self.ext.imports = Munch()

        log.debug(repr(self.dist))

        # check each package
        packages = getattr(self.ext, "packages", [])
        for package in packages:
            self.ext.imports[package] = self._get_packages(package) - {self.dist.name}

        # check dist package
        reqs = getattr(self.dist.requires, "run", set()) | {self.dist.name}
        run_imports = self.ext.imports.get(self.dist.name, set())
        self._warn_missing("run", reqs, run_imports)

        # check tests
        reqs |= getattr(self.dist.requires, "test", set())
        test_imports = set()
        for path in getattr(self.ext, "tests", []):
            test_imports |= self._get_packages(path)
        self._warn_missing("test", reqs, test_imports)
