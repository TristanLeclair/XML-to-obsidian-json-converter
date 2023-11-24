import argparse
import json
import xmltodict

from src.common.converter.helpers import convert_monster


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compendium XML parser to extract monsters"
    )
    parser.add_argument(
        "-i", type=argparse.FileType("r"), metavar="xml file", required=True
    )
    parser.add_argument(
        "-o", type=argparse.FileType("w"), metavar="json file", default="monsters.json"
    )
    parser.add_argument(
        "--format", type=str, choices=["json", "obsidian"], default="json"
    )

    args = parser.parse_args()
    return args.i, args.o, args.format


def main():
    input, output, format = parse_args()
    xml = xmltodict.parse(input.read())
    monsters = xml["compendium"]["monster"]

    if format == "obsidian":
        for monster in monsters:
            convert_monster(monster)

    print(f"Writing {len(monsters)} monsters to {output.name}")
    json.dump(monsters, indent=4, fp=output)
    pass


if __name__ == "__main__":
    main()
