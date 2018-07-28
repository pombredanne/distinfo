from distinfo.requirement import Requirement

from .cases import Case

REQUIREMENTS = """
aaa
http://h/p
-cxxx
"""


class TestRequirement(Case):

    def test_eq(self):
        assert Requirement.from_line("xxx") == Requirement.from_line("xxx")
        assert Requirement.from_line("Xxx") == "xxx"
        assert Requirement.from_line("xxx") != "yyy"
        assert Requirement.from_line("xxx") != 1
        assert Requirement.from_line("xxx>1") == Requirement.from_line("xxx>1")
        assert Requirement.from_line("xxx>1") != Requirement.from_line("xxx>2")
        assert Requirement.from_line("xxx>1") == Requirement.from_line("xxx")

    def test_from_file(self, tmpdir):
        requirements = "requirements.txt"
        reqs = tmpdir.join(requirements)
        reqs.write(REQUIREMENTS)
        assert list(Requirement.from_file(reqs)) == ["aaa", "http://h/p"]
