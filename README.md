# hal2cff

Want to add a [CITATION.cff](https://citation-file-format.github.io/) file to your repository? Already have a publication in [HAL](https://hal.archives-ouvertes.fr)?
`hal2cff` will attempt to draft a citation file from the HAL document metadata.

## Caveats

- `hal2cff` is meant to fill in metadata (and alleviate the chore of doing so) and create a draft CITATION.cff file, **not** 
a finished one that can be checked-in unmodified
- early WIP
- missing features (in particular, affiliations, and document type -- for now set to `generic`)
- This will create a "credit redirection"-style CITATION.cff, which may not be optimal (as the software itself should be cited)
