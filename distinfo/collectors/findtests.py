from .collector import Collector


class FindTests(Collector):

    def _collect(self):
        self.ext.tests = set(map(lambda p: str(p.parent), self.path.glob("**/*test*.py")))
