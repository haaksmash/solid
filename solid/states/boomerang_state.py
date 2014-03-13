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

from solid.states.base_state import BaseState
from solid.transition import Transition


class BoomerangState(BaseState):

    def on_exit(self, expected_transition):
        """Always return to the previous state."""
        transition = super(BoomerangState, self).on_exit(expected_transition)

        return Transition(
          origin=self.__class__,
          target=transition.origin,
          **transition.kwargs
        )