from rdflib import Graph, RDF, URIRef
import rdflib
import yaml
from urllib.parse import urlparse, urlunparse


def get_hal_graph(halref) -> Graph:
    """
    Given a HAL document URI, returns the corresponding Graph.
    
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


# +
def to_canonical(halref) -> URIRef:
    """
    halref: URIRef or str
        HAL document URI
    """
    if str(halref).endswith('.rdf'):
        return URIRef(str(halref)[:-4])
    else:
        return halref

def to_rdf(halref) -> URIRef:
    """
    halref: URIRef or str
        HAL document URI
    """
    if not str(halref).endswith('.rdf'):
        return URIRef(f"{str(halref)}.rdf")
    else:
        return halref


# -

def get_attribute(doc_graph, doc_uri, attr_name):
    """
    Retrieves an object whose subject is the canonical version of 'doc_uri' and whose
    predicate is 'attr_name'.
    
    doc_graph: Graph
    doc_uri: URIRef or str
    attr_name: URIRef or str
    """
    return doc_graph.value(to_canonical(URIRef(doc_uri)), URIRef(attr_name)) 


def get_abstract(doc_graph, doc_uri):
    return get_attribute(doc_graph, doc_uri, URIRef("http://purl.org/dc/terms/abstract"))


def get_title(doc_graph, doc_uri):
    return get_attribute(doc_graph, doc_uri, URIRef("http://purl.org/dc/terms/title"))


def get_one_version(doc_graph, doc_uri) -> URIRef:
    """
    A HAL document may be either a 'concrete' version of a document, 
    or a canonical document that points to one or more versions.
    
    get_one_version attempts to return the URI of a 'concrete' version.
    
    doc_graph: Graph
    doc_uri: URIRef or str
    """
    doc_uri = URIRef(doc_uri)
    
    if get_title(doc_graph, doc_uri) is not None:
        return doc_uri
    else:
        doc_versions = list(doc_graph.objects(to_canonical(doc_uri), URIRef("http://purl.org/dc/terms/hasVersion")))
        assert doc_versions, "no version found"
        return doc_versions[0]


def get_latest_version(doc_uri) -> URIRef:
    """
    Get the latest version of a document by following 'isReplacedBy' links
    """
    doc_graph = Graph().parse(to_rdf(doc_uri))
    while (replaced_by := get_attribute(doc_graph, doc_uri, "http://purl.org/dc/terms/isReplacedBy")) is not None:
        doc_uri = replaced_by
        doc_graph = Graph()
        doc_graph.parse(to_rdf(doc_uri))
    return doc_uri


def get_author_nodes(doc_graph: Graph):
    return doc_graph.subjects(RDF.type, URIRef("http://data.archives-ouvertes.fr/schema/Author"))


def hal_document(halref):
    """
    halref: str
        HAL document URL or identifier
    """
    halref = halref_to_data_url(halref)
    halref = to_canonical(halref)
    graph = get_hal_graph(halref)
    one_version_halref = get_one_version(graph, halref)
    latest_version = get_latest_version(one_version_halref)
    
    latest_doc_graph = get_hal_graph(latest_version)
    title = get_title(latest_doc_graph, latest_version).value  # XXX None case (value)
    abstract = get_abstract(latest_doc_graph, latest_version).value  # XXX None case (value)
    
    authors = []
    for node in get_author_nodes(latest_doc_graph):
        author_doc_ref = next(latest_doc_graph.objects(node, URIRef("http://data.archives-ouvertes.fr/schema/person")))
        author_graph = get_hal_graph(author_doc_ref)
        fname = get_attribute(author_graph, author_doc_ref, "http://xmlns.com/foaf/0.1/firstName")
        lname = get_attribute(author_graph, author_doc_ref, "http://xmlns.com/foaf/0.1/familyName")
        authors.append({'given-names': fname.value, 'family-names': lname.value})
    
    return {
        'title': title, 
        'abstract': abstract,
        'authors': authors
    }


def dump_cff(doc):
    """
    Note that while we do a "credit redirection" style CFF, the spec
    requires authors and title both at the top-level and at the preferred-citation level
    (those may be different of course, but since we are only extracting bibliographical info
    from HAL, we'll fill them with identical values)
    """
    return yaml.safe_dump({
        'cff-version': '1.2.0',
        'message': "If you use this software, please cite both the article from preferred-citation and the software itself.",
        'title': doc['title'],
        'authors': doc['authors'],
        'preferred-citation': {
            'title': doc['title'],
            'abstract': doc['abstract'],
            'authors': doc['authors'],
            'type': 'generic',
        }
    })


def hal2cff(halref):
    """
    """
    doc = hal_document(halref)
    return dump_cff(doc)
