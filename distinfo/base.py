class Base:

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return "<%s %s>" % (type(self).__name__, self)

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        if isinstance(other, type(self)):
            return str(self) == str(other)
        return False

    def __hash__(self):
        return hash(str(self))
