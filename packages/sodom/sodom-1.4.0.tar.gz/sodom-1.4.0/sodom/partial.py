__license__ = '''
sodom
Copyright (C) 2023  Dmitry Protasov (inbox@protaz.ru)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from typing import get_args, cast, get_origin
from typing import Any, Callable, Self
from functools import partial as _partial
from sodom.attrs import Attrs

from sodom.elements import ANY_ELEMENT, NormalElement, VoidElement


class partial[T](_partial[T]):
    def __new__(cls, func: Callable[..., T], /, *args: Any, **keywords: str) -> Self:
        result = super().__new__(cls, func, *args, **keywords)
        return result

    def __call__(self, /, *args: Any, **keywords: Any):
        keywords = Attrs(self.keywords).merge(**keywords)
        return self.func(*self.args, *args, **keywords)


def prebuild[ELEMENT](cls: type[ELEMENT] | partial[ELEMENT], *children: ANY_ELEMENT, **attrs: str) -> partial[ELEMENT]:
    if isinstance(cls, partial):
        constructor = cast(type[ELEMENT], cls.func)
        original_children = cast(tuple[ANY_ELEMENT], cls.args[1:])
        original_attrs = cast(dict[str, str], cls.keywords)
        merged_attrs = Attrs(original_attrs).merge(**attrs)
        return prebuild(constructor, *original_children, *children, **merged_attrs)
    elif issubclass(
        cast(type[ELEMENT], get_origin(cls)),
        (NormalElement, VoidElement),
    ):
        generics = get_args(cls)
        if not generics:
            raise TypeError('Invalid generic format.')
        tag_literal = generics[0]
        tag, = get_args(tag_literal)
        return partial(cls, tag, *children, **attrs)
    else:
        raise TypeError(f'Invalid type of cls: {type(cls)}. Check out signature.')
