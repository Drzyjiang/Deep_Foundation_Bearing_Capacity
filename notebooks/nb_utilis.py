from pathlib import Path


def find_project_root(marker = "pyproject.toml"):
    p = Path.cwd().resolve()
    while p != p.parent:
        if (p / marker).exists():
            return p
        else:
            p = p.parent
    raise FileNotFoundError(f"No {marker} found")