from .collector import Collector


class Dirty(Collector):

    def _collect(self):
        self.ext.dirty = bool(list(self.path.glob("**/*.py[co]")))
