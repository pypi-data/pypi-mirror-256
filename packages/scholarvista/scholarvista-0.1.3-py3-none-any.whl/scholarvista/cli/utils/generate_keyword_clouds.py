"""
This module contains the function to generate keyword clouds for the parsed data.
"""
from functools import reduce
from os import path
from typing import List
from ...keyword_cloud import KeywordCloud


def generate_keyword_clouds(parsed_data: dict[str, dict[str, str | int]],
                            output_dir: str) -> None:
    """
    Generates and saves a keyword cloud for all the abstracts in the parsed data
    and a keyword cloud of each abstract in the parsed data.
    """

    titles: List[str] = []
    abstracts: List[str] = []
    for title, data in parsed_data.items():
        titles.append(title)
        abstracts.append(str(data['abstract']))

    # Generate a global keyword cloud
    KeywordCloud(text=reduce(lambda a, b: a + b, abstracts),
                 title='All Abstracts').generate().save_to_file(dir_path=output_dir)

    # Generate a keyword cloud for every abstract
    for title, abstract in zip(titles, abstracts):
        KeywordCloud(text=abstract,
                     title=title).generate().save_to_file(dir_path=path.join(output_dir, title))
