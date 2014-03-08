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
from collections import namedtuple


class Transition(object):

    def __init__(self, target, **kwargs):
        self._target_state_class = target
        self._target_kwargs = kwargs
        self.origin = None

    @property
    def target(self):
        return self._target_state_class

    @property
    def kwargs(self):
        return self._target_kwargs

    def __repr__(self):
        return u"<Transition:{} --> {}>".format(self.origin, self.target)

END = namedtuple('END', [])()
START= namedtuple('START', [])()
