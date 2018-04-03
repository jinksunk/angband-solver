import math
from angband_solver.solver import _evaluate, _optimize, optimize,\
                                  _generate_eq_sets, _optimize_dfs
from angband_solver.models import EquipmentType


def test_generate_eq_sets(equipment_model):
    categories_to_test = [EquipmentType.RING, EquipmentType.MELEE]

    for category in categories_to_test:
        category_eq = [x for x in equipment_model.equipment_list
                       if x.type == category]
        '''
        category_eq = [1, 2, 3, 4, 5]
        '''
        result_set = _generate_eq_sets(category, category_eq)
        print("Got result: {}".format(result_set))
        assert len(result_set) == math.factorial(len(category_eq)) /\
            (math.factorial(category.max_number) *
             math.factorial(len(category_eq) - category.max_number))


def test_optimize_dfs(equipment_model, ability_score_model):
    (score, eset) = _optimize_dfs({}, [], ability_score_model)
    assert score == 0
    assert len(eset) == 0

    (score, eset) = _optimize_dfs(
            {EquipmentType.RING: [x for x in equipment_model.equipment_list]},
            [],
            ability_score_model)
    assert score == 14
    assert len(eset) == 2


def test_optimize_helper(equipment_model, ability_score_model):
    (score, eset) = _optimize({}, [], ability_score_model)
    assert score == 0
    assert len(eset) == 0

    (score, eset) = _optimize(
            {EquipmentType.RING: [x for x in equipment_model.equipment_list]},
            [],
            ability_score_model)
    assert score == 14
    assert len(eset) == 2


def test_evaluate(equipment_model, ability_score_model):
    eq_list = equipment_model.equipment_list
    assert _evaluate([eq_list[0]], ability_score_model) == 8


def test_optimize(equipment_model, ability_score_model):
    (best_score, best_set) = optimize(equipment_model, ability_score_model)
    assert best_score == 21.25
    assert len(best_set) == 4
