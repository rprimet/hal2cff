from rdflib import URIRef
from hal2cff._hal2cff import get_hal_graph, halref_to_data_url, to_canonical, to_rdf

def test_halref_to_data_url():
    assert halref_to_data_url("https://hal.archives-ouvertes.fr/hal-02371715v2") == "https://data.archives-ouvertes.fr/document/hal-02371715v2"
    assert halref_to_data_url("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf") == "https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf"
    assert halref_to_data_url("https://data.archives-ouvertes.fr/document/hal-02371715v2") == "https://data.archives-ouvertes.fr/document/hal-02371715v2"

    
def test_to_canonical():
    assert to_canonical(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf")) == URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2")
    assert to_canonical(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2")) == URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2")
    