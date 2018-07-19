import logging

from packaging.requirements import Requirement as _Requirement

from requirementslib.models.requirements import Requirement as XRequirement

from .base import Base

log = logging.getLogger(__name__)


class Requirement(Base, _Requirement):

    def __hash__(self):
        # HACK: used by set __contains__
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, str):
            other = type(self)(other)
        elif not isinstance(other, type(self)):
            return False
        if self.name.lower() == other.name.lower():
            if self.specifier == other.specifier:
                return True
            if not self.specifier or not other.specifier:
                return True
        return False

    @classmethod
    def parse(cls, line):
        return cls(XRequirement.from_line(line).as_line())

    @classmethod
    def parse_file(cls, path):
        for line in open(path):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            yield cls.parse(line)
