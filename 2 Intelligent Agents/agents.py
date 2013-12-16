class TableDrivenAgent(object):
    def __init__(self, table):
        self.table = table
        self.percepts = []
    def take_action(self, percept):
        self.percepts.append(percept)
        return self.table[self.percepts]

class ReflexVacuumAgent(object):
    def take_action(self, percept):
        location, status = percept
        if status == "Dirty":
            return "Suck"
        elif location == "A":
            return "Right"
        elif location == "B":
            return "Left"


class StatefulReflexVacuumAgent(object):
    def __init__(self):
        self.time_at_location = 3
        self.directions = dict(A="Right", B="Left")
    def take_action(self, percept):
        self.time_at_location += 1
        location, status = percept
        if status == "Dirty":
            return "Suck"
        elif self.time_at_location > 3:
            self.time_at_location = 0
            return self.directions[location]
        else:
            return "NoOp"

def test():
    agent = StatefulReflexVacuumAgent()
    assert agent.take_action(("A", "Dirty")) == "Suck"
    assert agent.take_action(("A", "Clean")) == "Right"
    assert agent.take_action(("B", "Clean")) == "NoOp"
    assert agent.take_action(("B", "Clean")) == "NoOp"
    assert agent.take_action(("B", "Clean")) == "NoOp"
    assert agent.take_action(("B", "Clean")) == "Left"
    assert agent.take_action(("A", "Clean")) == "NoOp"
    assert agent.take_action(("A", "Clean")) == "NoOp"
    assert agent.take_action(("A", "Clean")) == "NoOp"
    assert agent.take_action(("A", "Clean")) == "Right"
    assert agent.take_action(("B", "Clean")) == "NoOp"
    assert agent.take_action(("B", "Clean")) == "NoOp"
    assert agent.take_action(("B", "Clean")) == "NoOp"
    assert agent.take_action(("B", "Dirty")) == "Suck"
    assert agent.take_action(("B", "Clean")) == "Left"

test()