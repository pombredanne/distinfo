from pathlib import Path


class TestCase:

    data_path = Path(__file__).parent / "data"

    def _make_raiser(self, exc=Exception, function=None):
        def _raiser(*a, **kw):
            if function is not None:
                function(*a, **kw)
            raise exc()
        return _raiser
