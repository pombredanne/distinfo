import logging
import os

from pip._internal.req.req_install import InstallRequirement
from pip._vendor.packaging.requirements import Requirement as _Requirement

from .base import Base

log = logging.getLogger(__name__)


class Requirement(Base, _Requirement):

    # FIXME: mro is screwed
    __hash__ = Base.__hash__

    def __eq__(self, other):
        if isinstance(other, str):
            if str(self) == other:
                return True
            if self.name.lower() == other.lower():
                return True
        if not isinstance(other, type(self)):
            return False
        return self.name == other.name and self.specifier == other.specifier


def parse_requirement(source):
    # source may be a pathlib.Path
    req = InstallRequirement.from_line(str(source))
    if os.path.exists(source):
        req.source_dir = source
    return req
