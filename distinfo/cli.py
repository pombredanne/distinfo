import logging
from pathlib import Path

import appdirs

import click

from munch import munchify

import pkg_resources

from ptpython import repl

from . import util
from .config import cfg, configure_logging
from .distribution import Distribution
from .requirement import Requirement

VERSION = pkg_resources.get_distribution("distinfo").version

log = logging.getLogger(__name__)


@click.command()
@click.argument("source_dir", nargs=1, default=".",
                type=click.Path(exists=True, file_okay=False))
@click.option("-o", "--output", help="Output file")
@click.option("-i", "--interactive", is_flag=True)
@click.option("-c", "--color", is_flag=True, help="Force colored output")
@click.option("-f", "--fmt", type=click.Choice(util.DUMPERS.keys()),
              help="Output formats")
@click.option("-d", "--depends", is_flag=True, help="Print dependencies")
@click.version_option(VERSION)
def main(source_dir, **options):
    """
    Extract metadata from Python source distributions
    """

    options = munchify(options)

    if options.color:
        cfg.logging.config.isatty = True
    configure_logging()

    dist = Distribution.from_source(source_dir)

    if options.interactive:
        namespace = dict(
            Distribution=Distribution,
            Requirement=Requirement,
            dist=dist,
            dump=util.dump,
            dumps=util.dumps,
        )
        click.secho("distinfo shell %s:" % VERSION, fg="white", bold=True)
        cachedir = Path(appdirs.user_cache_dir("distinfo", "distinfo"))
        cachedir.mkdir(parents=True, exist_ok=True)
        repl.embed(
            namespace,
            configure=repl.run_config,
            history_filename=cachedir / "history",
        )
    else:
        if options.depends:
            obj = dist.requires
        else:
            obj = dist
        dump = util.dumps(obj, fmt=options.fmt)
        if options.output:
            with open(options.output, "w") as stream:
                stream.write(dump)
        else:
            print(dump)
