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
import mock
import pytest

from solid.states import BaseState
from solid.transition import END
from solid.util import ReadOnlyStateWrapper

class BadNewState(BaseState):
    pass

class GoodState(BaseState):

    def body(stuff):
        pass

def test_must_implement_body():
    bad_state = BadNewState(mock.Mock())
    with pytest.raises(NotImplementedError):
        bad_state.run(mock.MagicMock())

def test_run_calls_api_methods_in_order():
    """on_entry -> do_body -> on_exit"""
    state = GoodState(mock.Mock())
    mock_transition = mock.Mock(call_order=0)
    with mock.patch.multiple(
        state,
        on_exit=mock.DEFAULT,
        on_entry=mock.DEFAULT,
        do_body=mock.DEFAULT,
    ) as mocks:

        def add_to_call_order(t):
            new_t = mock.Mock(call_order=t.call_order + 1)
            return new_t

        for value in mocks.values():
            value.side_effect = add_to_call_order

        state.run(mock_transition)

        mocks['on_entry'].assert_called_once_with(
            ReadOnlyStateWrapper(
                mock_transition,
            ),
        )

        mocks['do_body'].assert_called_once_with(
            mock_transition,
        ),

        mocks['on_exit'].assert_called_once_with(
            ReadOnlyStateWrapper(
                mock.ANY,
            ),
        )
        assert mocks['on_exit'].call_args[0][0].call_order == 1


def test_instance_attr_name_is_underscore():

    assert GoodState.get_instance_attr_name() == "good_state"


def test_on_entry_can_abort():
    state = GoodState(mock.Mock())
    with mock.patch.object(state, 'on_entry') as entry_patch:
        entry_patch.return_value = False

        transition = state.run(mock.MagicMock())

        assert transition.target == END

