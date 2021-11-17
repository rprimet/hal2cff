# +
import ipywidgets as widgets
from IPython.display import display, display_html, Markdown

from hal2cff import hal2cff
# -

# # hal2cff
#
# Turn a [HAL](https://hal.archives-ouvertes.fr) URL into a draft [CITATION.cff](https://citation-file-format.github.io/) file.

url = widgets.Textarea(value="https://hal.archives-ouvertes.fr/hal-02485642v2")
button = widgets.Button(description="Generate CFF")
spinner = widgets.HTML(value="""
<img width="64" alt="Loading icon cropped" src="https://upload.wikimedia.org/wikipedia/commons/9/92/Loading_icon_cropped.gif">
""", layout=widgets.Layout(visibility="hidden"))
display(widgets.HBox([url, button]))
output = widgets.Output()
display(output)


def generate_cff(_):
    with output:
        output.clear_output()
        spinner.layout = widgets.Layout(visibility="visible")
        try:
            result = hal2cff(url.value)
            result_pre = f"<pre>{result}</pre>"
            display_html(result_pre, raw=True)
        finally:
            spinner.layout = widgets.Layout(visibility="hidden")


button.on_click(generate_cff)


