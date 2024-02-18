"""
This module contains the function to parse all the TEI XML files in the input directory
and return the parsed data.
"""
import os
from ...tei_xml_parser import TEIXMLParser


def parse_tei_xmls(input_dir: str) -> dict[str, dict[str, str | int]]:
    """
    Parses all the TEI XML files in the input directory.
    """
    files = [os.path.join(input_dir, file)
             for file in os.listdir(input_dir) if file.endswith('.tei.xml')]
    parsed_data = {}
    for file in files:
        parser = TEIXMLParser(file_path=file)
        parsed_data[parser.get_title()] = {
            'abstract': parser.get_abstract(),
            'figures_count': parser.get_figures_count(),
            'links': parser.get_links()
        }
    return parsed_data
