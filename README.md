# Python XML converter

A little 2 day project I created to convert some XML files to a valid json format for D&D in Obsidian.

This project specifically converts monsters from fight club 5e to a json format that can be imported in Obsidian by the [Fantasy-statblocks plugin](https://github.com/javalent/fantasy-statblocks/).

## Usage

### Python (by hand)

`python -m scripts.python.convert_to_json -h` for help

`python -m scripts.python.convert_to_json -i <path/to/xml/data> -o <output/path> --format obsidian` to convert the xml and output to the given path

`python -m scripts.python.convert_to_json -i <path/to/xml/data> -o <output/path> --format json` will convert the xml to straight json and output to the given path

### Make

*note: you need to have a file in `data/` and update the Makefile variable with the correct name of the file in order to run the makefile*

`make convert_monsters_to_obsidian` will convert the `data/monsters.xml` file to `data/monsters.json` and place it in the `monsters_obsidian.json` file.
