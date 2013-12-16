def minimax_decision(problem, state):
    # select the action with the maximum utility
    value, action = max_value_action(problem, state)
    return action

def max_value_action(problem, state):
    # simply return the known utility for leaf nodes
    if problem.is_terminal(state):
        return problem.get_utility(state), None
    # collect utility values for each available action
    items = []
    for action, state in problem.get_successors(state):
        value, _ = min_value_action(problem, state)
        items.append((value, action))
    # return the action with the maximum utility
    return max(items)

def min_value_action(problem, state):
    # simply return the known utility for leaf nodes
    if problem.is_terminal(state):
        return problem.get_utility(state), None
    # collect utility values for each available action
    items = []
    for action, state in problem.get_successors(state):
        value, _ = max_value_action(problem, state)
        items.append((value, action))
    # return the action with the minimum utility
    return min(items)

def get_value_action(problem, state, min_or_max):
    # simply return the known utility for leaf nodes
    if problem.is_terminal(state):
        return problem.get_utility(state), None
    # if this is min, the next is max and vice versa
    min_or_max2 = min if min_or_max is max else max
    # collect utility values for each available action
    items = []
    for action, state in problem.get_successors(state):
        value, _ = get_value_action(problem, state, min_or_max2)
        items.append((value, action))
    # return the action with the minimum or maximum utility
    return min_or_max(items)

pos_inf, neg_inf = 1e1000, -1e1000

def alpha_beta_search(problem, state):
    # select the action with the maximum utility
    value, action = max_ab(state, neg_inf, pos_inf)
    return action

def max_ab(problem, state, alpha, beta):
    # simply return the known utility for leaf nodes
    if problem.is_terminal(state):
        return problem.get_utility(state), None
    # examine utility values for each available action
    value, action = neg_inf, None
    for action2, state2 in problem.get_successors(state):
        value2, _ = min_ab(problem, state2, alpha, beta)
        # return the new value if higher than the global minimum
        value, action = max([value, action], [value2, action2])
        if value >= beta:
            return value, action
        # otherwise, update the global maximum
        alpha = max(alpha, value)
    # return the action with the maximum utility
    return value, action

def min_ab(problem, state, alpha, beta):
    # simply return the known utility for leaf nodes
    if problem.is_terminal(state):
        return problem.get_utility(state), None
    # examine utility values for each available action
    value, action = pos_inf, None
    for action2, state2 in problem.get_successors(state):
        value2, _ = max_ab(problem, state2, alpha, beta)
        # return the new value if lower than the global maximum
        value, action = min([value, action], [value2, action2])
        if value <= alpha:
            return value, action
        # otherwise, update the global minimum
        beta = min(beta, value)
    # return the action with the maximum utility
    return value, action


def test():
    class Problem(object):
        successors = {
            'A': [('a1', 'B'), ('a2', 'C'), ('a3', 'D')],
            'B': [('b1', 'E'), ('b2', 'F'), ('b3', 'G')],
            'C': [('c1', 'H'), ('c2', 'I'), ('c3', 'J')],
            'D': [('d1', 'K'), ('d2', 'L'), ('d3', 'M')],
        }
        utilities = dict(
            E=3, F=12, G=8, H=2, I=4, J=6, K=14, L=5, M=2,
        )
        def is_terminal(self, state):
            return state not in self.successors
        def get_successors(self, state):
            return self.successors[state]
        def get_utility(self, state):
            return self.utilities[state]

    assert minimax_decision(Problem(), 'A') == 'a1'
    assert min_value_action(Problem(), 'B') == (3, 'b1')
    assert min_value_action(Problem(), 'D') == (2, 'd3')
    
    assert get_value_action(Problem(), 'A', max) == (3, 'a1')
    assert get_value_action(Problem(), 'B', min) == (3, 'b1')
    assert get_value_action(Problem(), 'D', min) == (2, 'd3')

    assert max_ab(Problem(), 'A', neg_inf, pos_inf) == (3, 'a1')
    assert min_ab(Problem(), 'B', neg_inf, pos_inf) == (3, 'b1')
    assert min_ab(Problem(), 'D', neg_inf, pos_inf) == (2, 'd3')

test()