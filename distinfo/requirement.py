import logging

from pip._internal.req.req_install import InstallRequirement

from .base import Base

log = logging.getLogger(__name__)


class Requirement(Base, InstallRequirement):

    # FIXME: mro is screwed
    __hash__ = Base.__hash__
    __str__ = InstallRequirement.__str__

    def __eq__(self, other):
        if isinstance(other, str):
            if str(self) == other:
                return True
            if self.name.lower() == other.lower():
                return True
        if not isinstance(other, type(self)):
            return False
        return self.name == other.name and self.specifier == other.specifier

    @classmethod
    def from_source(cls, source_dir):
        req = cls.from_line(str(source_dir))
        req.source_dir = source_dir
        return req
