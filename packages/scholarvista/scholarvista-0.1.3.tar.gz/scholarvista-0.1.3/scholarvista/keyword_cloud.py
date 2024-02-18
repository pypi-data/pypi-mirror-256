"""
This module contains the KeywordCloud class which is used to generate
and display word clouds from a given text.
"""
import logging
from os import path
from typing import Self
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

logging.basicConfig(level=logging.ERROR)


class KeywordCloud:
    """
    This class is used to generate and display word clouds from a given text.
    """

    def __init__(self, text: str, title: str | None = None) -> None:
        """
        Initializes the KeywordCloud object with the given text.
        """
        self.title = title
        self.words_freq = Counter(text.split())
        self.word_cloud = None

    def generate(self) -> Self:
        """
        Generates the word cloud from the frequency of words in the text.
        """
        self.word_cloud = WordCloud(
            width=800, height=400).generate_from_frequencies(self.words_freq)
        plt.figure(figsize=(10, 5))
        plt.imshow(self.word_cloud, interpolation='bilinear')
        plt.axis('off')
        return self

    def display(self) -> None:
        """
        Displays the generated keyword cloud.
        """
        if self.word_cloud is None:
            raise ValueError('Word cloud has not been generated yet.')
        plt.show()
        plt.close()

    def save_to_file(self, dir_path: str) -> None:
        """
        Saves a previously generated keyword cloud in the desired directory.
        """
        if self.word_cloud is None:
            raise ValueError('Word cloud has not been generated yet.')
        plt.savefig(path.join(dir_path, 'keyword_cloud.png'))
        plt.close()
