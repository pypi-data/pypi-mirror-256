import setuptools
import urllib.request
import json


def major(version):
    return int(version.split(".")[0])


def minor(version):
    return int(version.split(".")[1])


def patch(version):
    return int(version.split(".")[2])


def current_major(releases):
    majors = [major(release) for release in releases.keys()]
    return max(majors)


def current_minor(releases):
    minors = [minor(release) for release in releases.keys()]
    return max(minors)


def current_patch(releases):
    patches = [patch(release) for release in releases.keys()]
    return max(patches)


def releases(package="automait_client") -> str:
    req = urllib.request.Request(f"https://pypi.python.org/pypi/{package}/json")
    r = urllib.request.urlopen(req)
    if r.code == 200:
        t = json.loads(r.read())
        releases = t.get("releases", [])
        if releases:
            print(releases)
            return releases


def new_v():
    rel = releases()
    new_version = f"{current_major(rel)}.{current_minor(rel)}.{current_patch(rel)+1}"
    print(f'pushing to version: {".".join(new_version)}')
    return new_version


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="automait_client",
    version=new_v(),
    author="Lukas Leuschen",
    author_email="lukas.leuschen@automait.ai",
    description="automait package for interfacing our modeling services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/automait_public/automait_client",
    project_urls={
        "Bug Tracker": "https://gitlab.com/automait_public/automait_client/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.11",
)
