from itertools import permutations

# Define unit class advantage mapping
advantage_map = {
    "Militia": ["Spearmen", "LightCavalry"],
    "Spearmen": ["LightCavalry", "HeavyCavalry"],
    "LightCavalry": ["FootArcher", "CavalryArcher"],
    "HeavyCavalry": ["Militia", "FootArcher", "LightCavalry"],
    "CavalryArcher": ["Spearmen", "HeavyCavalry"],
    "FootArcher": ["Militia", "CavalryArcher"]
}

def parse_input(line):
    platoons = []
    for item in line.strip().split(";"):
        unit, count = item.split("#")
        platoons.append((unit.strip(), int(count)))
    return platoons

def effective_strength(attacker, defender):
    attacker_class, attacker_count = attacker
    defender_class, defender_count = defender

    if defender_class in advantage_map.get(attacker_class, []):
        effective_attacker_count = attacker_count * 2
    else:
        effective_attacker_count = attacker_count

    if attacker_class in advantage_map.get(defender_class, []):
        effective_defender_count = defender_count * 2
    else:
        effective_defender_count = defender_count

    if effective_attacker_count > effective_defender_count:
        return 1  # Win
    elif effective_attacker_count == effective_defender_count:
        return 0  # Draw
    else:
        return -1  # Lose

def find_best_arrangement(my_platoons, enemy_platoons):
    for perm in permutations(my_platoons):
        results = [effective_strength(my, en) for my, en in zip(perm, enemy_platoons)]
        wins = sum(1 for r in results if r == 1)
        if wins >= 3:
            return perm
    return None

# Sample input
my_input = "Spearmen#10;Militia#30;FootArcher#20;LightCavalry#1000;HeavyCavalry#120"
enemy_input = "Militia#10;Spearmen#10;FootArcher#1000;LightCavalry#120;CavalryArcher#100"

my_platoons = parse_input(my_input)
enemy_platoons = parse_input(enemy_input)

best_arrangement = find_best_arrangement(my_platoons, enemy_platoons)

if best_arrangement:
    print(";".join(f"{unit}#{count}" for unit, count in best_arrangement))
else:
    print("There is no chance of winning")
