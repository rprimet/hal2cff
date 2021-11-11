from rdflib import Graph, URIRef
import rdflib


def hal2cff(halref):
    """
    halref: str
        HAL document URL or identifier
    """
    pass


def get_hal_graph(halref):
    """
    """
    g = Graph()
    g.parse(halref)
    return g


def halref_to_url(halref):
    """
    https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf -> https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf
    https://data.archives-ouvertes.fr/document/hal-02371715 -> https://data.archives-ouvertes.fr/document/hal-02371715.rdf
    https://data.archives-ouvertes.fr/document/hal-02371715v2.json -> https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf
    hal-02371715 -> https://data.archives-ouvertes.fr/document/hal-02371715.rdf
    """
    if halref.startswith("https://data.archives-ouvertes.fr/document/"):
        pass


def get_latest_version(doc):
    """
    doc: Graph
    """
    pass


g = get_hal_graph("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf")

for (sub, obj, pred) in g:
    print(sub,obj,pred)


def get_abstract(doc_graph):
    return doc_graph.value(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2"), URIRef("http://purl.org/dc/terms/abstract")).value


abstract = get_abstract(g)

abstract


