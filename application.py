import argparse
import yaml
import logging

import angband_solver
from angband_solver.models import AbilityType

"""
Read a yaml file describing available equipment options, and return
the survival value for each piece of equipment, as well as the optimal
set of equipment to wear given all options.

Arguments include:

:param eqfile: - The yaml file describing the equipment to load. See
                 templates/equipment.yaml for an example.
"""

'''
Define arguments:

'''

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Optimize equipment')
parser.add_argument('eqfile', metavar="F",
                    help=('A yaml file describing the current equipment ' +
                          'available.'))
parser.add_argument('abfile', metavar="F",
                    help=('A yaml file describing value of each ability'))


def __main__():
    args = parser.parse_args()
    with open(args.eqfile, 'r') as eqstream:
        eq_model = yaml.load(eqstream)
        logging.debug("Loaded {}".format(eq_model))
        assert eq_model.validate()
    with open(args.abfile, 'r') as abstream:
        ab_model = yaml.load(abstream)
        assert ab_model.validate()

    result = angband_solver.optimize(eq_model, ab_model)

    print("Overall Score: {}\nEquipment List:\n".format(result[0]))

    type_dict = dict()
    for eq_item in result[1]:
        if eq_item.type not in type_dict.keys():
            type_dict[eq_item.type] = list()
        type_dict[eq_item.type].append(eq_item.name)

    for category in type_dict.keys():
        print("[{}]: ".format(category))
        for name in type_dict[category]:
            print("\t - {}".format(name))

    # Determine what is covered and what is missing from the equipment set:
    covered = set()
    missing = {x for x in ab_model.abilities.keys()
               if ab_model.abilities[x]['type'] == AbilityType.BINARY}

    missing_list = list(missing)
    for ability in missing_list:
        # Check equipment set to see if any item covers it:
        for eq_item in result[1]:
            if ability in eq_item.abilities.keys():
                missing.remove(ability)
                covered.add(ability)
                break
    print("\nCovered by equipment set: {}".format(covered))
    print("\nMissing from equipment set: {}".format(missing))


if __name__ == "__main__":
    __main__()
