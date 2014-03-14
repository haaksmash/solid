

class State(object):

    def __init__(self, name=None):
        # keep track of the transitions associated with this state, for
        # visualization purposes
        self.source_transitions = set()
        self.destination_transitions = set()
        self.name = name

    def __repr__(self):
        if self.name is not None:
            return u"<State: {}>".format(self.name)
        return super(State, self).__repr__()


def states_factory(*args):
    return type(
        "StateCollection",
        (object,),
        {
            arg: State(arg) for arg in args
        },
    )
