from .collector import Collector


class FindTests(Collector):

    def _collect(self):
        self.ext.tests = sorted(set(map(lambda p: p.parent,
                                        self.path.glob("**/test*.py"))))
