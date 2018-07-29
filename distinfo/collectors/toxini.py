import logging
import os
from pathlib import Path
import re
import sys

from munch import Munch

from tox.config import parseconfig
from tox.exception import ConfigError

from .collector import Collector

log = logging.getLogger(__name__)


class ToxIni(Collector):

    ENV_IGNORE_PATTERN = re.compile("doc|lint")

    def _detox(self, config, expr):
        cwd = os.getcwd()
        expr = expr.replace(str(config.envbindir) + "/", "")
        expr = expr.replace(str(config.envdir) + "/", "")
        expr = expr.replace(cwd + "/", "")
        expr = expr.replace(cwd, "")
        return expr

    def _collect(self):

        if not (self.path / "tox.ini").exists():
            return

        try:
            toxconf = parseconfig([])
        except ConfigError as exc:
            self._warn_exc(exc)
            return

        python = "python%d.%d" % (sys.version_info.major, sys.version_info.minor)
        configs = sorted(
            filter(
                lambda c: not self.ENV_IGNORE_PATTERN.match(c.envname),
                toxconf.envconfigs.values(),
            ),
            key=lambda c: c.envname,
            reverse=True,
        )
        match_configs = [c for c in configs
                         if Path(c.basepython).name in (python, python + "m")]
        if match_configs:
            envname = "py%d%d" % (sys.version_info.major, sys.version_info.minor)
            for config in match_configs:
                if config.envname == envname:
                    break
            else:
                for config in match_configs:
                    if config.envname.startswith("py"):
                        break
                else:
                    config = match_configs[0]
        else:
            if not configs:
                log.warning("%r no config found", self)
                return
            config = configs[0]
            log.warning("%r has no config for %s, using %s", self, python, config.envname)

        # dependencies
        for dep in config.deps:
            if dep.name.startswith("-r"):
                reqs_file = dep.name[2:].strip()
                if not (self.path / reqs_file).exists():
                    log.warning(
                        "%r %r from tox.ini does not exist",
                        self,
                        reqs_file,
                    )
                    continue
                self.add_requirements_file(reqs_file, "test")
            else:
                # unpin dependencies
                dep = dep.name.split("==")[0].strip()
                self.add_requirement(dep, "test")

        # environment
        env = Munch()
        for key in config.setenv.keys():
            if key != "PYTHONHASHSEED":
                env[key] = self._detox(config, config.setenv[key])

        # commands
        commands = [[self._detox(config, c) for c in cmd] for cmd in config.commands]

        self.ext.tox = Munch(commands=commands, env=env)
