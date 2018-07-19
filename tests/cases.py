from pathlib import Path


class TestCase:

    data_path = Path(__file__).parent / "data"

    def _raiser(self, exc=Exception):
        def _raiser(*_args, **_kwargs):
            raise exc()
        return _raiser
