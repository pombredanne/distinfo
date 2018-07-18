import copy
import logging

from munch import Munch

from pip._internal.exceptions import InstallationError

from property_manager import cached_property

import wrapt

from . import registry
from .base import Base
from .config import cfg

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
        req = registry.Requirement.from_source(source_dir)
        return cls(req=req)

    @property
    def ext(self):
        return self.extensions.distinfo

    def add_requirement(self, req, extra="run"):
        if extra != "run":
            self.provides_extra.add(extra)
            req = "%s; extra == '%s'" % (req, extra)
        self.requires_dist.add(req)
        del self.reqs
        del self.requires

    @cached_property
    def reqs(self):
        from . import registry
        reqs = set()
        for req in self.requires_dist:
            try:
                reqs.add(registry.Requirement.from_req(req))
            except InstallationError as exc:
                log.warning("%r requirement %r fail: %r", self, req, exc)
        return reqs

    @cached_property
    def requires(self):
        reqs = set(map(copy.deepcopy, self.reqs))
        requires = Munch()
        run = set(filter(lambda r: r.markers is None, self.reqs))
        if run:
            requires["run"] = run
            reqs -= run
        for extra in self.provides_extra:
            requires[extra] = set(map(
                # take the marker off the requirement
                lambda r: setattr(r.req, "marker", None) or r,
                # pylint: disable=cell-var-from-loop
                filter(lambda r: r.markers.evaluate(dict(extra=extra)), reqs)
            ))
        return requires
