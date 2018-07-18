import copy
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
                getattr(collectors, name)(self, req.source_dir, req=req).collect()

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

    def add_requirement(self, req, extra="run"):
        if isinstance(req, str):
            req = registry.Requirement(req)
        if extra != "run":
            self.provides_extra.add(extra)
            assert req.marker is None, "%r has marker" % req
            req.marker = Marker("extra == '%s'" % extra)
        self.requires_dist.add(str(req))
        del self.requires

    @cached_property
    def requires(self):
        from . import registry
        reqs = set(map(registry.Requirement, self.requires_dist))
        requires = Munch()
        run = set(filter(lambda r: r.marker is None, reqs))
        if run:
            requires["run"] = run
            reqs -= run
        for extra in self.provides_extra:
            requires[extra] = set(map(
                # take the marker off the requirement
                lambda r: setattr(r, "marker", None) or r,
                # pylint: disable=cell-var-from-loop
                filter(lambda r: r.marker is not None
                       and r.marker.evaluate(dict(extra=extra)), reqs)
            ))
        return requires
