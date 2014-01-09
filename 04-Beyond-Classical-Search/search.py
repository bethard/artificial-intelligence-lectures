def hill_climb(problem):
    
    # start at the problem's initial state
    current = Node(problem.initial_state)
    while True:

        # select the neighboring state with the best score
        state_scores = []
        get_successors = problem.get_successors
        for state, score in get_successors(current.state):
            state_scores.append((score, state))
        best_score, best_state = max(state_scores)

        # if no neighbors are better, return the current
        if best_score < current.score:
            return current.state

        # otherwise, move current to the best state
        current = Node(best_state, best_score)

def simulated_annealing(problem, get_temperature):
    current = Node(problem.initial_state)
    for time in itertools.count():
        
        # stop when the temperature reaches zero
        temperature = get_temperature(time)
        if not temperature:
            return current
        
        # select a random neighbor
        get_successors = problem.get_successors
        successors = get_successors(current.state)
        state, score = random.choice(successors)
        
        # always move to the neighbor always if it's
        # better, and sometimes if it's worse
        change = score - current.score
        prob = math.exp(change / temperature)
        if change > 0 or random.random() < prob:
            current = Node(state, score)
            
def local_beam_search(problem, k):
    current = [problem.generate_state() for _ in range(k)]
    while True:
        
        # get all neighbors of the current states
        state_scores = []
        for node in current:
            get_successors = problem.get_successors
            for state, score in get_successors(node.state):
                
                # return the first goal state generated
                if problem.is_goal(state):
                    return state
                state_scores.append((score, state))
        
        # select the k best states to consider next time
        current = []
        for score, state in heapq.nlargest(k, state_scores):
            current.append(Node(state, score))