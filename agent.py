class Agent:

    def __init__(self, initial_config):
        self.state = initial_config

    def __str__(self):
        return {0: '0', 1: '1', 2: '?'}[self.state]

    def interact(self, agent):
        return three_state_protocol(self, agent)


def three_state_protocol(agent1, agent2):

    def calculate(state1, state2):
        if (state1 == 0) and (state2 == 0 or state2 == 2):
            return state1, 0
        if (state1 == 1) and (state2 == 1 or state2 == 2):
            return state1, 1
        if (state1 == 0 and state2 == 1) or (state1 == 1 and state2 == 0):
            # Observer becomes unsure due to contradiction
            return state1, 2
        if state1 == 2:
            # Observer keeps its belief
            return state1, state2

    _, new_state = calculate(agent1.state, agent2.state)

    result = {
        'agent1': str(agent1),
        'agent2': str(agent2),
        'agent2_': str(new_state),
        'change': (agent2.state != new_state)
    }

    agent2.state = new_state

    return result
