import configparser
import logging
from pathlib import Path
import sys

from pip._internal.req import parse_requirements
from pip._vendor.packaging.markers import InvalidMarker
from pip._vendor.packaging.requirements import InvalidRequirement

from setuptools import sandbox

from ..base import Base

log = logging.getLogger(__name__)


class Collector(Base):

    def __init__(self, dist, source_dir, req=None):
        self.dist = dist
        self.source_dir = source_dir
        self.req = req
        self._seen_files = set()

    def __str__(self):
        return str(self.dist)

    def _collect(self):
        raise NotImplementedError()

    def collect(self):
        with sandbox.pushd(self.source_dir), sandbox.save_path():
            sys.path.insert(0, self.source_dir)
            self._collect()

    def add_requirement(self, req, extra="test"):
        log.debug("%r %r add %r", self, extra, req)
        try:
            self.dist.add_requirement(req, extra=extra)
        except (InvalidMarker, InvalidRequirement) as exc:
            log.warning("%r %r add %r raised %r", self, extra, req, exc)

    def add_requirements_file(self, path):
        if path in self._seen_files:
            log.warning("%r already seen %r", self, path)
            return
        self._seen_files.add(path)
        for req in parse_requirements(path, session=True):
            self.add_requirement(req.req)

    def get_setup_cfg(self):
        setup = Path("setup.cfg")
        if setup.exists():
            config = configparser.ConfigParser()
            config.read(setup)
            return config


class PackageCollector(Collector):

    name = None

    def _requires(self):
        raise NotImplementedError()

    def _collect(self):
        if getattr(self.dist, "name", None) == self.name:
            return
        # check imports for the package name
        req = False
        extra = "test"
        imports = getattr(self.dist.ext, "imports", None)
        if imports is not None:
            for package in getattr(self.dist.ext, "packages", []):
                if self.name in getattr(imports, package, []):
                    req = self.name
                    if package == self.dist.name:
                        extra = "run"
                    break
        # if not found here then hand off to subclass
        if not req:
            req = self._requires()
        if req:
            self.add_requirement(req, extra=extra)
