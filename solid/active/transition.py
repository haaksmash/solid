from solid.active.state import State


class Transition(object):

    FROM = None
    TO = None

    def __init__(self, from_state, to_state, parent_machine=None):
        self.from_state = from_state
        self.to_state = to_state
        self._parent_machine = parent_machine

        # support State's attempt to enable visualization
        if isinstance(from_state, State):
            from_state.source_transitions.add(self)

        if isinstance(to_state, State):
            to_state.destination_transitions.add(self)

    def pre_run(self, *args, **kwargs):
        """any guards for the transition go here"""
        pass

    def run(self, *args, **kwargs):
        """Do what needs to be done to get from from_state to to_state"""
        raise NotImplemented()

    def post_run(self, *args, **kwargs):
        pass

    def __repr__(self):
        return u"<Transition: {} -> {}>".format(self.from_state, self.to_state)
