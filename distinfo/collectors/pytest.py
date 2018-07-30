from .collector import PackageCollector


class Pytest(PackageCollector):

    name = "pytest"

    def _parse_addopts(self, config):
        addopts = config.get("addopts", "")
        if "--cov" in addopts:
            return "pytest-cov"
        return self.name

    def _requires(self):

        # look for setup.cfg section
        config = self._get_setup_cfg()
        if config is not None:
            for key in ("pytest", "tool:pytest"):
                if key in config:
                    return self._parse_addopts(config[key])

        # look for conftest.py files
        conftest = list(self.path.glob("**/conftest.py"))
        if conftest:
            self.ext.setdefault("tests", set())
            self.ext.tests |= set(map(lambda p: str(p.parent), conftest))
            return self.name

        # look for ini
        config = self._get_ini_config("pytest.ini")
        if config is not None:
            if "pytest" in config:
                return self._parse_addopts(config["pytest"])
