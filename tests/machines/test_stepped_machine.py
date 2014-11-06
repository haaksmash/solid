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

import pytest

from solid.machines.stepped_machine import SteppedMachine
from solid.states import BaseState, is_entry_state
from solid.transition import to, END


class TestSteppedMachine(object):

    class Machine(SteppedMachine):

        @is_entry_state
        class EntersHere(BaseState):
            def body(self):
                return to(self.parent_machine.ThenGoesHere)

        class ThenGoesHere(BaseState):
            def body(self):
                return to(self.parent_machine.AndThenHere)

        class AndThenHere(BaseState):
            def body(self):
                return to(self.parent_machine.AndFinallyHere)

        class AndFinallyHere(BaseState):
            def body(self):
                return

    @pytest.fixture
    def machine(self):
        return self.Machine()

    def test_start_only_hits_one_state(self, machine):
        machine.start()

        assert len(machine.history) == 1

    def test_stepping_machine(self, machine):
        machine.start()
        assert machine.history[-1].target == machine.ThenGoesHere

        machine.step()
        assert machine.history[-1].target == machine.AndThenHere

        machine.step()
        assert machine.history[-1].target == machine.AndFinallyHere

        machine.step()
        assert machine.history[-1].target == END

    def test_stepping_machine_past_END_is_totally_cool(self, machine):
        machine.start()
        machine.step()
        machine.step()
        machine.step()
        assert machine.history[-1].target == END
        history_length = len(machine.history)

        machine.step()
        assert machine.history[-1].target == END
        assert len(machine.history) == history_length
