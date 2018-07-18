import logging

from munch import Munch

from pipreqs import pipreqs

from ..config import cfg
from .collector import Collector

log = logging.getLogger(__name__)


class PipReqs(Collector):

    def _get_packages(self, package):
        path = package.replace(".", "/")
        try:
            return set(
                map(
                    lambda p: cfg.package_aliases.get(p, p),
                    map(
                        str.lower,
                        pipreqs.get_pkg_names(pipreqs.get_all_imports(path)),
                    )
                )
            )
        except Exception as exc:
            log.exception("%r fail", self)
            return set()

    def _collect(self):

        imports = Munch()

        # check each package
        packages = getattr(self.dist.ext, "packages", [])
        for package in packages:
            pkgs = self._get_packages(package)
            if pkgs:
                imports[package] = pkgs

        # remove self references
        for pkg_imports in imports.values():
            for package in packages:
                if package in pkg_imports:
                    pkg_imports.remove(package)

        # check dist package
        distpkg = imports.get(self.dist.name)
        if distpkg is not None:
            run = getattr(self.dist.depends, "run", set())
            missing = []
            for pkg in distpkg:
                if pkg not in run and pkg.replace("_", "-") not in run:
                    missing.append(pkg)
            if missing:
                log.warning("%s missing run dependencies: %r", self, missing)
        if imports:
            self.dist.ext.imports = imports
