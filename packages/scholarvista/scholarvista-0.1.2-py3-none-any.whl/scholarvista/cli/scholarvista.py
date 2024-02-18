#!/usr/bin/env python3

"""
Command Line Interface for the scholarvista package.
"""
import os
from tempfile import TemporaryDirectory
import click
from .utils.parse_pdfs import parse_pdfs
from .utils.parse_tei_xmls import parse_tei_xmls
from .utils.generate_links_list import generate_links_list
from .utils.generate_keyword_clouds import generate_keyword_clouds
from .utils.generate_figures_histogram import generate_figures_histogram


@click.group()
@click.pass_context
@click.option('--input-dir',
              required=True,
              type=click.Path(exists=True),
              help='Directory containing PDF files.')
@click.option('--output-dir',
              type=click.Path(),
              default=os.getcwd(),
              help='Directory to save results. Defaults to current directory.')
def cli(ctx,
        input_dir: str,
        output_dir: str) -> None:
    """
    ScholarVista's CLI main entry point.
    """
    if not os.path.exists(output_dir):
        response = click.prompt(f'''Output directory '{
            output_dir}' does not exist.\nDo you want to create it? [y/n]''',
            default='y',
            show_default=True)
        if response.lower() == 'y':
            os.makedirs(output_dir)
        else:
            click.echo(
                'ScholarVista cannot proceed without a valid input directory.')
            return
    ctx.obj = {
        'input_dir': input_dir,
        'output_dir': output_dir,
    }


@cli.command(name='process-pdfs')
@click.pass_context
def process_pdfs(ctx) -> None:
    """
    Process all PDFs in the given directory.
    """
    input_dir, output_dir = ctx.obj['input_dir'], ctx.obj['output_dir']
    parsed_data = {}

    with TemporaryDirectory() as tmp_dir:
        print(f'> Processing all PDF files in {input_dir}...')
        parse_pdfs(input_dir=input_dir, output_dir=tmp_dir)

        print('> Processing all TEI XML files...')
        parsed_data = parse_tei_xmls(input_dir=input_dir)

    generate_data(parsed_data=parsed_data, output_dir=output_dir)

    print('> Done!')


@cli.command(name='process-xmls')
@click.pass_context
def process_xmls(ctx) -> None:
    """
    Process all TEI XMLs in the given directory.
    """
    input_dir, output_dir = ctx.obj['input_dir'], ctx.obj['output_dir']

    print('> Processing all TEI XML files...')
    parsed_data = parse_tei_xmls(input_dir=input_dir)

    generate_data(parsed_data=parsed_data, output_dir=output_dir)

    print('> Done!')


def generate_data(parsed_data: dict[str, dict[str, str | int]],
                  output_dir: str) -> None:
    """
    Generates and saves the keyword clouds, links lists, and figures histogram.
    """
    print('> Generating Directory Structure...')
    generate_directories(titles=list(parsed_data.keys()),
                         output_dir=output_dir)

    print('> Generating Keyword Clouds...')
    generate_keyword_clouds(parsed_data=parsed_data,
                            output_dir=output_dir)

    print('> Generating Links Lists...')
    generate_links_list(parsed_data=parsed_data,
                        output_dir=output_dir)

    print('> Generating Figures Histogram...')
    generate_figures_histogram(parsed_data=parsed_data,
                               output_dir=output_dir)


def generate_directories(titles: list[str], output_dir: str) -> None:
    """
    Generates the directory structure for the output.
    """
    for title in titles:
        os.makedirs(os.path.join(output_dir, title), exist_ok=True)


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    # The Click library will automatically pass the parameters to the main function.
    cli()
