"""
This module is the main module of the scholarvista package.
"""

from .exceptions.tag_not_found_in_tei_xml import TagNotFoundInTeiXmlException
from .keyword_cloud import KeywordCloud
from .plotter import Plotter
from .tei_xml_parser import TEIXMLParser
from .pdf_parser import PDFParser
from .cli.scholarvista import cli

__all__ = ['TagNotFoundInTeiXmlException', 'KeywordCloud',
           'Plotter', 'TEIXMLParser', 'PDFParser', 'cli']
