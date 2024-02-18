"""
This file contains the PDFParser class, which is used to process PDFs using Grobid.
"""
import os
from grobid_client.grobid_client import GrobidClient

# pylint: disable=too-few-public-methods
# It is a good practice to keep the classes small and focused on a single task.


class PDFParser:
    """
    Analyzes and extracts content of PDF files using Grobid.
    """

    def __init__(self) -> None:
        """
        Initializes the PDFParser object by creating a Grobid Client.
        """
        try:
            print('> Connecting to Grobid server...')
            self.grobid_client = GrobidClient(
                config_path=f'.{os.sep}config.json')
        except ConnectionRefusedError as e:
            raise ConnectionRefusedError(
                '> The Grobid server is not running') from e

    def process_pdfs(self, pdf_dir: str, output_dir: str) -> None:
        """
        Processes all the PDFs contained in the `pdf_dir` directory and
        leaves the results in the `output_dir` directory.
        """
        self.grobid_client.process(service='processFulltextDocument',
                                   input_path=pdf_dir,
                                   output=output_dir)
