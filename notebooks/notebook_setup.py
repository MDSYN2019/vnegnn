import os
from pathlib import Path

from dotenv import load_dotenv


def _find_project_root(start: Path, indicator: str = '.project-root') -> Path:
    """Find the project root by walking parent directories."""
    for candidate in [start, *start.parents]:
        if (candidate / indicator).exists():
            return candidate
    raise FileNotFoundError(
        f"Could not locate project root (missing '{indicator}') starting from {start}"
    )


def setup_notebook():
    """Setup notebook environment with proper path handling and environment variables.

    This function first tries `rootutils` (if installed). If unavailable, it falls back to a
    pure pathlib-based root discovery so notebooks remain usable in lighter environments.
    """
    notebook_dir = Path(os.getcwd()).resolve()

    try:
        import rootutils

        root_path = Path(
            rootutils.setup_root(
                notebook_dir.as_posix(), indicator='.project-root', pythonpath=True
            )
        )
    except ImportError:
        root_path = _find_project_root(notebook_dir)
        if str(root_path) not in os.sys.path:
            os.sys.path.insert(0, str(root_path))

    os.chdir(root_path)

    env_path = root_path / '.env'
    if env_path.exists():
        load_dotenv(env_path.as_posix(), override=True)

    return root_path
