from enum import Enum


"""
This module contains the model classes used to represent aspects of the
problem.
"""


class EquipmentType(Enum):
    MELEE = ("melee", 1)
    SHOOTER = ("shooter", 1)
    RING = ("ring", 2)
    AMULET = ("amulet", 1)
    SHIELD = ("shield", 1)
    BODY = ("body", 1)
    SELF = ("self", 1)
    HANDS = ("hands", 1)
    FEET = ("feet", 1)
    CLOAK = ("cloak", 1)
    HEAD = ("head", 1)
    LIGHT = ("light", 1)

    def __init__(self, name, max_number):
        self.max_number = max_number


class AbilityType(Enum):
    BINARY = 1
    INCREMENTAL = 2


class Ability(Enum):
    RACID = 1
    RELEC = 2
    RFIRE = 3
    RCOLD = 4
    RPOIS = 5
    RLITE = 6
    RDARK = 7
    SOUND = 8
    SHARD = 9
    NEXUS = 10
    NETHR = 11
    CHAOS = 12
    DISEN = 13
    PFEAR = 14
    PBLND = 15
    PCONF = 16
    PSTUN = 17
    HLIFE = 18
    REGEN = 19
    ESP = 20
    INVIS = 21
    FRACT = 22
    FEATH = 23
    S_DIG = 24
    IMPHP = 25
    FEAR = 26
    AGGRV = 27
    STEA_ = 28
    SEAR_ = 29
    INFRA = 30
    TUNN_ = 31
    SPEED = 32
    BLOWS = 33
    SHOTS = 34
    MIGHT = 35
    LIGHT = 36
    SSTR = 37
    SDEX = 38
    SINT = 39
    SWIS = 40
    SCON = 41
    PSTR = 42
    PDEX = 43
    PINT = 44
    PWIS = 45
    PCON = 46


class AbilityScoreModel(object):
    """
    Given an ability, and a count or value for the ability, return a utility
    score for it.

    This class is initialized by a yaml file, for the form:
    abilities:
      <ability1>:
        type: <BINARY|INCREMENTAL>
        value: <value>
        multiplier: <floating point number from 0 to 1>
      <ability2>:
        ...
    """

    def validate(self):
        """
        Ensure that the loaded data is valid.
        """
        failed_elements = list()

        ability_list = list(self.abilities.keys())
        for ability in ability_list:
            try:
                if not isinstance(self.abilities[ability]['type'],
                                  AbilityType):
                    type_enum =\
                        AbilityType[self.abilities[ability]['type']]  # noqa F841
                    self.abilities[ability]['type'] = type_enum
            except KeyError:
                print("Could not find key {} in ability type enum."
                      .format(self.abilities[ability]['type']))
                failed_elements.append(ability)
                break

            try:
                if not isinstance(ability, Ability):
                    ability_enum = Ability[ability]  # noqa F841
                    self.abilities[ability_enum] = self.abilities[ability]
                    self.abilities.pop(ability)
            except KeyError:
                print("Could not find key {} in ability enum."
                      .format(ability))
                failed_elements.append(ability)
                break

        if len(failed_elements) == 0:
            return True
        else:
            for felement in failed_elements:
                print("Element {} failed validation."
                      .format(felement))
            return False

    def get_score(self, ability, value, ability_count):
        if self.abilities[ability]["type"] == AbilityType.BINARY:
            if ability_count == 1:
                return self.abilities[ability]["value"]
            else:
                return 0
        elif self.abilities[ability]["type"] == AbilityType.INCREMENTAL:
            if 'max_effective' not in self.abilities[ability].keys() or \
                    ability_count <= self.abilities[ability]["max_effective"]:
                return value * self.abilities[ability]["multiplier"]
            else:
                effective_count = self.abilities[ability]["max_effective"]\
                        - (ability_count - value)
                return max(0, effective_count)
        else:
            print("Unknown ability type: {}"
                  .format(self.abilities[ability]["type"]))


class EquipmentModel(object):
    """
    Each piece of equipment has a name, a type, and a set of abilities.
    On creation, this object will have a member called equipment_list, a
    list of dictionaries of the form:
    { 'name': <name>,
      'type': <equipment_type>,
      'abilities: { <ability1>: <value>, ... } }
    """

    class EquipmentPiece(object):
        """
        A hashable representation of equipment.
        """
        def __init__(self, eq_dict):
            if not isinstance(eq_dict['type'], EquipmentType):
                eq_dict['type'] = EquipmentType[eq_dict['type']]
            for ability in eq_dict['abilities']:
                if not isinstance(ability, Ability):
                    value = eq_dict['abilities'].pop(ability)
                    eq_dict['abilities'][Ability[ability]] = value

            self.type = eq_dict['type']
            self.abilities = eq_dict['abilities']
            self.name = eq_dict['name']

    def validate(self):
        """
        Ensure that each equipment component is loaded correctly.
        """
        new_equipment_list = list()
        return_value = True

        for eq_item in self.equipment_list:
            # Check to make sure that each 'type' is an actual enum value
            try:
                new_equipment_list.append(self.EquipmentPiece(eq_item))
            except KeyError:
                print("Problem instantiating equipment item {}"
                      .format(eq_item))
                return_value = False
                continue
        self.equipment_list = new_equipment_list
        return return_value
