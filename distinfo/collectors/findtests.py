from .collector import Collector


class FindTests(Collector):

    def _collect(self):
        self.ext.tests = set(map(
            lambda p: str(p.parent),
            filter(
                lambda p: "pytest" not in p.name,
                self.path.glob("**/*test*.py"),
            ),
        ))
