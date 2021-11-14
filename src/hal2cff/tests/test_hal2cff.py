from rdflib import URIRef
from hal2cff._hal2cff import get_hal_graph, halref_to_data_url

def test_halref_to_data_url():
    assert halref_to_data_url("https://hal.archives-ouvertes.fr/hal-02371715v2") == "https://data.archives-ouvertes.fr/document/hal-02371715v2"
