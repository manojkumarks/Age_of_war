from typing import List
from itertools import permutations


class Platoon:
    advantage_map = {
        "Militia": ["Spearmen", "LightCavalry"],
        "Spearmen": ["LightCavalry", "HeavyCavalry"],
        "LightCavalry": ["FootArcher", "CavalryArcher"],
        "HeavyCavalry": ["Militia", "FootArcher", "LightCavalry"],
        "CavalryArcher": ["Spearmen", "HeavyCavalry"],
        "FootArcher": ["Militia", "CavalryArcher"]
    }

    def __init__(self, unit_type: str, count: int):
        self.unit_type = unit_type
        self.count = count

    def has_advantage_over(self, other: 'Platoon') -> bool:
        return other.unit_type in Platoon.advantage_map.get(self.unit_type, [])

    def effective_strength_against(self, opponent: 'Platoon') -> int:
        strength = self.count * 2 if self.has_advantage_over(opponent) else self.count
        return strength

    def __str__(self):
        return f"{self.unit_type}#{self.count}"


class Army:
    def __init__(self, platoons: List[Platoon]):
        self.platoons = platoons

    @staticmethod
    def from_string(data: str) -> 'Army':
        units = []
        for unit in data.strip().split(";"):
            unit_type, count = unit.split("#")
            units.append(Platoon(unit_type.strip(), int(count.strip())))
        return Army(units)

    def get_all_permutations(self) -> List[List[Platoon]]:
        return list(permutations(self.platoons))

    def __len__(self):
        return len(self.platoons)


class Battle:
    def __init__(self, attacker: Platoon, defender: Platoon):
        self.attacker = attacker
        self.defender = defender

    def result(self) -> int:
        atk_strength = self.attacker.effective_strength_against(self.defender)
        def_strength = self.defender.effective_strength_against(self.attacker)

        if atk_strength > def_strength:
            return 1  # Win
        elif atk_strength == def_strength:
            return 0  # Draw
        return -1  # Loss


class War:
    def __init__(self, my_army: Army, enemy_army: Army):
        self.my_army = my_army
        self.enemy_army = enemy_army

    def find_winning_arrangement(self) -> List[Platoon]:
        for permutation in self.my_army.get_all_permutations():
            wins = 0
            for my_unit, enemy_unit in zip(permutation, self.enemy_army.platoons):
                result = Battle(my_unit, enemy_unit).result()
                if result == 1:
                    wins += 1
            if wins >= 3:
                return list(permutation)
        return []


def main():
    print("=== Medieval War Simulation ===\n")

    my_input = input("Enter your platoons (e.g., Spearmen#10;Militia#30;...):\n")
    enemy_input = input("Enter opponent's platoons:\n")

    my_army = Army.from_string(my_input)
    enemy_army = Army.from_string(enemy_input)

    if len(my_army) != len(enemy_army):
        print("Error: Both armies must have the same number of platoons.")
        return

    war = War(my_army, enemy_army)
    arrangement = war.find_winning_arrangement()

    print("\n=== Recommended Battle Formation ===")
    if arrangement:
        print(";".join(str(p) for p in arrangement))
    else:
        print("There is no chance of winning")


if __name__ == "__main__":
    main()
