from rdflib import Graph, RDF, URIRef
import rdflib
import yaml
from urllib.parse import urlparse, urlunparse
from dataclasses import dataclass


def get_hal_graph(halref) -> Graph:
    """
    halref: URIRef or str
        HAL document URL or identifier
    """
    g = Graph()
    g.parse(to_rdf(halref))
    return g


def halref_to_data_url(halref: str) -> str:
    """
    Given a HAL or HAL-data document URIRef, returns the corresponding HAL-data URL
    halref: str
        HAL document URL
    (Most important!) https://hal.archives-ouvertes.fr/hal-02371715v2 -> https://data.archives-ouvertes.fr/document/hal-02371715v2
    https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf -> https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf
    https://data.archives-ouvertes.fr/document/hal-02371715 -> https://data.archives-ouvertes.fr/document/hal-02371715
    """
    parsed_ref = urlparse(halref)
    assert "archives-ouvertes.fr" in parsed_ref.netloc, "Expected HAL (or HAL-data) document URL"
    assert "hal-" in parsed_ref.path, "Expected HAL (or HAL-data) document URL"
    if "hal.archives-ouvertes.fr" in parsed_ref.netloc:
        parsed_ref = parsed_ref._replace(netloc="data.archives-ouvertes.fr",
                                         path=f"/document{parsed_ref.path}")
    return urlunparse(parsed_ref)


