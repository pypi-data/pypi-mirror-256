"""
This module contains the function to generate keyword clouds for the parsed data.
"""
from os import path
from ...keyword_cloud import KeywordCloud


def generate_keyword_clouds(parsed_data: dict[str, dict[str, str | int]],
                            output_dir: str) -> None:
    """
    Generates and saves a keyword cloud for each abstract in the parsed data.
    """
    for title, data in parsed_data.items():
        KeywordCloud(text=str(data['abstract']),
                     title=title).generate().save_to_file(dir_path=path.join(output_dir, title))
