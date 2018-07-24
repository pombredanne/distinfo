class Base:

    _short_name = None

    def __repr__(self):
        name = self._short_name or type(self).__name__
        return "<%s %s>" % (name, self)
