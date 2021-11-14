from hal2cff import hal2cff

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
# Extra credits: 
# - tools/UIs to wrangle affiliation data, 
# - first/other authors distinction, 
# - keywords, 
# - search docs with the HAL API directly,
# - et caetera
#
# Stuff that would be nice but not trivial to do (and it's irksome): "copy to clipboard" button, urlparams...
#
# Point to make: really nice for projects that require a server side but no (writable) DB 

print(hal2cff("https://hal.archives-ouvertes.fr/hal-01361430v1"))


