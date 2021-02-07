from setuptools import setup
import re

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("spotify/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("version is not set")

with open("README.rst") as f:
    readme = f.read()

extras_require = {
    "docs": [
        "sphinx==3.0.3",
        "sphinxcontrib_trio==1.1.2",
        "sphinxcontrib-websupport",
    ],
}

setup(
    name="SpotifyPy",
    author="mohamed040406",
    url="https://github.com/mohamed040406/SpotifyPy",
    project_urls={
        "Documentation": "https://SpotifyPy.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/mohamed040406/SpotifyPy/issues",
    },
    version=version,
    packages=[
        "spotify",
        "spotify.models",
        "spotify.models.abc",
        "spotify.models.extras",
        "spotify.models.simple",
    ],
    license="MIT",
    description="A Python wrapper for the Spotify API",
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
