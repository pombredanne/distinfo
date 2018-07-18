from distinfo.requirement import Requirement

from .cases import TestCase


class TestRequirement(TestCase):

    def test_repr(self):
        req = Requirement("xxx")
        assert "Requirement xxx" in repr(req)

    def test_eq(self):
        req = Requirement("xxx")
        req2 = Requirement("xxx")
        req3 = Requirement("yyy>1")
        assert req == req2
        assert req != req3
        assert req == "xxx"
        assert req != "yyy"
        assert req3 == "yyy"
