from rdflib import URIRef
from cffconvert import Citation
from hal2cff._hal2cff import get_author_nodes, get_hal_graph, hal2cff, hal_document, halref_to_data_url, to_canonical, to_rdf

def test_halref_to_data_url():
    assert halref_to_data_url("https://hal.archives-ouvertes.fr/hal-02371715v2") == "https://data.archives-ouvertes.fr/document/hal-02371715v2"
    assert halref_to_data_url("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf") == "https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf"
    assert halref_to_data_url("https://data.archives-ouvertes.fr/document/hal-02371715v2") == "https://data.archives-ouvertes.fr/document/hal-02371715v2"

    
def test_to_canonical():
    assert to_canonical(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf")) == URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2")
    assert to_canonical(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2")) == URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2")

    
def test_to_rdf():
    assert to_rdf(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2")) == URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf")
    assert to_rdf(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf")) == URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf")


def test_get_author_nodes():
    assert len(list(get_author_nodes(get_hal_graph("https://data.archives-ouvertes.fr/document/hal-02485642v2")))) == 8
    # the document below has a corresponding author in addition to the authors
    assert len(list(get_author_nodes(get_hal_graph("https://data.archives-ouvertes.fr/document/inria-00582640v2")))) == 4


def test_hal_document():
    model = hal_document("https://hal.archives-ouvertes.fr/hal-01361430v1")
    assert "Progressive Analytics" in model['title']
    assert "sequential computations" in model['abstract']
    assert len(model['authors']) == 2

    
def test_hal2cff():
    dump = hal2cff("https://hal.archives-ouvertes.fr/hal-02371715")
    assert "DiCoDiLe" in dump
    other_dump = hal2cff("https://hal.archives-ouvertes.fr/hal-02485642")
    assert "Primet" in other_dump


def test_hal2cff_validate():
    dump = hal2cff("https://hal.archives-ouvertes.fr/inria-00582640")
    Citation(dump).validate()
