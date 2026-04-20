# Notebook usage

## Opening notebooks reliably

From repository root:

```bash
jupyter lab
# or
jupyter notebook
```

Open `notebooks/bindingsite/analyse_preds.ipynb`.

The notebook now uses `notebooks/notebook_setup.py` to automatically locate the project root and load `.env` if available.

## Visualization dependencies

3D rendering uses `nglview` and Jupyter widgets. If visualization cells fail, install/enable:

```bash
pip install nglview ipywidgets
jupyter-nbextension enable nglview --py --sys-prefix
jupyter-nbextension enable --py widgetsnbextension --sys-prefix
```

(For JupyterLab, ensure your lab version has widget manager support.)

## Notebook sections (`analyse_preds.ipynb`)

The notebook is annotated with markdown sections explaining each stage:

1. Environment setup.
2. Imports.
3. Load prediction outputs and dataset paths.
4. Interactive protein rendering.
5. Clustering choice.
6. DCA/DCC metric computation loop.
7. DCA summary + averages.
8. DCC summary + averages.
