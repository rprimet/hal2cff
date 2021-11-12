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
    halref: str
        HAL document URL or identifier
    """
    g = Graph()
    g.parse(halref)
    return g


def halref_to_rdf_url(halref):
    """
    halref: str
        HAL document URL or identifier
    
    https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf -> https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf
    https://data.archives-ouvertes.fr/document/hal-02371715 -> https://data.archives-ouvertes.fr/document/hal-02371715.rdf
    https://data.archives-ouvertes.fr/document/hal-02371715v2.json -> https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf
    hal-02371715 -> https://data.archives-ouvertes.fr/document/hal-02371715.rdf
    """
    if halref.startswith("https://data.archives-ouvertes.fr/document/"):
        pass


# +
def rdf_to_canonical(ref):
    assert str(ref).endswith('.rdf')
    return URIRef(str(ref)[:-4])

def canonical_to_rdf(ref):
    return URIRef(f"{str(ref)}.rdf")


# -

rdf_to_canonical(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf"))


def get_latest_version(doc_graph, doc_uri):
    """
    doc_graph: Graph
    doc_uri: URIRef or str
    """
    doc_uri = URIRef(doc_uri)
    # if the document contains a title, return 'doc_uri'.
    # otherwise, see if doc_uri is in one or more 'has_version' relationships,
    # and return the URI of the document whose version seems the highest
    if get_title(doc_graph, doc_uri) is not None:
        return doc_uri
    else:
        print("oh noes")


g = get_hal_graph("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf")

get_latest_version(g, "https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf")

for (sub, obj, pred) in g:
    print(sub,obj,pred)


def get_attribute(doc_graph, doc_uri, attr_name):
    """
    doc_graph: Graph
    doc_uri: URIRef or str
    attr_name: URIRef or str
    """
    
    return doc_graph.value(URIRef(doc_uri), URIRef(attr_name)) 


def get_abstract(doc_graph, doc_uri):
    return get_attribute(doc_graph, doc_uri, URIRef("http://purl.org/dc/terms/abstract"))


get_abstract(g, URIRef("https://data.archives-ouvertes.fr/document/hal-02371715"))


def get_title(doc_graph, doc_uri):
    return get_attribute(doc_graph, doc_uri, URIRef("http://purl.org/dc/terms/title"))


