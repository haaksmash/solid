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
from solid.machines import BaseMachine
from solid.states import BaseState, is_entry_state
from solid.transition import to, Transition, END


class TestTransitionTracking(object):
    class SimpleMachine(BaseMachine):

        @is_entry_state
        class SimpleState(BaseState):
            def body(self):
                return to(TestTransitionTracking.SimpleMachine.SimplerState)

        class SimplerState(BaseState):
            def body(self):
                pass

    def test_transitions_are_tracked(self):
        machine = self.SimpleMachine()
        machine.start()

        expected_history = [
            Transition(machine.SimpleState, machine.SimplerState),
            Transition(machine.SimplerState, END),
        ]

        assert machine.history == expected_history