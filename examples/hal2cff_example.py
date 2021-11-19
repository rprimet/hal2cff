from hal2cff import hal2cff
import ipywidgets as widgets
from IPython.display import display, display_html, Markdown

# # hal2cff example
# print(hal2cff("https://hal.archives-ouvertes.fr/hal-01361430v1"))

# +
example_query = "https://hal.archives-ouvertes.fr/hal-01361430v1"
url = widgets.Textarea(value=example_query)
button = widgets.Button(description="Generate CFF")
output = widgets.Output()
display(widgets.HBox([url, button]))
display(button)
display(output)

def generate_cff(_):
    with output:
        output.clear_output()
        # spinner.layout = widgets.Layout(visibility="visible")
        result = hal2cff(url.value)
        result_pre = f"<pre>{result}</pre>"
        display_html(result_pre, raw=True)
    


button.on_click(generate_cff)
# -


