"""
This file contains the TeiXmlParser class, which is used to parse TEI XML files.

The TeiXmlParser class provides methods to extract information from TEI XML files,
such as the title, abstract, body text, figures count, and links.
"""

import logging
import xml.etree.ElementTree as ET
from .exceptions.tag_not_found_in_tei_xml import TagNotFoundInTeiXmlException
from ._utils import get_links_from_text


logging.basicConfig(level=logging.ERROR)


class TEIXMLParser:
    """
    The TEIXMLParser class is used to parse TEI XML files.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes the TEIXMLParser object with the given file path.
        """
        try:
            self.file_path = file_path
            self.namespace = 'http://www.tei-c.org/ns/1.0'
            self.root = ET.parse(self.file_path).getroot()
            self.body = self.__find_element_by_tag('body')
        except FileNotFoundError as e:
            logging.error('File not found: %s', file_path)
            raise e
        except ET.ParseError as e:
            logging.error('Error parsing XML file: %s', file_path)
            raise e
        except TagNotFoundInTeiXmlException as e:
            raise e

    def get_title(self) -> str:
        """
        Returns the text of the title of the document.
        """
        try:
            return self.__get_text_by_tag('title')
        except TagNotFoundInTeiXmlException as e:
            raise e

    def get_abstract(self) -> str:
        """
        Returns the text of the abstract of the document.
        """
        try:
            element = self.__find_element_by_tag('abstract')
            return str(element[0][0].text)
        except TagNotFoundInTeiXmlException as e:
            logging.error("Tag 'abstract' not found in: %s", self.file_path)
            raise e

    def get_body(self) -> str:
        """
        Returns the text of the body of the document.
        """
        try:
            body_text = ''
            for paragraph in self.body.iter(self.__wrap_tag_with_namespace('p')):
                if paragraph.text is not None:
                    body_text += f'{paragraph.text} '
            return body_text
        except AttributeError as e:
            logging.error("Invalid XML structure: missing body element")
            raise e

    def get_figures_count(self) -> int:
        """
        Returns the number of figures in the document.
        """
        try:
            return len(list(self.body.iter(self.__wrap_tag_with_namespace('figure'))))
        except AttributeError as e:
            logging.error("Invalid XML structure: missing body element")
            raise e

    def get_links(self) -> list[str]:
        """
        Returns a list of links found in the document.
        """
        try:
            links = []
            for elem in self.root.iter():
                if elem.text is None:
                    continue
                links.extend(get_links_from_text(elem.text))
            return links
        except Exception as e:
            logging.error("Error occurred while extracting links")
            raise e

    def __get_text_by_tag(self, tag: str) -> str:
        try:
            element = self.__find_element_by_tag(tag)
            return str(element.text)
        except TagNotFoundInTeiXmlException as e:
            logging.error("Tag '%s' not found in: %s", tag, self.file_path)
            raise e

    def __find_element_by_tag(self, tag: str) -> ET.Element:
        """
        Returns the first element with the given tag in the document.
        Raises `TagNotFoundInTeiXmlException` if the tag is not found in the document.
        """
        elem = None
        for e in self.root.iter(self.__wrap_tag_with_namespace(tag)):
            elem = e
            break

        if elem is None:
            raise TagNotFoundInTeiXmlException(f'The {tag} tag was not found')

        return elem

    def __wrap_tag_with_namespace(self, tag: str) -> str:
        """
        Wraps the given tag with the TEI namespace.
        """
        return '{' + self.namespace + '}' + tag
