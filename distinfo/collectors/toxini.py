import logging
import os
import re
import sys

from munch import Munch

from tox.config import parseconfig
from tox.exception import ConfigError

from .collector import Collector

log = logging.getLogger(__name__)


class ToxIni(Collector):

    ENV_NAME_PATTERN = re.compile("^py[0-9]+")

    def _collect(self):

        if not (self.path / "tox.ini").exists():
            return

        try:
            toxconf = parseconfig([])
        except ConfigError as exc:
            self._warn_exc(exc)
            return

        name = "py%d%d" % (sys.version_info.major, sys.version_info.minor)
        configs = sorted([c for c in toxconf.envconfigs.values()
                          if self.ENV_NAME_PATTERN.match(c.envname)],
                         key=lambda c: c.envname)
        for config in configs:
            if config.envname.startswith(name):
                break
        else:
            if not configs:
                return
            # take the last environment which will be the highest python
            config = configs[-1]
            log.warning(
                "%r has no environment for %r, falling back to %r",
                self,
                name,
                config.envname,
            )

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
                # don't allow pinned dependencies
                dep = dep.name.split("==")[0].strip()
                self.add_requirement(dep, "test")

        # environment
        env = Munch()
        for key in config.setenv.keys():
            if key in ("PYTHONHASHSEED", "PYTHONPATH"):
                continue
            env[key] = config.setenv[key].replace(os.getcwd(), ".")

        # commands
        cwd = os.getcwd()
        commands = []
        for command in config.commands:
            if command[0] == "pip":
                log.warning("%r ignoring command %r", self, command)
            else:
                cmd = []
                for expr in command:
                    expr = expr.replace(str(config.envbindir) + "/", "")
                    expr = expr.replace(str(config.envdir) + "/", "")
                    expr = expr.replace(str(config.envname), "result")
                    expr = expr.replace(cwd + "/", "")
                    expr = expr.replace(cwd, ".")
                    cmd.append(expr)
                commands.append(cmd)

        self.ext.tox = Munch(commands=commands, env=env)
