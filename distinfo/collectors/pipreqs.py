import logging
from setuptools import find_packages

from munch import DefaultFactoryMunch

from pipreqs import pipreqs

from ..config import cfg
from .collector import Collector

log = logging.getLogger(__name__)


class PipReqs(Collector):

    def _get_packages(self, path):
        try:
            return set(map(
                str.lower,
                pipreqs.get_pkg_names(pipreqs.get_all_imports(path)),
            ))
        except Exception as exc:
            log.exception("%r failed to get packages", self)
            return set()

    def _collect(self):

        imports = DefaultFactoryMunch(set)
        toplevel_imports = self._get_packages(".")
        packages = list(filter(lambda p: p.find(".") == -1, find_packages()))

        # check each package
        for package in packages:
            imports[package] |= self._get_packages(package)
            toplevel_imports -= imports[package]

        # remove self references
        for pkg_imports in imports.values():
            for package in packages:
                if package in pkg_imports:
                    pkg_imports.remove(package)

        # check dist package
        distpkg = imports.get(self.dist.name)
        if distpkg is not None:
            run = self.dist.depends.run
            missing = []
            for pkg in distpkg:
                if cfg.package_aliases.get(pkg, pkg) not in run \
                        and pkg.replace("_", "-") not in run:
                    missing.append(pkg)
            if missing:
                log.warning("%s missing run dependencies: %r", self, missing)
        if toplevel_imports:
            imports["build"] = toplevel_imports
        if imports:
            self.dist.ext.imports = imports
