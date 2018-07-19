from distinfo.requirement import Requirement

from .cases import TestCase


class TestRequirement(TestCase):

    def test_repr(self):
        req = Requirement("xxx")
        assert "Requirement xxx" in repr(req)

    def test_eq(self):
        assert Requirement("xxx") == Requirement("xxx")
        assert Requirement("Xxx") == "xxx"
        assert Requirement("xxx") != "yyy"
        assert Requirement("xxx") != 1
        assert Requirement("xxx>1") == Requirement("xxx>1")
        assert Requirement("xxx>1") != Requirement("xxx>2")
        assert Requirement("xxx>1") == Requirement("xxx")
