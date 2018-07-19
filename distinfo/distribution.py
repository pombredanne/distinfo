import importlib
import logging

from munch import Munch

from packaging.markers import InvalidMarker, Marker
from packaging.requirements import InvalidRequirement

from property_manager import cached_property

from requirementslib.models.requirements import FileRequirement

import wrapt

from . import registry, util
from .base import Base
from .config import cfg

log = logging.getLogger(__name__)


class Distribution(Base, wrapt.ObjectProxy):

    def __init__(self, **kwargs):
        metadata = Munch(
            requires_dist=set(),
            provides_extra=set(),
            extensions=Munch(distinfo=Munch()),
        )
        metadata.update(kwargs)
        super().__init__(metadata)

    def __str__(self):
        version = getattr(self, "version", "0.0.0")
        return "%s-%s" % (self.name, version)

    @property
    def name(self):
        return getattr(self, "name", "UNKNOWN")

    @classmethod
    def from_source(cls, source_dir):
        req = FileRequirement.from_line(str(source_dir))
        dist = cls()
        for name in cfg.collectors:
            module = importlib.import_module(
                "distinfo.collectors.%s" % name.lower()
            )
            getattr(module, name)(dist, req.path).collect()
        # XXX: a side effect of the below is that `requires` will remove any
        # invalid requirements
        log.debug(
            "%r requires:\n%s",
            dist,
            util.dump(dist.requires, fmt="yamls"),
        )
        return dist

    @property
    def ext(self):
        return self.extensions.distinfo

    def _filter_reqs(self, reqs, extra=None):
        filtered = set()
        env = dict(extra=extra)
        for req in reqs:
            if extra is None:
                if req.marker is None or req.marker.evaluate(env):
                    filtered.add(req)
            else:
                if req.marker is not None and req.marker.evaluate(env):
                    filtered.add(req)
        return filtered

    @cached_property
    def requires(self):
        from . import registry
        reqs = set()
        for req in self.requires_dist:
            try:
                req = registry.Requirement(req)
            except InvalidRequirement as exc:
                log.warning("%r requirement %r raised: %r", self, req, exc)
                self.requires_dist.remove(req)
            else:
                reqs.add(req)
        requires = Munch()
        run = self._filter_reqs(reqs)
        if run:
            requires["run"] = run
            reqs -= run
        for extra in self.provides_extra:
            filtered = set(self._filter_reqs(reqs, extra=extra))
            if filtered:
                requires[extra] = filtered
        return requires

    def _merge_requirement(self, mreq, extra):
        for req in self.requires.get(extra, []):
            if mreq.name == req.name:
                str_req = str(req)
                req.specifier &= mreq.specifier
                if mreq.marker is not None:
                    if req.marker is None:
                        req.marker = mreq.marker
                    else:
                        req.marker = Marker("(%s) and %s" % (req.marker, mreq.marker))
                return req, str_req

    def _add_requirement(self, req, old=None):
        if old is not None:
            self.requires_dist.remove(old)
        self.requires_dist.add(str(req))
        del self.requires
        return req

    def add_requirement(self, req, extra="run"):

        # cast to Requirement
        if isinstance(req, str):
            try:
                req = registry.Requirement(req)
            except InvalidRequirement as exc:
                log.warning("%r %r add %r raised %r", self, extra, req, exc)
                return
        else:
            # belt and braces
            assert isinstance(req, registry.Requirement)

        # try to merge with existing
        mreq = self._merge_requirement(req, extra)
        if mreq is not None:
            return self._add_requirement(*mreq)

        if extra != "run":
            # try to merge with existing in "run"
            mreq = self._merge_requirement(req, "run")
            if mreq is not None:
                return self._add_requirement(*mreq)
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

        return self._add_requirement(req)
