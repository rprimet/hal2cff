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

g = get_hal_graph("https://data.archives-ouvertes.fr/document/hal-02371715.rdf")

list(get_author_nodes(get_hal_graph("https://data.archives-ouvertes.fr/document/hal-02371715v2")))

for (sub, obj, pred) in g:
    print(sub,obj,pred)

get_abstract(g, URIRef("https://data.archives-ouvertes.fr/document/hal-02371715"))

get_one_version(g, "https://data.archives-ouvertes.fr/document/hal-02371715")

get_latest_version("https://data.archives-ouvertes.fr/document/hal-02371715v1")

model = hal2cff("https://hal.archives-ouvertes.fr/hal-02371715")
model = hal2cff("https://hal.archives-ouvertes.fr/hal-01361430v1")

model

print(output_cff(model))


