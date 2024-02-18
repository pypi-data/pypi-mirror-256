import urllib.request
import json

from packaging.version import Version


def current_pypi_version(package: str) -> str:
    req = urllib.request.Request(f"https://pypi.python.org/pypi/{package}/json")
    r = urllib.request.urlopen(req)
    if r.code == 200:
        t = json.loads(r.read())
        releases = t.get("releases", [])
        if releases:
            release_numbers = list(releases.keys())
            release_numbers.sort(key=Version)
            return release_numbers[-1]


def new_v():
    current_version = current_pypi_version(package="automait_client").split(".")
    current_version.append(str((int(current_version.pop()) + 1)))
    return ".".join(current_version)


__version__ = new_v()
