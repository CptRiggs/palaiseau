"""Handles palaiseau install, remove, list"""

import json
import subprocess

from pathlib import Path
from palaiseau.constructs import Package


CACHE_DIR = Path("/var/cache/palaiseau")
DB_DIR = Path("/var/lib/palaiseau/db/builtins")


def install(path: str):
    """Installs a provided tar file"""

    try:
        pkg = Package(path)
        name = pkg.get_buildfl().get("name")
        if not name:
            raise ValueError("Package name not found in metadata.")

        extract_path = CACHE_DIR / name
        extract_path.mkdir(parents=True, exist_ok=True)
        pkg.get_tar().extractall(extract_path)

        for file in pkg.get_buildfl().get("files", []):
            src = extract_path / file
            dest = Path("/") / file
            dest.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["install", "-Dm755", str(src), str(dest)], check=True)

        # Install build metadata
        build_src = extract_path / ".build.json"
        build_dest = DB_DIR / name / "build.json"
        build_dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["install", "-Dm644", str(build_src), str(build_dest)], check=True)

        print(f"Package '{name}' installed successfully.")
    except ValueError:
        print("[Error] Install failed")


def info(name: str) -> dict | None:
    """Provides package information"""

    build_path = DB_DIR / name / "build.json"
    try:
        with open(build_path, encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"[Error] Package '{name}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"[Error] Invalid JSON in '{build_path}'.")
        return None

def remove(name: str):
    """Removes a package"""

    build_json = info(name)
    if build_json is not None:
        for file in build_json.get("files")[-1]:
            subprocess.run(["rm", "-rf", file], check=True)
