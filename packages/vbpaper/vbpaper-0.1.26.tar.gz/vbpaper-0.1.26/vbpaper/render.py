import click
import os

@click.command(
        help="Renders pngs into pdf"
        )
@click.option(
    '-t',
    '--title',
    type=str,
    default='Plant Morphology',
    show_default=True,
    help="Title"
    )
@click.option(
    '-n',
    '--no_of_pngs',
    type=int,
    default=1,
    show_default=True,
    help="No of pngs"
    )
@click.option(
    '-e',
    '--eps',
    is_flag=True,
    help="eps"
    )
@click.option(
    '-c',
    '--columns',
    type=int,
    default=1,
    show_default=True,
    help="No of columns"
    )
def render(title, no_of_pngs, eps, columns):
    """Renders pngs into pdf"""
    from .functions import create_main_tex_file, render_to_pdf, rename_png_to_eps
    cwd = os.getcwd()
    if eps:
        rename_png_to_eps(cwd)
        create_main_tex_file(cwd, title, no_of_pngs, eps, columns)
    else:
        create_main_tex_file(cwd, title, no_of_pngs, eps, columns)
    render_to_pdf(cwd)
    click.echo('Paper rendered successfully')
