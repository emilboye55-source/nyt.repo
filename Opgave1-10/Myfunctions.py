def one_shot(current_state, previous_state):
    return current_state and not previous_state

def falling_edge(current_state, previous_state):
    return not current_state and previous_state