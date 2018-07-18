import logging

from munch import Munch

from pip._vendor.packaging.markers import Marker
from pip._vendor.packaging.requirements import InvalidRequirement

from property_manager import cached_property

import wrapt

from . import registry
from .base import Base
from .config import cfg
from .requirement import parse_requirement

log = logging.getLogger(__name__)


class Distribution(Base, wrapt.ObjectProxy):

    def __init__(self, req=None, **kwargs):
        metadata = Munch(
            requires_dist=set(),
            provides_extra=set(),
            extensions=Munch(distinfo=Munch()),
        )
        metadata.update(kwargs)
        super().__init__(metadata)
        if req is not None:
            from . import collectors
            for name in cfg.collectors:
                collector = getattr(collectors, name)
                collector(self, req.source_dir, req=req).collect()

    def __str__(self):
        version = getattr(self, "version", "unversioned")
        return "%s-%s" % (self.name, version)

    @property
    def name(self):
        return getattr(self, "name", "unnamed")

    @classmethod
    def from_source(cls, source_dir):
        return cls(req=parse_requirement(source_dir))

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
            else:
                reqs.add(req)
        requires = Munch()
        run = self._filter_reqs(reqs)
        if run:
            requires["run"] = run
            reqs -= run
        for extra in self.provides_extra:
            filtered = set(map(
                # take the marker off the requirement
                lambda r: setattr(r, "marker", None) or r,
                # pylint: disable=cell-var-from-loop
                self._filter_reqs(reqs, extra=extra),
            ))
            if filtered:
                requires[extra] = filtered
        return requires

    def add_requirement(self, req, extra="run"):
        if isinstance(req, str):
            try:
                req = registry.Requirement(req)
            except InvalidRequirement as exc:
                log.warning("%r %r add %r raised %r", self, extra, req, exc)
                return
        if extra != "run":
            self.provides_extra.add(extra)
            assert req.marker is None, "%r has marker" % req
            marker = extra
            if marker.startswith(":"):
                marker = marker[1:]
            else:
                marker = "extra == '%s'" % extra
            req.marker = Marker(marker)
        self.requires_dist.add(str(req))
        del self.requires
