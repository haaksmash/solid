"""
Copyright (C) 2014 Haak Saxberg

This file is part of Solid, a state machine package for Python.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import functools

from solid.exception import IllegalTransitionError
from solid.states.base_state import BaseState
from solid.transition import START


class ForbiddenTransitionError(IllegalTransitionError): pass


class GatedState(BaseState):
    """ Raises an IllegalTransitionError if this state is being entered from an unregistered state."""

    @classmethod
    def can_receive(cls, state_class):
        """class decorator for adding states to the REGISTERED_STATES set"""
        if hasattr(cls, 'REGISTERED_STATES'):
            cls.REGISTERED_STATES.add(state_class)
        else:
            cls.REGISTERED_STATES = set([state_class])
        return state_class

    def run(self, previous_transition):
        if previous_transition.origin is not START:
            if not hasattr(self, 'REGISTERED_STATES') or previous_transition.origin not in self.REGISTERED_STATES:
                import ipdb;ipdb.set_trace() # FIXME: breakpoint!
                raise ForbiddenTransitionError(
                    "{} not allowed to transition to {}".format(
                        previous_transition.origin, self.__class__
                    )
                )

        return super(GatedState, self).run(previous_transition)