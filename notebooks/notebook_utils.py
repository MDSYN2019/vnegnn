from pathlib import Path

import pandas as pd


def _load_nglview_or_raise():
    """Load nglview lazily so non-visual notebook cells can run without it."""
    try:
        import nglview as nv
        from nglview.shape import Shape
    except ImportError as exc:
        raise ImportError(
            'nglview is required for 3D rendering. Install it with: pip install nglview '
            'and enable widgets for your environment.'
        ) from exc

    return nv, Shape


def render_protein(protein_name: str, df: pd.DataFrame, dataset_path: Path):
    """Render a protein, ligands, and predicted binding site centers in an NGL widget."""
    nv, Shape = _load_nglview_or_raise()

    complex_path = Path(f"{dataset_path}/{protein_name}")
    pdb_file = complex_path / "protein.pdb"
    ligands = [lig for lig in complex_path.glob("ligand_*.pdb")]
    if len(ligands) == 0:
        ligands = [lig for lig in complex_path.glob("ligand_*.mol2")]

    view = nv.show_file(pdb_file.as_posix())
    view.layout.width = "800px"
    view.layout.height = "600px"

    view.clear_representations()
    view.add_representation(
        "surface", selection="protein", opacity=0.3, color="lightblue"
    )
    view.add_representation("cartoon", selection="protein", color="secondary structure")

    for ligand in ligands:
        view.add_component(ligand.as_posix())
        view.add_representation("ball+stick", component=view.n_components - 1)

    shape = Shape(view)

    p = df.loc[lambda x: x["protein_name"] == protein_name].reset_index(drop=True)
    for i, row in p.iterrows():
        confidence = (
            round(row["confidence_0"], 3) if hasattr(row, "confidence_0") else "n/a"
        )
        shape.add_sphere(
            [row["x"], row["y"], row["z"]],
            [1, 0, 0],
            0.8,
            f"Prediction {i} (conf={confidence})",
        )

    view.add_component(shape)

    return view
