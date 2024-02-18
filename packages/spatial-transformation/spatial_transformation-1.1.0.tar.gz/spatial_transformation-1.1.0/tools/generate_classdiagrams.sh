mkdir -p docs/diagrams
mkdir -p docs/diagrams/3d
mkdir -p docs/diagrams/2d

pyreverse src/transform/*3d.py src/transform/utils.py src/transform/definitions.py -o png -d docs/diagrams/3d -f ALL
pyreverse src/transform/*2d.py src/transform/utils.py src/transform/definitions.py -o png -d docs/diagrams/2d -f ALL

pyreverse src/transform/ -o png -d docs/diagrams/ -f ALL
