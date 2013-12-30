def csp_search(csp, heuristic, assignment=None):
    if assignment is None:
        assignment = {}
    # if assignment is complete, return it
    if len(assignment) == len(csp.variables):
        return assignment
    # select an unassigned variable and order the values
    variable = heuristic.select_variable(csp, assignment)
    values = heuristic.order_values(csp, assignment, var)
    # try assigning each value to the variable
    for value in values:
        assignment[variable] = value
        # for consistent assignments, recursively check if
        # it is possible to assign the remaining variables
        if csp.is_consistent(assignment):
            result = csp_search(csp, heuristic, assignment)
            if result is not None:
                return result
        del assignment[variable]
    # all assignments failed
    return None



def arc_consistency(csp):
    # check all arcs in the CSP
    queue = collections.deque(csp.get_arcs())
    while queue:
        var1, var2 = queue.popleft()
        # if inconsistent values are found, add all neighbors
        if remove_inconsistent_values(csp, var1, var2):
            for var3 in csp.get_neighbors(var1) - set([var2]):
                queue.append(var3, var1)

def remove_inconsistent_values(csp, var1, var2):
    # search all the values of var1's domain
    removed = False
    for value1 in var1.domain:
        # remove the value if it is inconsistent with var2
        if all(not csp.is_consistent({var1:value1, var2:value2})
               for value2 in var2.domain):
            var1.domain.remove(value1)
            removed = True
    # return whether or not any inconsistent values were removed
    return removed




def min_conflicts(csp, max_steps):
    # start with an initial complete assignment
    assignment = {}
    for variable in csp.variables:
        assignment[variable] = random.choice(variable.domain)
    # adjust one variable each time through the loop
    for i in range(max_steps):
        # return the assignment when it is consistent
        if csp.is_consistent(assignment):
            return assignment
        # otherwise, select a random conflicted variable
        var = random.choice(csp.get_conflicts(assignment))
        # assign the variable the value with minimal conflicts
        counts = {}
        for value in var.domain:
            assignment[var] = value
            conflicts = csp.get_conflicts(assignment)
            counts[value] = len(conflicts)
        assignment[var] = min(counts, key=counts.get)
    # all assignments failed
    return None
