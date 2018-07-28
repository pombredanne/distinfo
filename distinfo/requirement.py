import logging

import pkg_resources

from requirementslib import Requirement as _Requirement

from .base import Base

log = logging.getLogger(__name__)


class Requirement(Base, _Requirement):

    def __eq__(self, other):
        if isinstance(other, str):
            other = type(self).from_line(other)
        elif not isinstance(other, type(self)):
            return False
        if self.normalized_name == other.normalized_name:
            if self.specifiers == other.specifiers:
                return True
            if not self.specifiers or not other.specifiers:
                return True
        return False

    def __hash__(self):
        return hash(self.normalized_name)

    def __str__(self):
        return self.as_line()

    @classmethod
    def from_file(cls, path):
        for line in pkg_resources.yield_lines(open(path)):
            try:
                yield cls.from_line(line)
            except pkg_resources.RequirementParseError as exc:
                log.warning("line %r of %r raised %r", line, path, exc)
