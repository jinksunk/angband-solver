from angband_solver.models import Ability


def test_equipment_model(equipment_model):
    assert equipment_model.validate()


def test_ability_score_model(ability_score_model):
    assert ability_score_model.validate()
    assert ability_score_model.get_score(Ability["RPOIS"], 1, 1) == 1
    assert ability_score_model.get_score(Ability["RPOIS"], 1, 2) == 0
    assert ability_score_model.get_score(Ability["SPEED"], 1, 1) == 1
    assert ability_score_model.get_score(Ability["SPEED"], 2, 2) == 2
