import pytest
import yaml


@pytest.fixture
def equipment_model():

    eq_test_yaml = '''
--- !!python/object:angband_solver.models.EquipmentModel
equipment_list:
  - name: Ring 1
    type: RING
    abilities:
      RPOIS: 1
      PFEAR: 1
      SPEED: 6
  - name: Ring 2
    type: RING
    abilities:
      RPOIS: 1
      PFEAR: 1
      SPEED: 5
  - name: Ring 3
    type: RING
    abilities:
      RPOIS: 1
      PFEAR: 1
      SPEED: 4
  - name: Trident of Wrath
    type: MELEE
    abilities:
      RPOIS: 1
      PFEAR: 1
      SPEED: 6
  - name: Light Crossbow of the Haradrim
    type: SHOOTER
    abilities:
      MIGHT: 3
'''
    to_return = yaml.load(eq_test_yaml)
    to_return.validate()
    return to_return


@pytest.fixture
def ability_score_model():
    ab_test_yaml = '''
--- !!python/object:angband_solver.models.AbilityScoreModel
abilities:
  RPOIS:
    type: BINARY
    value: 1
  PFEAR:
    type: BINARY
    value: 1
  SPEED:
    type: INCREMENTAL
    value: 1
    multiplier: 1
  MIGHT:
    type: INCREMENTAL
    value: 0.5
    multiplier: 0.75
'''
    to_return = yaml.load(ab_test_yaml)
    to_return.validate()
    return to_return
