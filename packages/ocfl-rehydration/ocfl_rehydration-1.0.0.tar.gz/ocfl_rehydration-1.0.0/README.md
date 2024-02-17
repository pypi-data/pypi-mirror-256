# OCFL Rehydration
OCFL Rehydration reconstitutes DRS objects from their OCFL representation

This tool has no dependencies on any external services such as the DRS database or storage.
The expectation is that the OCFL object root directory for a DRS object exists on local disk.
This tool takes as input the location of the OCFL object root directory and recreates the a representation of the DRS object in a form similar to what the depositor initially supplied in the DRS batch for ingest.
Specifically, the resultant object is created in a directory named after the supplied object name;
the data files are created with their supplied file names within directories named with their supplied names.

## Build
The tool is a python command-line application that is designed to be run within a Docker container.
To build the Docker image:
```
docker build -t rehydrate:latest .
```
## Usage
To run the application after a Docker image has been built as detailed above:
```
docker run --rm --mount type=bind,source=${PWD},target=/tmp -it rehydrate -h

usage: main.py [-h] -i INPUT_DIR -o OUTPUT_DIR

Converts the OCFL form of a DRS Object and reconstitutes (rehydrates) a form expected by curators. The input is the OCFL
object root directory of object to rehydrate.

options:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input_dir INPUT_DIR
                        Local directory containing the OCFL Object root of the object to rehydrate
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Local directory where rehydrated object will be written
```

### Example
The directory '102559752' is the OCFL object root directory for a DRS object.
OCFL object root directories contain the top-level 'inventory.json', the object version namaste file (e.g. '0=ocfl_object_1.0') and OCFL version directories.
```
docker run --rm --mount type=bind,source=${PWD},target=/tmp -it rehydrate -i /tmp/input/102559752 -o /tmp/output
```
