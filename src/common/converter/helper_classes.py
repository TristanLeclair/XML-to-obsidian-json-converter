from enum import Enum


class Size(Enum):
    L = "Large"
    M = "Medium"
    S = "Small"
    G = "Gargantuan"
    T = "Tiny"


class Stat(Enum):
    Con = "constitution"
    Int = "intelligence"
    Str = "strength"
    Dex = "dexterity"
    Wis = "wisdom"
    Cha = "charisma"
