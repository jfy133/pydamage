#!/usr/bin/env python3

import click
from pydamage.main import analyze
from pydamage import __version__


@click.command()
@click.version_option(__version__)
@click.argument('bam', type=click.Path(exists=True))
@click.option('-w',
              '--wlen',
              default=20,
              type=int,
              show_default=True,
              help='Window length from beginning of read')
@click.option('-p',
              '--process',
              default=2,
              type=int,
              show_default=True,
              help='Number of processes/CPUs to use')
@click.option('-m',
              '--mini',
              default=2000,
              type=int,
              show_default=True,
              help='Minimum reads required to be aligned to a reference to estimate damage')
@click.option('-c',
              '--cov',
              default=0.5,
              type=float,
              show_default=True,
              help='Minimum coverage to consider reference to estimate damage')
@click.option('-s',
              '--show_al',
              is_flag=True,
              help='Show alignments representations')
@click.option('-pl',
              '--plot',
              is_flag=True,
              help='Make the damage plots')
@click.option('--verbose', is_flag=True, help='Verbose mode')
@click.option('-o',
              '--outdir',
              type=click.Path(writable=True),
              default="pydamage_results",
              show_default=True,
              help="Output directory")
def cli(no_args_is_help=True, **kwargs):
    analyze(**kwargs)


if __name__ == "__main__":
    cli()
