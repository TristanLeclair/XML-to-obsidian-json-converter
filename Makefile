compendium_path=data/191328_Complete.xml

run-tests:
	@echo "Running tests..."
	@python3 -m unittest discover -s tests -v

read_monsters_from_compendium: Complete.json
	@echo "Reading monsters from compendium..."
	@python3 -m scripts.python.convert_to_json -i $(compendium_path) -o monsters.json

convert_monsters_to_obsidian: Complete.json
	@echo "Converting monsters to obsidian format..."
	@python3 -m scripts.python.convert_to_json -i $(compendium_path) -o monsters_obsidian.json --format obsidian
