"""
This module contains the function to parse the PDFs using the PDFParser class.
"""

import click
from ...pdf_parser import PDFParser


def parse_pdfs(input_dir: str, output_dir: str) -> None:
    """
    Process all PDFs in the given directory and save the results to the output directory.
    """
    try:
        # Process the PDFs with PDFParser
        PDFParser().process_pdfs(pdf_dir=input_dir,
                                 output_dir=output_dir)
    except ConnectionRefusedError as e:
        click.echo('> The Grobid server is not running')
        raise e
