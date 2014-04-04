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
