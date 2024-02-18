# Spatial Transformation #

## Installation ##

TL;DR

``` bash
python -m venv .venv
source .venv/bin/activate

git clone git@github.com:TrafoToolkit/spatial_transformation.git
cd spatial_transformation

pip install -e .
```

## Usage ##

Basic example:

``` python
from transform.position_3d import Position3D
from transform.rotation_3d import Rotation3D
from transform.transform_3d import Transform3D

p_0 = Position3D.from_cartesian(30, 450, 20, Unit.MM_DEG)
o_0 = Rotation3D.from_EULER_INTRINSIC_XYZ(210, 120, 140, Unit.MM_DEG)

sys_R = Transform3D(p_0, o_0)


print(p_0)
```

## Development ##

This project is structured according to the guidelines of [hatchling 1.7](https://hatch.pypa.io/).

### Setup ###

In order to install the requirements for development, install the dependencies from the `requirements.txt`:

This project uses pre-commits. To setup this up, do the following:

```sh
# With activated virtual environment
pip install -r requirements.txt
pre-commit install
```

This will install the pre-commit hook. When trying the next commit, the tools for the code check will be installed. Further commits will not need this setup step.

This will apply the checks to all files in the repository. During a commit only the diff is style-checked, the commit is aborted, if style / format is not according to the configuration.

In order to run the files over all __git-tracked__ files, invoke:

```bash
pre-commit run --all
```

### Testing ###

Testing requires you to install pip packages `pytest pytest-cov`

Run `bash tools/runtest.sh MARKERNAME` for running the tests in `test/` directory. `MARKERNAME` can be
- `randomized` for randomized tests using a random number generator with seed 0
- `hardcoded` for testcases that test if an operation generates a known error, so mathematical problems can be found
- or omitted for running all testcases

Coverage reports will be generated into htmlcov/

### Documentation ###

For building the documentation you need pip packages `Sphinx sphinx-autoapi` and you need to install Sphinx with `apt-get install python3-sphinx`.

Run `bash tools/generate_classdiagrams.sh` for generating classdiagrams in `docs/classdiagrams/` using pyreverse.

[WIP] Run `bash tools/build_docs.sh` for auto-generating documentation in `docs/build/` using sphinx.
