def tree_search(problem, strategy):
    # start with the initial state
    strategy.add(...problem.initial_state...)
    # search nodes in strategy order
    for node in strategy:
        # return actions if goal is found
        if problem.is_goal(node.state):
            return node.get_actions()
        # otherwise, add nodes for each successor
        items = problem.get_successors(node.state)
        for state, action, ... in items:
            strategy.add(...state...action...)
    # search failed
    return None


def tree_search(problem, strategy):
    strategy.add(Node(problem.initial_state))
    for node in strategy:
        if problem.is_goal(node.state):
            return node.get_actions()
        succs = problem.get_successors(node.state)
        for state, action, cost in succs:
            strategy.add(Node(
                state=state,
                action=action,
                parent=node,
                cost=node.cost + cost,
                depth=node.depth + 1))
    return None

def graph_search(problem, strategy):
    seen = set()
    strategy.add(Node(problem.initial_state))
    for node in strategy:
        if problem.is_goal(node.state):
            return node.get_actions()
        if node not in seen:
            seen.add(node)
            succs = problem.get_successors(node.state)
            for state, action, cost in succs:
                strategy.add(Node(
                    state=state,
                    action=action,
                    parent=node,
                    cost=node.cost + cost,
                    depth=node.depth + 1))
            
