"""
This module contains the Plotter class which is used to plot a histogram of the given data.
"""

import logging
from os import path
from typing import Self
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.ERROR)


class Plotter:
    """
    This class is used to plot a histogram of the given data.
    """
    # pylint: disable=too-many-arguments
    # The number of arguments is reasonable in this case.

    def __init__(self, title, x_label, x_data, y_label, y_data) -> None:
        """
        Initializes the Plotter object with the given data.
        """
        self.figure_created = False
        self.title = title
        self.x_label = x_label
        self.x_data = x_data
        self.y_label = y_label
        self.y_data = y_data

    def generate(self) -> Self:
        """
        Generates a histogram of the given data.
        """
        plt.bar(self.x_data, self.y_data)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        self.figure_created = True
        return self

    def display(self) -> None:
        """
        Displays a previously generated histogram.
        """
        try:
            if not self.figure_created:
                raise ValueError('The figure has not been generated yet.')
            plt.show()
        except ValueError:
            logging.error('Error displaying the figure: %s', self.title)

    def save_to_file(self, dir_path: str) -> None:
        """
        Saves a previously generated histogram in the specified directory.
        """
        try:
            if not self.figure_created:
                raise ValueError('The figure has not been generated yet.')
            plt.savefig(path.join(dir_path, f'{self.title}.png'))
            plt.close()
        except ValueError:
            logging.error('Error saving the figure: %s', self.title)
