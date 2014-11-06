"""
Copyright (C) 2014 Haak Saxberg

This file is part of Solid, a state machine package for Python.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
from solid.active.state import State


class Transition(object):

    FROM = None
    TO = None

    _wants_after_signal = set()
    _wants_before_signal = set()

    def __init__(self, from_state, to_state, parent_machine=None):
        self.from_state = from_state
        self.to_state = to_state
        self._parent_machine = parent_machine

        # support State's attempt to enable visualization
        if isinstance(from_state, State):
            from_state.source_transitions.add(self)

        if isinstance(to_state, State):
            to_state.destination_transitions.add(self)

    def signal_before_begin(self, *args, **kwargs):
        """any guards for the transition go here"""
        pass

    def run(self, *args, **kwargs):
        """Do what needs to be done to get from from_state to to_state"""
        raise NotImplemented()

    def signal_after_complete(self, *args, **kwargs):
        for fn in self._wants_after_signal:
            fn(
                machine=self.__parent_machine,
                transition=self.__class__,
            )

    def __repr__(self):
        return u"<Transition: {} -> {}>".format(self.from_state, self.to_state)

    @classmethod
    def register_callback(cls, callback_fn, after=True, before=False):
        """callback hooks should only expect the following arguments:
            transition - the transition class
            machine - the machine applying the transition
        """
        if after:
            cls._wants_after_signal.add(callback_fn)
        if before:
            cls._wants_before_signal.add(callback_fn)

