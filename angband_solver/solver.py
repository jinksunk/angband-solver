import logging
logger = logging.getLogger(__name__)

"""
Load the relevant data files, and return an optimized equipment report.
"""


def optimize(eq_model, ability_score_model):
    """
    :param eqfile: An equipment description file to optimize.
    """

    # Categorize the available equipment according to type.
    # For each category:
    #   1. If there is only one option in the category, add it to the result.
    #   2. If there is more than one, add it to the optimization list.

    equipment_set = list()
    best_score = 0

    categories = dict()
    for eq_item in eq_model.equipment_list:
        if eq_item.type not in categories.keys():
            categories[eq_item.type] = list()
        categories[eq_item.type].append(eq_item)

    categories_to_remove = list()
    for category in categories.keys():
        if len(categories[category]) <= category.max_number:
            for i in range(0, len(categories[category])):
                equipment_set.append(categories[category][i])
            categories_to_remove.append(category)
    for goner in categories_to_remove:
        categories.pop(goner)

    # If we've placed all the equipment, just return...
    if len(categories.keys()) == 0:
        return (_evaluate(equipment_set, ability_score_model), equipment_set)

    # For remaining categories, optimize:
    (best_score, best_set) =\
        _optimize_dfs(categories, equipment_set, ability_score_model)

    return (best_score, best_set)


def _optimize_dfs(available_categories, equipment_set, ability_score_model):
    """
    Use a depth-first search to exhaustively select the best possible
    combination.

    :param available_categories: - A dictionary with equipment category as
                                   the key, and a list of equipment in that
                                   category as the value.
    :param equipment_set: - The set of equipment chosen so far.
    :param ability_score_model: - The scoring model to use
    :return: A tuple: (<max_score>, equipment_set), giving the maximum
             possible score that can be achieved from the provided
             available and selected equipment.
    """

    # If there are no more categories, return the score and the equipment
    # set.
    if len(available_categories) == 0:
        return (_evaluate(equipment_set, ability_score_model), equipment_set)

    # Otherwise, choose our category and iterate over each set of equipment:
    new_available_categories = dict(available_categories)
    (category, category_eq) = new_available_categories.popitem()
    to_try = _generate_eq_sets(category, category_eq)

    # Iterate over equipment choices from our category to see what yields the
    # best result:
    best_score = 0
    best_set = None

    logging.debug("Found {} candidate sets for category {}"
                  .format(len(to_try), category))
    for candidate_set in to_try:
        # pick the best one:
        proposed_set = list(equipment_set + [x for x in candidate_set])
        logging.debug("Making recursive call for category {}".format(category))
        (score, _set) = _optimize_dfs(new_available_categories, proposed_set,
                                      ability_score_model)
        logging.debug("Best score for set including {} {}: {}"
                      .format(category, [x.name for x in candidate_set],
                              score))
        if score >= best_score:
            best_score = score
            best_set = _set

    return (best_score, best_set)


def _generate_eq_sets(category, category_eq):
    """
    Return a list of all sets of equipment to try for this category.
    For rings it will be sets of 2, for everything else it will be
    singleton sets.
    """
    set_size = category.max_number

    to_return = list()  # Return a list of sets
    to_return.append(set())

    for i in range(0, set_size):
        candidate_return = [x for x in to_return]
        for partial_set in candidate_return:
            to_return.remove(partial_set)
            for new_item in category_eq:
                new_set = set(partial_set)
                new_set.add(new_item)
                if len(new_set) == len(partial_set):
                    continue
                else:
                    if new_set not in to_return:
                        to_return.append(new_set)

    return to_return


def _optimize(categories, equipment_set, ability_score_model):
    """
    Recursively optimize categories, until there is only one left:
    """

    if len(categories) == 0:
        return (0, [])

    cat_keys = list(categories.keys())

    our_category = categories.pop(cat_keys[0])

    if len(categories.keys()) >= 1:
        (best_score, equipment_set) = _optimize(categories, equipment_set,
                                                ability_score_model)

    best_set = list(equipment_set)
    for i in range(0, cat_keys[0].max_number):
        best_score = 0
        best_item = None
        for eq_item in our_category:
            # pick the best one:
            proposed_set = list(best_set)
            proposed_set.append(eq_item)
            score = _evaluate(proposed_set, ability_score_model)
            if score > best_score:
                best_score = score
                best_item = eq_item
        best_set.append(best_item)
        # print("Adding {} yielded a score of {}"
        #       .format(best_item, best_score))
        our_category.remove(best_item)

    return (best_score, best_set)


def _evaluate(equipment_list, ability_score_model):
    """
    Given a list of chosen equipment, evaluate it:
    """
    ability_track = {}
    score = 0
    for eq_item in equipment_list:
        for ability in eq_item.abilities:
            if ability not in ability_track.keys():
                ability_track[ability] = 0
            ability_track[ability] += eq_item.abilities[ability]
            score += ability_score_model.get_score(
                    ability,
                    eq_item.abilities[ability],
                    ability_track[ability])
    return score
