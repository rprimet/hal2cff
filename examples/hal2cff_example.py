# # hal2cff example

# For the first step, we want to get
# - title
# - abstract
#
# from a HAL reference.
#
# In a second step, we want to format those as a YAML snippet as a valid, preferred-citation CFF file.
#
# In a third step, we want to enrich this with the authors list
#
# In a fourth (and last?) step, we want to add (draft) affiliation data to the authors list
#
# Extra credits: tools/UIs to wrangle affiliation data, first/other authors distinction, keywords, ...
#
# Stuff that would be nice but not trivial to do (and it's irksome): "copy to clipboard" button, urlparams...
#
# Point to make: really nice for projects that require a server side but no (writable) DB 

to_canonical(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf"))

to_canonical(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2"))

to_rdf(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2"))

to_rdf(URIRef("https://data.archives-ouvertes.fr/document/hal-02371715v2.rdf"))

g = get_hal_graph("https://data.archives-ouvertes.fr/document/hal-02371715.rdf")


def get_author_nodes(doc_graph: Graph):
    return doc_graph.subjects(RDF.type, URIRef("http://data.archives-ouvertes.fr/schema/Author"))


list(get_author_nodes(get_hal_graph("https://data.archives-ouvertes.fr/document/hal-02371715v2")))

for (sub, obj, pred) in g:
    print(sub,obj,pred)


def get_attribute(doc_graph, doc_uri, attr_name):
    """
    doc_graph: Graph
    doc_uri: URIRef or str
    attr_name: URIRef or str
    """
    
    return doc_graph.value(to_canonical(URIRef(doc_uri)), URIRef(attr_name)) 


def get_abstract(doc_graph, doc_uri):
    return get_attribute(doc_graph, doc_uri, URIRef("http://purl.org/dc/terms/abstract"))


get_abstract(g, URIRef("https://data.archives-ouvertes.fr/document/hal-02371715"))


def get_title(doc_graph, doc_uri):
    return get_attribute(doc_graph, doc_uri, URIRef("http://purl.org/dc/terms/title"))


def get_one_version(doc_graph, doc_uri) -> URIRef:  # XXX change name, refactor
    """
    doc_graph: Graph
    doc_uri: URIRef or str
    """
    doc_uri = URIRef(doc_uri)
    # if the document contains a title, return 'doc_uri'.
    # otherwise, see if doc_uri is in one or more 'has_version' relationships,
    # and return the URI of the document whose version seems the highest
    
    # get latest version by walking isReplacedBy links
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


get_one_version(g, "https://data.archives-ouvertes.fr/document/hal-02371715")

get_latest_version("https://data.archives-ouvertes.fr/document/hal-02371715v1")


# +
@dataclass
class HALAuthor:
    firstName: str
    familyName: str

@dataclass
class HALDocument:
    title: str
    abstract: str
    authors: list[HALAuthor]


# -

def hal2cff(halref):
    """
    halref: str
        HAL document URL or identifier
    """
    halref = halref_to_data_url(halref)
    halref = to_canonical(halref)
    graph = get_hal_graph(halref)
    one_version_halref = get_one_version(graph, halref)
    latest_version = get_latest_version(one_version_halref)
    graph = get_hal_graph(latest_version)  # XXX do not reuse name!
    title = get_title(graph, latest_version).value  # XXX None case
    abstract = get_abstract(graph, latest_version).value  # XXX None case
    
    # XXX refactor!
    authors = []
    for node in get_author_nodes(graph):
        author_doc_ref = next(graph.objects(node, URIRef("http://data.archives-ouvertes.fr/schema/person")))
        author_graph = get_hal_graph(author_doc_ref)
        fname = get_attribute(author_graph, author_doc_ref, "http://xmlns.com/foaf/0.1/firstName")
        lname = get_attribute(author_graph, author_doc_ref, "http://xmlns.com/foaf/0.1/familyName")
        authors.append(HALAuthor(firstName=fname.value, familyName=lname.value))
    
    return HALDocument(title=title, abstract=abstract, authors=authors)


model = hal2cff("https://hal.archives-ouvertes.fr/hal-02371715")
model = hal2cff("https://hal.archives-ouvertes.fr/hal-01361430v1")

model


def output_cff(doc: HALDocument):
    return yaml.dump({
        'cff-version': '1.2.0',
        'message': "If you use this software, please cite both the article from preferred-citation and the software itself.",
        'preferred-citation': {
            'title': doc.title,
            'abstract': doc.abstract,
            'authors': doc.authors
        }
    })


print(output_cff(model))


