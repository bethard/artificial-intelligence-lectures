def forward_chaining(knowledge_base, query):
    # keep adding to the KB until no new sentences are generated
    new = True
    while sentences:
        new = set()
        for sentence in knowledge_base:
            # find something that unifies with the sentence body
            n = len(sentence.body)
            for subset in all_subsets(knowledge_base, n):
                assignment = unify(subset, sentence.body)
                if assignment is not None:
                    # conclude the sentence head
                    head = assignment.substitute(sentence.head)
                    if head not in knowledge_base + new:
                        new.add(head)
                        # return if the query is concluded
                        result = unify(head, query)
                        if result is not None:
                            return result
        knowledge_base.update(new)




def backward_chaining(knowledge_base, goals, assignment):
    # if all goals have been resolved, generate the assignment
    if not goals:
        yield assignment
    # otherwise, check the first goal and recurse
    else:
        term = assignment.substitute(goals[0])
        for sentence in knowledge_base:
            # try to unify the sentence with the first goal
            new_assignment = unify(sentence.head, term)
            if new_assignment is None:
                continue
            # add the sentence's premise to the remaining goals
            new_goals = list(sentence.body)
            new_goals.extend(goals[1:])
            new_assignment = new_assignment.compose(assignment)
            # recursively search for the remaining goals
            args = knowledge_base, new_goals, new_assignment
            for result in backward_chaining(*args):
                yield result