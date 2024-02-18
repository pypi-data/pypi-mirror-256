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

from itertools import starmap
from sodom.literals import SPECIAL_ATTRS


_attr_form = '{k}={q}{v}{q}'.format


class Attrs(dict[str, str]):
    '''
    Mapping allowing to merge attributes.
    Merge means adding attribute values to end of existing ones or create new attribute.
    For example:
    ```python
    Attrs(foo='bar').merge(foo='baz')
    Attrs(foo='bar').merge(**Attrs(foo='baz'))
    Attrs(foo='bar').merge(**dict(foo='baz'))
    Attrs(foo='bar') | Attrs(foo='baz')
    Attrs(foo='bar') | {'foo': 'baz'}
    ```
    returns
    ```python
    {'foo': 'bar baz'}
    ```
    Also supports "empty" attributes e.g. `disabled=''`. It be rendered as `<... disabled ...>`
    '''
    def __call__(self) -> None:
        from sodom.elements import CURRENT_ELEMENT

        if (parent := CURRENT_ELEMENT.get()) is None:
            raise RuntimeError('Attribute should be called in context of Normal Element.')

        parent.attrs.merge_update(**self)

    def __or__( # type: ignore
        self,
        other: 'Attrs | dict[str, str]',
    ) -> 'Attrs':
        return self.merge(**other)

    def merge(self, separator_: str = ' ', **right: str) -> 'Attrs':
        '''Merge attributes into new Attrs instance.'''
        result = Attrs(self)
        for k, v in right.items():
            result[k] = separator_.join(filter(
                bool,
                (
                    self.get(k, ''),
                    v,
                ),
            ))
        return result

    def merge_update(self, separator_: str = ' ', **other: str) -> None:
        '''Merge attributes inplace.'''
        self.update(self.merge(separator_, **other))

    def torows(
        self,
        *,
        quotes: str = '"',
        replace_underscores: bool = True
    ) -> list[str]:
        '''Build attrs (`dict[str, str]`) to `list[str]` with `f'{key}={quote}{value}{quote}'` format.'''

        result = list[str]()
        result_append = result.append

        for attr_name, attr_value in self.items():
            if attr_name := attr_name.strip('_'):
                if replace_underscores:
                    attr_name = attr_name.replace('_', '-')
                elif attr_name.split('_', 1)[0] in SPECIAL_ATTRS:
                    attr_name = attr_name.replace('_', '-', 1)

                if attr_value:  # attribute value must be significant otherwise empty will be rendered.
                    attr_content = _attr_form(k=attr_name, q=quotes, v=attr_value)
                else:
                    attr_content = attr_name

                result_append(attr_content)
        return result

    def torow(
        self,
        separator: str = ' ',
        *,
        quotes: str = '"',
        replace_underscores: bool = True,
    ) -> str:
        '''Same as Attrs.torows() but merge them into single string with `separator`.'''
        result = separator.join(self.torows(quotes=quotes, replace_underscores=replace_underscores))
        return result
