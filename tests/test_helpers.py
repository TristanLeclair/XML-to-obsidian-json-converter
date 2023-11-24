import unittest

from src.common.converter.helpers import (
    convert_skillsaves,
    fix_hp,
    convert_size,
    convert_stats,
    convert_saves,
    convert_resistances,
    add_bestiary_trait,
    convert_traits,
    convert_actions,
    convert_legendary_actions,
    convert_spells,
    convert_slots,
    convert_environment,
)


class TestHelpers(unittest.TestCase):
    def test_fix_hp_normal(self):
        monster = {"hp": "19 (3d10+3)"}
        fix_hp(monster)
        self.assertEqual(monster["hp"], "19")
        self.assertEqual(monster["hit_dice"], "3d10 + 3")

    def test_fix_hp_no_hit_dice(self):
        monster = {"hp": "19"}
        fix_hp(monster)
        self.assertEqual(monster["hp"], "19")
        self.assertEqual(monster["hit_dice"], "")

    def test_fix_hp_multiple_hit_dice(self):
        monster = {"hp": "19 (3d10+3+4d10)"}
        fix_hp(monster)
        self.assertEqual(monster["hp"], "19")
        self.assertEqual(monster["hit_dice"], "3d10 + 3 + 4d10")

    def test_fix_hp_no_hp(self):
        monster = {"hp": None}
        fix_hp(monster)
        self.assertEqual(monster["hp"], "")
        self.assertEqual(monster["hit_dice"], "")

    def test_convert_size(self):
        monster = {"size": "M"}
        convert_size(monster)
        self.assertEqual(monster["size"], "Medium")

    def test_convert_size_invalid(self):
        monster = {"size": "A"}
        convert_size(monster)
        self.assertEqual(monster["size"], "Medium")

    def test_convert_stats(self):
        monster = {
            "str": "10",
            "dex": "11",
            "con": "12",
            "int": "13",
            "wis": "14",
            "cha": "15",
        }
        convert_stats(monster)
        self.assertEqual(
            monster["stats"],
            ["10 (0)", "11 (0)", "12 (+1)", "13 (+1)", "14 (+2)", "15 (+2)"],
        )
        self.assertEqual(monster.get("str"), None)
        self.assertEqual(monster.get("dex"), None)
        self.assertEqual(monster.get("con"), None)
        self.assertEqual(monster.get("int"), None)
        self.assertEqual(monster.get("wis"), None)
        self.assertEqual(monster.get("cha"), None)

    def test_convert_saves(self):
        monster = {"save": "Str +1, Wis +5, Cha +6"}
        convert_saves(monster)
        self.assertEqual(
            monster["saves"],
            [
                {"strength": 1},
                {"wisdom": 5},
                {"charisma": 6},
            ],
        )
        self.assertEqual(monster.get("save"), None)

    def test_convert_skills(self):
        monster = {"skill": "Perception +5, Stealth +3"}
        convert_skillsaves(monster)
        self.assertEqual(
            monster["skillsaves"],
            [
                {"perception": 5},
                {"stealth": 3},
            ],
        )
        self.assertEqual(monster.get("skill"), None)

    def test_convert_resistances(self):
        monster = {
            "resist": "fire, bludgeoning, piercing, and slashing from nonmagical attacks",
            "vulnerable": "fire",
            "immune": "poison",
            "conditionImmune": "poisoned",
            "senses": "darkvision 60 ft.",
            "passive": "10",
        }
        convert_resistances(monster)
        self.assertEqual(
            monster["damage_resistances"],
            "fire, bludgeoning, piercing, and slashing from nonmagical attacks",
        )
        self.assertEqual(monster.get("resist"), None)
        self.assertEqual(monster["damage_vulnerabilities"], "fire")
        self.assertEqual(monster.get("vulnerable"), None)
        self.assertEqual(monster["damage_immunities"], "poison")
        self.assertEqual(monster.get("immune"), None)
        self.assertEqual(monster["condition_immunities"], "poisoned")
        self.assertEqual(monster.get("conditionImmune"), None)
        self.assertEqual(monster["senses"], "darkvision 60 ft., passive Perception 10")
        self.assertEqual(monster.get("passive"), None)

    def test_add_bestiary_trait(self):
        monster = {}
        add_bestiary_trait(monster)
        self.assertEqual(
            monster,
            {
                "bestiary": True,
            },
        )

    def test_convert_traits(self):
        monster = {
            "trait": [
                {
                    "name": "Amphibious",
                    "text": "The aboleth can breathe air and water.",
                },
                {
                    "name": "Source",
                    "text": "Source of monster",
                },
            ]
        }
        convert_traits(monster)
        self.assertEqual(
            monster,
            {
                "traits": [
                    {
                        "name": "Amphibious",
                        "desc": "The aboleth can breathe air and water.",
                    },
                ],
                "source": "Source of monster",
            },
        )

    def test_convert_traits_missing_source(self):
        monster = {
            "trait": [
                {
                    "name": "Amphibious",
                    "text": "The aboleth can breathe air and water.",
                },
            ]
        }
        convert_traits(monster)
        self.assertEqual(
            monster,
            {
                "traits": [
                    {
                        "name": "Amphibious",
                        "desc": "The aboleth can breathe air and water.",
                    },
                ],
                "source": "Not Found",
            },
        )

    def test_convert_actions(self):
        monster = {
            "action": [
                {
                    "name": "Multiattack",
                    "text": "The aboleth makes three tentacle attacks.",
                },
            ]
        }
        convert_actions(monster)
        self.assertEqual(
            monster,
            {
                "actions": [
                    {
                        "name": "Multiattack",
                        "desc": "The aboleth makes three tentacle attacks.",
                    },
                ],
            },
        )

    def test_convert_actions_attack(self):
        monster = {
            "action": [
                {
                    "name": "Multiattack",
                    "text": "The aboleth makes three tentacle attacks.",
                    "attack": "Tentacle|9|5d6+6",
                },
            ]
        }
        convert_actions(monster)
        self.assertEqual(
            monster,
            {
                "actions": [
                    {
                        "name": "Multiattack",
                        "desc": "The aboleth makes three tentacle attacks.",
                        "attack_bonus": "9",
                        "damage_dice": "5d6",
                        "damage_bonus": "6",
                    },
                ],
            },
        )

    def test_convert_legendary_actions(self):
        monster = {
            "legendary": [
                {
                    "name": "Detect",
                    "text": "The aboleth makes a Wisdom (Perception) check.",
                },
            ]
        }
        convert_legendary_actions(monster)
        self.assertEqual(
            monster,
            {
                "legendary_actions": [
                    {
                        "name": "Detect",
                        "desc": "The aboleth makes a Wisdom (Perception) check.",
                    },
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
