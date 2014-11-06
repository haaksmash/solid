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

from solid.machines import BaseMachine
from solid.states import BaseState, is_entry_state
from solid.states.boomerang_state import BoomerangState
from solid.transition import to, Transition, END


class TestBoomerangStateBehavior(object):
    class RepeatingMachine(BaseMachine):

        class SimpleBoomerang(BoomerangState):
            def body(self):
                return to(None, from_boomerang=True)

        @is_entry_state
        class StartState(BaseState):

            def body(self, from_boomerang=False):

                if not from_boomerang:
                    return to(
                        TestBoomerangStateBehavior.RepeatingMachine.SimpleBoomerang
                    )

                return

    def test_returns_to_previous_state(self):
        machine = self.RepeatingMachine()

        machine.start()

        expected_history = [
            Transition(
                origin=machine.StartState,
                target=machine.SimpleBoomerang,
            ),
            Transition(
                origin=machine.SimpleBoomerang,
                target=machine.StartState,
                from_boomerang=True,
            ),
            Transition(
                origin=machine.StartState,
                target=END,
            ),
        ]

        assert machine.history == expected_history
