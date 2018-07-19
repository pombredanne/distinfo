import importlib
import logging

from munch import Munch

from packaging.markers import InvalidMarker, Marker
from packaging.requirements import InvalidRequirement

from property_manager import cached_property

from requirementslib.models.requirements import FileRequirement

import wrapt

from . import util
from .base import Base
from .config import cfg
from .requirement import Requirement

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
        return self.get("name", "UNKNOWN")

    @name.setter
    def name(self, name):
        self["name"] = name

    @classmethod
    def from_source(cls, source_dir):
        req = FileRequirement.from_line(str(source_dir))
        dist = cls()
        for name in cfg.collectors:
            module = importlib.import_module(
                "distinfo.collectors.%s" % name.lower()
            )
            getattr(module, name)(dist, req.path).collect()
        if dist.name == "UNKNOWN":
            log.warning("%r metadata unavailable")
        else:
            # XXX: a side effect of the below is that `requires` will remove
            # any invalid requirements
            log.debug(
                "%r requires:\n%s",
                dist,
                util.dumps(dist.requires, fmt="yamls"),
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

    @property
    def reqs(self):
        reqs = set()
        for req_str in self.requires_dist:
            try:
                req = Requirement(req_str)
            except InvalidRequirement as exc:
                log.warning("%r requirement %r raised: %r", self, req_str, exc)
                self.requires_dist.remove(req_str)
            else:
                # keep the requirement string which may be needed later to
                # remove it from `requires_dist`
                req.req_str = req_str
                reqs.add(req)
        return reqs

    @cached_property
    def requires(self):
        requires = Munch()
        reqs = self.reqs
        run = self._filter_reqs(reqs)
        if run:
            requires["run"] = run
            reqs -= run
        for extra in self.provides_extra:
            # set the marker to None as it has already served its purpose and
            # now is just noise
            filtered = set(map(lambda r: setattr(r, "marker", None) or r,
                               self._filter_reqs(reqs, extra=extra)))
            if filtered:
                requires[extra] = filtered
        return requires

    def _merge_requirement(self, mreq, extra):
        for req in self.requires.get(extra, []):
            if mreq.name == req.name:
                mreq.specifier &= req.specifier
                if req.marker is not None:
                    if mreq.marker is None:
                        mreq.marker = req.marker
                    else:
                        mreq.marker = Marker("(%s) and %s" % (req.marker, mreq.marker))
                return mreq, req

    def _add_requirement(self, req, old=None):
        if old is not None:
            log.debug("%r replacing %r with %r", self, old, req)
            self.requires_dist.remove(old.req_str)
        self.requires_dist.add(str(req))
        del self.requires
        return req

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
