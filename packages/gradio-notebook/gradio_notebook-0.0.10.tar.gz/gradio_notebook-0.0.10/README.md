# gradio_notebook

A Custom Gradio component to build AI Notebooks powered by AIConfig.
See https://aiconfig.lastmileai.dev/docs/gradio-notebook for full documentation.

## Example usage

Please see the demo/app.py for full details, but generally all you need to do
is add these lines to your component:

```python
import gradio as gr
from gradio_notebook import GradioNotebook

with gr.Blocks() as demo:
    GradioNotebook()

demo.queue().launch()
```

Configure the default AIConfig for the notebook by specifying a path to the config:

```python
import gradio as gr
from gradio_notebook import GradioNotebook

with gr.Blocks() as demo:
    GradioNotebook(config_path="./my_app.aiconfig.json")

demo.queue().launch()
```

For the remaining commands for local development, please follow the
instructions from the `README-dev.md` file!
