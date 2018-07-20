import importlib
import logging
import os
import sys

from munch import DefaultMunch, Munch

from packaging.markers import InvalidMarker, Marker
from packaging.requirements import InvalidRequirement

from property_manager import cached_property

from setuptools import sandbox

import wrapt

from . import util
from .base import Base
from .config import cfg
from .requirement import Requirement

log = logging.getLogger(__name__)


class Distribution(Base, wrapt.ObjectProxy):

    path = None

    def __init__(self, path=None, **kwargs):
        metadata = Munch(
            requires_dist=set(),
            provides_extra=set(),
            extensions=Munch(distinfo=Munch()),
        )
        metadata.update(kwargs)
        super().__init__(metadata)
        self.path = path
        if self.path is not None:
            self.path = os.path.relpath(self.path)
            with sandbox.pushd(self.path), sandbox.save_path():
                sys.path.insert(0, ".")
                for name in cfg.collectors:
                    module = importlib.import_module(
                        "distinfo.collectors.%s" % name.lower()
                    )
                    getattr(module, name)(self).collect()
        # XXX: a side effect of the below is that `requires` will remove
        # any invalid requirements
        log.debug(
            "%r requires:\n%s",
            self,
            util.dumps(self.requires, fmt="yamls"),
        )

    def __str__(self):
        return "%s-%s%s" % (
            self.name,
            self.version,
            self.path and " %s" % self.path or "",
        )

    @property
    def name(self):
        return self.get("name", "UNKNOWN")

    @name.setter
    def name(self, name):
        self["name"] = name

    @property
    def version(self):
        return self.get("version", "0.0.0")

    @version.setter
    def version(self, version):
        self["version"] = version

    @property
    def ext(self):
        return self.extensions.distinfo

    def _filter_reqs(self, reqs, extra):
        filtered = set()
        env = dict(extra=extra)
        for req in reqs:
            if extra == "run":
                if req.marker is None or req.marker.evaluate(env):
                    filtered.add(req)
            else:
                if req.marker is not None and req.marker.evaluate(env):
                    filtered.add(req)
        return filtered

    @cached_property
    def requires(self):
        reqs = set()
        for req in self.requires_dist:
            try:
                req = Requirement(req)
            except InvalidRequirement as exc:
                log.warning("%r requirement %r raised: %r", self, req, exc)
                self.requires_dist.remove(req)
            else:
                reqs.add(req)
        requires = DefaultMunch(set())
        run = self._filter_reqs(reqs, "run")
        if run:
            requires["run"] = run
            reqs -= run
        for extra in self.provides_extra:
            ereqs = self._filter_reqs(reqs, extra)
            if ereqs:
                requires[extra] = ereqs
        return requires

    def add_requirement(self, req, extra="run"):

        # cast to Requirement
        if isinstance(req, str):
            try:
                req = Requirement(req)
            except InvalidRequirement as exc:
                log.warning("%r %r add %r raised %r", self, extra, req, exc)
                return
        else:
            # belt and braces
            assert isinstance(req, Requirement)

        # skip out if requirement is already present
        if req in self.requires[extra] \
                or (extra != "run" and req in self.requires["run"]):
            return

        if extra != "run":
            self.provides_extra.add(extra)
            # set marker
            try:
                marker = Marker(extra[1:] if extra.startswith(":")
                                else "extra == '%s'" % extra)
            except InvalidMarker as exc:
                log.warning("%r %r add %r raised %r", self, extra, req, exc)
                return
            if req.marker is not None:
                marker = Marker("(%s) and %s" % (req.marker, marker))
            req.marker = marker

        self.requires_dist.add(str(req))
        del self.requires
        return req
