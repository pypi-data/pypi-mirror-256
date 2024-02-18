"""
Module to generate and save a histogram of the number of figures in each article.
"""
from ...plotter import Plotter


def generate_figures_histogram(parsed_data: dict[str, dict[str, str | int]],
                               output_dir: str) -> None:
    """
    Generates and saves to `output_dir` a histogram of the number of figures in each article.
    """
    figures_counts = [data['figures_count']
                      for data in list(parsed_data.values())]
    Plotter(title='Figures per Article',
            x_label='Article',
            x_data=range(0, len(figures_counts)),
            y_label='Figures',
            y_data=figures_counts).generate().save_to_file(output_dir)
