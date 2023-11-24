from src.common.converter.helper_classes import Size, Stat


# Only call function if key is present in item
def verify_has_key(key):
    def decorator_verify_has_key(func):
        def wrapper_verify_has_key(monster):
            if key in monster:
                return func(monster)

        return wrapper_verify_has_key

    return decorator_verify_has_key


# Only call function if all keys are present in item
def verify_has_keys(keys):
    def decorator_verify_has_keys(func):
        def wrapper_verify_has_keys(monster):
            if isinstance(keys, list):
                if len(keys) == 0:
                    return func(monster)
                else:
                    if all(item in monster for item in keys):
                        return func(monster)

        return wrapper_verify_has_keys

    return decorator_verify_has_keys


def convert_monster(monster):
    fix_hp(monster)
    convert_size(monster)
    convert_stats(monster)
    convert_saves(monster)
    convert_resistances(monster)
    add_bestiary_trait(monster)
    convert_traits(monster)
    convert_actions(monster)
    convert_legendary_actions(monster)
    convert_spells(monster)
    convert_slots(monster)
    convert_environment(monster)


def get_monster_with_name(name, monsters, copy=True):
    """
    Get monster from compendium with name
    """
    monster = [monster for monster in monsters if monster["name"] == name][0]
    if copy:
        monster = monster.copy()
    return monster


@verify_has_key(key="hp")
def fix_hp(monster):
    """
    Split monster hp into hp and hit_dice
    """
    current_hp = monster["hp"]
    if current_hp is None:
        monster["hp"] = ""
        monster["hit_dice"] = ""
        return

    hp_and_hit_dice = monster["hp"].split(" ")
    monster["hp"] = hp_and_hit_dice[0]
    monster["hit_dice"] = (
        " ".join(hp_and_hit_dice[1:])
        .replace("(", "")
        .replace(")", "")
        .replace("+", " + ")
        .lstrip()
    )


@verify_has_key(key="size")
def convert_size(monster):
    """
    Convert monster size into correct format
    If size not found, default to Medium
    """
    try:
        monster["size"] = Size[monster["size"]].value
    except KeyError:
        monster["size"] = "Medium"


@verify_has_keys(keys=["str", "dex", "con", "int", "wis", "cha"])
def convert_stats(monster):
    monster["stats"] = [
        get_final_stat(monster["str"]),
        get_final_stat(monster["dex"]),
        get_final_stat(monster["con"]),
        get_final_stat(monster["int"]),
        get_final_stat(monster["wis"]),
        get_final_stat(monster["cha"]),
    ]
    _ = (
        monster.pop("str"),
        monster.pop("dex"),
        monster.pop("con"),
        monster.pop("int"),
        monster.pop("wis"),
        monster.pop("cha"),
    )


def get_final_stat(stat):
    return stat + " (" + get_modifier(stat) + ")"


def get_modifier(stat):
    stat = int(stat)
    val = (stat - 10) // 2
    if val > 0:
        return "+" + str(val)
    elif val < 0:
        return "-" + str(abs(val))
    else:
        return "0"


@verify_has_key(key="save")
def convert_saves(monster):
    if monster["save"] is None:
        monster["saves"] = []
        monster.pop("save")
        return

    saves = monster["save"].split(",")
    new_saves = []
    for save in saves:
        save = save.lstrip()
        try:
            stat, value = save.split(" ")
        except ValueError:
            print(monster)
            raise ValueError
        try:
            value = int(value.replace("+", ""))
        except ValueError:
            print(monster)
            raise ValueError
        try:
            stat = Stat[stat.capitalize()].value
        except KeyError:
            print(monster)
            raise ValueError
        print(stat, value)
        new_saves.append({stat: value})
    monster["saves"] = new_saves
    monster.pop("save")


@verify_has_key(key="skill")
def convert_skillsaves(monster):
    if monster["skill"] is None:
        monster["skillsaves"] = []
        monster.pop("skill")
        return

    skillsaves = monster["skill"].split(",")
    new_skillsaves = []
    for save in skillsaves:
        save = save.lstrip()
        stat, value = save.split(" ")
        value = int(value.replace("+", ""))
        stat = stat.lower()
        print(stat, value)
        new_skillsaves.append({stat: value})
    monster["skillsaves"] = new_skillsaves
    monster.pop("skill")


def convert_resistances(monster):
    rename_damage_resistances(monster)
    rename_damage_vulnerabilities(monster)
    rename_damage_immunities(monster)
    rename_condition_immunities(monster)


def rename_damage_resistances(monster):
    rename_key(monster, "resist", "damage_resistances")


def rename_damage_vulnerabilities(monster):
    rename_key(monster, "vulnerable", "damage_vulnerabilities")


def rename_damage_immunities(monster):
    rename_key(monster, "immune", "damage_immunities")


def rename_condition_immunities(monster):
    rename_key(monster, "conditionImmune", "condition_immunities")


def rename_key(monster, old_key, new_key):
    if old_key in monster:
        monster[new_key] = monster.pop(old_key) or ""


@verify_has_key(key="senses")
def convert_senses(monster):
    monster["senses"] += ", passive Perception " + (monster.pop("passive") or "")


def add_bestiary_trait(monster):
    monster["bestiary"] = True


@verify_has_key(key="trait")
def convert_traits(monster):
    source_trait = None
    if isinstance(monster["trait"], list):
        for trait in monster["trait"]:
            wasSource = convert_trait(trait)
            if wasSource:
                source_trait = trait
    elif isinstance(monster["trait"], dict):
        source_trait = monster["trait"]
        convert_trait(monster["trait"])

    if source_trait:
        text = source_trait["text"]
        if isinstance(text, list):
            text = [item.split(" p.")[0] for item in text]
            books = text
        else:
            books = text.split(" p.")[0]
        monster["source"] = books
    else:
        monster["source"] = "Not Found"

    monster["traits"] = monster.pop("trait")


def convert_trait(trait) -> bool:
    source_trait = False
    if "Source" in trait["name"]:
        source_trait = trait
    elif trait.get("text") is not None:
        trait["desc"] = trait.pop("text")
    return source_trait


@verify_has_key(key="action")
def convert_actions(monster):
    monster["actions"] = monster.pop("action")

    actions = monster["actions"]
    if isinstance(actions, list):
        for action in monster["actions"]:
            convert_action(action)
    elif isinstance(actions, dict):
        convert_action(actions)


def convert_action(action):
    text = action.get("text")
    if text and action.get("desc") is None:
        if isinstance(text, list):
            # remove None values
            text = [item for item in text if item is not None and item != ""]
            text = "\n".join(text)
            action["text"] = text
        action["desc"] = action.pop("text")

    if action.get("attack") is not None:
        # Unfortunatly, Obsidian does not support multiple attacks per action
        # aka, melee and ranged attacks with the same weapon
        attack = action.pop("attack")

        if isinstance(attack, list):
            attack = attack[0]

        if "Magic Missile" in attack:
            _, damage = attack.split("|")
        if "|" in attack:
            if "Magic Missile" in attack:
                _, damage = attack.split("|")
                attack_bonus = 0
            else:
                try:
                    _, attack_bonus, damage = attack.split("|")
                except ValueError:
                    print(action)
                    raise ValueError
            if "+" in damage:
                damages = damage.split("+")
            elif "-" in damage:
                damages = damage.split("-")
            else:
                damages = [damage]
            damage_dice_list = [
                damage_instance for damage_instance in damages if "d" in damage_instance
            ]
            damage_bonus_list = [
                damage_instance
                for damage_instance in damages
                if "d" not in damage_instance
            ]
            damage_dice = "".join(damage_dice_list)
            damage_bonus = damage_bonus_list[0] if len(damage_bonus_list) > 0 else None
            action["attack_bonus"] = attack_bonus if attack_bonus else 0
            action["damage_dice"] = damage_dice
            if damage_bonus:
                action["damage_bonus"] = damage_bonus
        else:
            action["attack_bonus"] = 0


@verify_has_key(key="legendary")
def convert_legendary_actions(monster):
    monster["legendary_actions"] = monster.pop("legendary")

    for legendary in monster["legendary_actions"]:
        text = legendary.get("text")
        if text and legendary.get("desc") is None:
            if isinstance(text, list):
                text = [item if item is not None else "" for item in text]
                text = "\n".join(text)
                legendary["text"] = text
            legendary["desc"] = legendary.pop("text")


@verify_has_key(key="spells")
def convert_spells(monster):
    monster.pop("spells")


@verify_has_key(key="slots")
def convert_slots(monster):
    monster.pop("slots")


@verify_has_key(key="environment")
def convert_environment(monster):
    monster.pop("environment")
