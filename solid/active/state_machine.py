from solid.exception import IllegalTransitionError
from solid.active.transition import Transition


class _MachineMeta(type):

    def __new__(cls, name, bases, attrs):
        transitions = set()
        for attr in attrs.itervalues():
            if type(attr) is type and issubclass(attr, Transition):
                transitions.add(attr)

        if '_transitions' in attrs:
            attrs['_transitions'].update(transitions)
        else:
            attrs['_transitions'] = transitions

        return super(_MachineMeta, cls).__new__(cls, name, bases, attrs)


class Machine(object):
    __metaclass__ = _MachineMeta

    def __init__(self):

        self._current_state = None
        self._history = []

        self._transition_set = set()
        for value in self._transitions:
            transition = value(value.FROM, value.TO, parent_machine=self)

            self._transition_set.add(transition)

    def _find_transition(self, to_state):
        def filter_func(desired, considered):
            if desired == considered:
                return True
            try:
                if desired in considered:
                    return True
            except TypeError:
                pass

            return False

        transitions = filter(
            lambda trans: bool(
                filter_func(to_state, trans.to_state) and
                filter_func(self.current_state, trans.from_state)
            ),
            self._transition_set,
        )
        if not transitions:
            raise IllegalTransitionError(
                "Cannot find transition: {} -> {}".format(
                    self.current_state,
                    to_state,
                ),
            )
        elif len(transitions) > 1:
            raise IllegalTransitionError(
                "Multiple transitions found: from {} -> {}".format(
                    self.current_state,
                    to_state,
                ),
            )

        [transition] = transitions
        return transition

    def transition_to(self, to_state, *args, **kwargs):
        transition = self._find_transition(to_state)

        transition.pre_run(*args, **kwargs)
        transition.run(*args, **kwargs)
        # transition has completed, update our current state...
        self._current_state = to_state
        # and inform history.
        self._history.append(transition)

        # finally, do any signalling
        transition.post_run(*args, **kwargs)

    @property
    def current_state(self):
        return self._current_state

    @property
    def is_started(self):
        return self.current_state is not None

    @property
    def history(self):
        return self._history
