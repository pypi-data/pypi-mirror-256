"""
Module to generate a list of links from the parsed data.
"""
from os import path


def generate_links_list(parsed_data: dict[str, dict[str, str | int]],
                        output_dir: str) -> None:
    """
    Generates and saves to `output_dir` a list of links for each article in the parsed data.
    """
    for title, data in parsed_data.items():
        with open(path.join(output_dir, title, 'links_list.txt'), 'w', encoding='utf-8') as file:
            file.write('\n'.join(data['links']))
