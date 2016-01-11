class TableDrivenAgent(object):
    def __init__(self, table):
        self.table = table
        self.percepts = []
    def act(self, percept):
        self.percepts.append(percept)
        return self.table[self.percepts]

class ReflexVacuumAgent(object):
    def act(self, percept):
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
    def act(self, percept):
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
    assert agent.act(("A", "Dirty")) == "Suck"
    assert agent.act(("A", "Clean")) == "Right"
    assert agent.act(("B", "Clean")) == "NoOp"
    assert agent.act(("B", "Clean")) == "NoOp"
    assert agent.act(("B", "Clean")) == "NoOp"
    assert agent.act(("B", "Clean")) == "Left"
    assert agent.act(("A", "Clean")) == "NoOp"
    assert agent.act(("A", "Clean")) == "NoOp"
    assert agent.act(("A", "Clean")) == "NoOp"
    assert agent.act(("A", "Clean")) == "Right"
    assert agent.act(("B", "Clean")) == "NoOp"
    assert agent.act(("B", "Clean")) == "NoOp"
    assert agent.act(("B", "Clean")) == "NoOp"
    assert agent.act(("B", "Dirty")) == "Suck"
    assert agent.act(("B", "Clean")) == "Left"

test()
