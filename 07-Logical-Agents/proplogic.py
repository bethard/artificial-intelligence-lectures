class KnowledgeBaseAgent(object):
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.time = 0
    def take_action(self, percept):
        # convert the percept to knowledge
        percept_sentence = self.percept_to_sentence(percept)
        self.knowledge_base.tell(percept_sentence)
        # select an action based on the knowledge
        action_query = self.make_action_query()
        action = self.knowledge_base.ask(action_query)
        # update the knowledge base with the planned action
        action_sentence = self.action_to_sentence(action)
        self.knowledge_base.tell(action)
        self.time += 1
        # perform the action
        return action


def truth_table_entails(knowledge_base, query):
    query_true = query.is_true_for
    kb_true = knowledge_base.is_true_for
    # check all assignments of knowledge base and query symbols:
    # if the knowledge base is true the query should be true
    symbols = set.union(knowledge_base.symbols, query.symbols)
    return all(
        query_true(assignment) if kb_true(assignment) else True
        for assignment in all_models(symbols))

def all_models(symbols):
    # base case: no symbols, generate an empty assignment
    if not symbols:
        yield {}
    # recursive case: assign to the first symbol and recurse
    else:
        first, rest = symbols[0], symbols[1:]
        for assignment in all_models(rest):
            for value in [True, False]:
                assignment[first] = value
                yield assignment




def forward_chaining_entails(knowledge_base, query):
    # count the symbols in the body of each clause
    counts = {}
    for clause in knowledge_base.get_clauses():
        counts[clause] = len(clause.body)
    # start with known symbols and search for non-inferred
    inferred = set()
    agenda = knowledge_base.get_true_symbols()
    while agenda:
        symbol = agenda.pop()
        if symbol not in inferred:
            inferred.add(symbol)
            # update counts and infer heads when possible
            for clause in knowledge_base.get_clauses():
                if symbol in clause.body:
                    counts[clause] -= 1
                    if counts[clause] == 0:
                        if clause.head == query:
                            return True
                        agenda.append(clause.head)
    return False




def test():
    def list_models(symbols):
        return list(d.copy() for d in all_models(symbols))            
    
    assert list_models('') == [{}]
    assert list_models('a') == [dict(a=True), dict(a=False)]
    assert list_models('ab') == [
        dict(a=True, b=True),
        dict(a=False, b=True),
        dict(a=True, b=False),
        dict(a=False, b=False),
    ]
    assert list_models('abc') == [
        dict(a=True,  b=True,  c=True),
        dict(a=False, b=True,  c=True),
        dict(a=True,  b=False, c=True),
        dict(a=False, b=False, c=True),
        dict(a=True,  b=True,  c=False),
        dict(a=False, b=True,  c=False),
        dict(a=True,  b=False, c=False),
        dict(a=False, b=False, c=False),
    ]
    

test()